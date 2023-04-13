from __future__ import annotations

import datetime
import inspect
import json
import logging  # call that deforestation
import pytz
import random

from copy import deepcopy
from enum import Enum
from typing import Callable, Any

import tornado.websocket
import tornado.escape
import tornado.options
from tornado.ioloop import IOLoop

# python moment: https://www.stefaanlippens.net/circular-imports-type-hints-python.html
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.dsp_session import DSPSession

from app.models.user import User
from app.models.history import ReviewHistory
from app.models.history_event import HistoryEvent
from app.models.track import Track
from app.models.review_item import ReviewItem, ReviewState
from app.core.srs.scheduler import OrderedReviewItem, V1
from app.core.srs.spn import SPN

logger = logging.getLogger(__name__)


class GameSessionSocketHandler(tornado.websocket.WebSocketHandler):
    class SessionState(Enum):
        START = "start"  # initial state
        WAITING_FOR_DSP = "waiting_for_dsp"  # waiting for a DSP to pair
        SELECTING_STRING = (
            "string_select"  # waiting for user to select a string/learning track
        )
        SCHEDULING = "scheduling"
        WAITING_FOR_PLAY = (
            "waiting_for_play"  # waiting for user to play a note on their instrument
        )
        SCORING = "scoring"  # game logic is scoring the response
        REMEDIATING = "remediating"  # user got it wrong, waiting for them to play again
        REVIEW_DONE = "review_done"  # user has finished reviewing for the moment

        def __str__(self):
            return self.value

    # on_open is a function callback
    cb_on_open: Callable

    # on_close is a function callback
    cb_on_close: Callable

    # socket for this connection. what's in the tuple depends on what the socket is.
    sock: tuple

    # Paired DSP session
    dsp_session: DSPSession | None

    # Pairing code, assigned by SuperEarApplication
    _pair_code: list[int] | None

    # State of the session
    _state: SessionState

    # username
    _username: str = "demo"

    # user object
    _user: User | None

    # history object
    _history: ReviewHistory | None

    # current review queue, if there is one
    _reviewing_queue: list[OrderedReviewItem] | None

    # item being reviewed, if there is one
    _next_item: OrderedReviewItem | None

    # scheduler used by the game
    _scheduler = V1

    # start time of the review session, if it exists
    _start_time: datetime.datetime | None

    async def get_current_user(self) -> str | None:
        if self.get_secure_cookie("user"):
            return tornado.escape.to_unicode(self.get_secure_cookie("user"))
        else:
            return None

    def __init__(self, *args, **kwargs):
        assert "on_open" in kwargs
        assert callable(kwargs["on_open"])

        assert "on_close" in kwargs
        assert callable(kwargs["on_close"])

        assert "on_message" in kwargs
        assert callable(kwargs["on_message"])

        self.cb_on_open = kwargs["on_open"]
        self.cb_on_close = kwargs["on_close"]
        self.cb_on_message = kwargs["on_message"]

        # oops
        del kwargs["on_open"]
        del kwargs["on_close"]
        del kwargs["on_message"]

        self.dsp_session = None
        self._pair_code = None
        self._user = None
        self._history = None
        self._reviewing_queue = None
        self._next_item = None
        self._start_time = None
        self._state = self.SessionState.START

        # call parent ctor
        super().__init__(*args, **kwargs)

    # oop
    def check_origin(self, _):
        return True

    #
    ## -- game logic --
    #

    # main multiplexer for game logic
    async def _process_message(self, typ: str, payload: Any):
        print("GameSessionSocketHandler::_process_message")
        match typ:
            case "string_select":
                self._string_select(payload)
                await self._set_state(self.SessionState.SCHEDULING)
                await self._init_scheduling()
                return
            case "exit_review":
                return  # TODO
            case "play":
                await self._handle_play(payload)
                return

        # if here, we didn't match any of the above cases
        self.send_frontend_message("error", f"Unknown message type: {typ}")

    async def _handle_play(self, payload: float):
        print("GameSessionSocketHandler::_handle_play")
        if self._state != self.SessionState.WAITING_FOR_PLAY:
            self._send_to_dsp("warning was not expecting a note play message. ignoring")
            return

        assert (
            self._user is not None
        ), "pre: user should be authenticated. bad state mgmt or missed assumptions in getting to here"
        assert self._next_item is not None, "pre: _expected_note is None"
        assert self._start_time is not None, "pre: _start_time is None"
        assert (
            self._reviewing_queue is not None
        ), "pre: _reviewing_queue is None, it should be initialized here"

        actual_note: SPN = SPN.from_freq(payload)
        expected_note: SPN = SPN.from_str(self._next_item.item.content)

        print(f"actual note: {repr(actual_note)}, expected note: {repr(expected_note)}")

        note_distance: int = abs(actual_note - expected_note)
        due_prev = deepcopy(self._next_item.due_date)

        do_readd: bool = self._scheduler.review(
            self._user.collection, self._next_item.item, note_distance, 0
        )
        await self._sync_collection()  # sync
        await self._update_history(
            self._next_item.item, actual_note, due_prev, self._next_item.item.state
        )

        if do_readd:
            if len(self._reviewing_queue) > 0:
                # then insert in a random place that's not at the start- minimize repeats
                self._reviewing_queue.insert(
                    random.randint(1, len(self._reviewing_queue)), self._next_item
                )
            else:  # just insert at the start
                self._reviewing_queue.insert(0, self._next_item)

        print(" ".join([str(item.item.content) for item in self._reviewing_queue]))

        to_send = {"expected": repr(expected_note), "played": repr(actual_note)}

        self.send_frontend_message("note played", to_send)
        await self._try_send_next_review()

    async def _init_scheduling(self):
        assert self._user is not None, "pre: _init_scheduling called before _user set"
        assert (
            self._state == self.SessionState.SCHEDULING
        ), "pre: _state should be SCHEDULING"

        self._reviewing_queue = self._scheduler.generate_reviewing_queue(
            self._user.collection
        )

        self._start_time = datetime.datetime.now(tz=pytz.utc)

        await self._try_send_next_review()

    # given a review queue, try to send the next review item
    async def _try_send_next_review(self):
        assert self._reviewing_queue is not None, "pre: _reviewing_queue is None"

        if len(self._reviewing_queue) == 0:
            await self._set_state(self.SessionState.REVIEW_DONE)
            return

        self._next_item = self._reviewing_queue.pop(0)

        # send to DSP the frequeny
        expected_freq = SPN.from_str(self._next_item.item.content).to_freq()

        self._send_to_dsp(f"play {expected_freq}")
        self.send_frontend_message(
            "should play", repr(SPN.from_str(self._next_item.item.content))
        )

        await self._set_state(self.SessionState.WAITING_FOR_PLAY)

    # Called when the user selects a string to study
    def _string_select(self, identifier: Any):
        if self._state != self.SessionState.SELECTING_STRING:
            self.send_frontend_message(
                "error",
                "Wasn't expecting a string select command. Ignoring.",
            )
            return

        if type(identifier) == int or type(identifier) == str:
            try:
                self._set_active_track(identifier)
            except ValueError:
                self.send_frontend_message(
                    "error",
                    "Invalid track identifier. Use string # as an int or String name (e.g. 'String 1')",
                )

            # send confirmation message
            self.send_frontend_message("string_select", identifier)
        else:
            self.send_frontend_message(
                "error", "Invalid track identifier type. Use a string or integer"
            )

    # mirrors a state machine
    async def _set_state(self, next_state: SessionState):
        prev_state = self._state
        self._state = next_state

        match prev_state:
            case [
                self.SessionState.SCHEDULING,
                self.SessionState.SCORING,
                self.SessionState.REMEDIATING,
                self.SessionState.SCORING,
                self.SessionState.WAITING_FOR_PLAY,
            ]:
                match next_state:
                    case self.SessionState.WAITING_FOR_DSP:  # --> dsp d/c'd mid-play
                        if self._reviewing_queue is not None:
                            await self._sync_collection()

        self.send_frontend_message("state", str(next_state))

    # async candidate
    def _send_to_dsp(self, msg: str):
        print(f"Sending to DSP: {msg}")
        if self.dsp_session is None:
            return

        assert (
            self._state != self.SessionState.WAITING_FOR_DSP
        ), "shouldn't be sending to dsp if we're waiting for one to pair"

        self.dsp_session.send_message(msg)

    #
    ## -- collection-related things --
    #
    def _get_active_track(self) -> Track:
        assert self._user is not None, "_get_active_track called before _user set"
        col = self._user.collection
        return col.get_active_track()

    def _set_active_track(self, identifier: str | int) -> None:
        assert self._user is not None, "_set_active_track called before _user set"
        col = self._user.collection
        col.set_active_track(identifier)

    #
    ## -- database-related things --
    #
    # synchronizes the collection in self._user with the database
    # ~technically~ this should be done per review item and NOT the full collection but oh well
    async def _sync_collection(self):
        assert self._user is not None, "pre: _user is None in sync collection"
        await self._user.save_changes()

    # updates the history table with the given review item and the note played
    async def _update_history(
        self,
        item: ReviewItem,
        actual_note: SPN,
        due_date: datetime.datetime,
        new_state: ReviewState,
    ):
        assert self._history is not None, "pre: _history is None in update history"

        expected_note = SPN.from_str(item.content)

        # add new list if doesn't exist
        if str(expected_note) not in self._history.events:
            self._history.events[str(expected_note)] = []

        now = datetime.datetime.now(tz=pytz.utc)

        # make a history item
        history_event_now = HistoryEvent(
            time=now,
            answer=str(actual_note),
            ease_factor=item.ease_factor,
            review_offset=(due_date - now) / datetime.timedelta(hours=1),
            state=new_state,
        )

        # append & save
        self._history.events[str(expected_note)].append(history_event_now)
        await self._history.save()

    # populates self._history and creates it if it doesn't exist
    async def _init_history(self):
        assert self._user is not None, "pre: _user is None in init history"
        search_result = await ReviewHistory.find_one(
            ReviewHistory.user_uuid == self._user.uuid
        )

        if search_result is None:  # create
            self._history = ReviewHistory(user_uuid=self._user.uuid)
            await self._history.save()
        else:  # pull
            self._history = search_result

        assert self._history is not None, "post: _history is None"

    #
    ## -- tornado-related things --
    #

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def set_default_headers(self) -> None:
        self.set_header("Server", "")

    async def open(self) -> None:
        assert self.ws_connection is not None
        assert self.ws_connection.stream is not None
        assert self.ws_connection.stream.socket is not None

        if not tornado.options.options.demo:
            # check auth
            possible_username = await self.get_current_user()

            if possible_username is None:
                self.close(code=401, reason="Unauthorized")
                return
        else:
            possible_username = "demo"

        print(f"Auth'd as {possible_username}")

        self._username = possible_username

        self.sock = self.ws_connection.stream.socket.getpeername()

        await self._set_state(self.SessionState.WAITING_FOR_DSP)

        assert (
            self._state == self.SessionState.WAITING_FOR_DSP
        ), "post: set state should set the state"

        # TODO: Auth
        search_result = await User.find_one(User.username == self._username)
        assert (
            search_result is not None
        ), f"user '{possible_username}' not found, is the database bootstrapped?"
        self._user = search_result

        # then with user setup, initialize history
        await self._init_history()

        if inspect.iscoroutinefunction(self.cb_on_open):
            await self.cb_on_open(self.sock, self)
        else:
            self.cb_on_open(self.sock, self)

    def on_close(self) -> None:
        if inspect.iscoroutinefunction(self.cb_on_close):
            IOLoop.current().add_callback(self.cb_on_close, self.sock)
        else:
            self.cb_on_close(self.sock)

    async def on_message(self, message: str) -> None:
        assert self.ws_connection is not None
        assert self.ws_connection.stream is not None
        assert self.ws_connection.stream.socket is not None
        assert (
            self.ws_connection.stream.socket.getpeername() == self.sock
        )  # should be turned off for prod

        # decode JSON message
        try:
            data = tornado.escape.json_decode(message)
        except ValueError:
            self.send_frontend_message("error", "Invalid JSON")
            return

        print(f"Got message: {data}")

        # validate message
        if not isinstance(data, dict):
            return

        if "type" not in data:
            self.send_frontend_message("error", "JSON message missing 'type' attribute")
            return

        if "payload" not in data:
            self.send_frontend_message(
                "error", "JSON message missing 'payload' attribute"
            )
            return

        assert type(data["type"]) == str, "message type should be string"

        if inspect.iscoroutinefunction(self.cb_on_message):
            await self.cb_on_message(self.sock, data)
        else:
            self.cb_on_message(self.sock, data)

        await self._process_message(data["type"], data["payload"])

    #
    ## -- things called by external things --
    #

    def assign_pair_code(self, pair_code: list[int]):
        assert self._pair_code is None
        self._pair_code = pair_code

    async def pair(self, dsp_session: DSPSession) -> None:
        assert self.dsp_session is None, "Already paired"
        self.dsp_session = dsp_session
        await self._set_state(self.SessionState.SELECTING_STRING)

        assert (
            self._state == self.SessionState.SELECTING_STRING
        ), "post: set state should set the state"

    async def unpair(self):
        self.dsp_session = None
        await self._set_state(self.SessionState.WAITING_FOR_DSP)

        assert (
            self._state == self.SessionState.WAITING_FOR_DSP
        ), "post: set state should set the state"

    # Sends a message to the connected frontend client
    def send_frontend_message(self, type: str, data: float | int | str | list | dict):
        print("Sending message to frontend")
        msg = json.dumps({"type": type, "payload": data})
        self.write_message(msg)
