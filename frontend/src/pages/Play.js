import React from "react";
import {useState} from 'react';
function Play(){

    const [bids, setBids] = useState([0]);

    const ws = new WebSocket("localhost:3000/game_session");

    const apiCall = {
        event: "bts:subscribe",
        data: { channel: "order_book_btcusd" },
    };

    ws.onopen = (event) => {
        ws.send(JSON.stringify(apiCall));
    };

    ws.onmessage = function (event) {
        const json = JSON.parse(event.data);
        try {
            if ((json.event = "data")) {
                setBids(json.data.bids.slice(0,5));
            }
        } catch (err) {
            console.log("error")
        }
    };

    const firstBids = bids.map((item) =>{
        return (
            <div>
                <p> {item} </p>
            </div>
        );
    });

    return(
        <div class = "min-h-screen bg-black">
            <div class = "flex min-h-screen justify-center items-center text-8xl text-white">
                <div>{firstBids} </div>
            </div>
        </div>
    );
};

export default Play;