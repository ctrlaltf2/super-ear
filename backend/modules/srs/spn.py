import math
import re

from enum import Enum

# ref: https://en.wikipedia.org/wiki/Scientific_pitch_notation


class NoteModifier(Enum):
    DoubleFlat = -2
    Flat = -1
    Natural = 0
    Sharp = 1
    DoubleSharp = 2

    def __str__(self):
        match self:
            case NoteModifier.DoubleFlat:
                return "♭♭"
            case NoteModifier.Flat:
                return "♭"
            case NoteModifier.Natural:
                return ""
            case NoteModifier.Sharp:
                return "♯"
            case NoteModifier.DoubleSharp:
                return "♯♯"

    def __repr__(self):
        match self:
            case NoteModifier.DoubleFlat:
                return "bb"
            case NoteModifier.Flat:
                return "b"
            case NoteModifier.Natural:
                return ""
            case NoteModifier.Sharp:
                return "#"
            case NoteModifier.DoubleSharp:
                return "##"


# Class for scientific pitch notation
# Helper for music theory things
class SPN:
    # A-G
    tone_name: str

    # Octave #
    octave: int

    # Modifiers, (e.g. sharp, flat)
    modifier: NoteModifier

    def __init__(self, note, octave, modifier):
        self.tone_name = note
        self.octave = octave
        self.modifier = modifier

    def __str__(self):
        octave_as_str = {
            0: "₀",
            1: "₁",
            2: "₂",
            3: "₃",
            4: "₄",
            5: "₅",
            6: "₆",
            7: "₇",
            8: "₈",
            9: "₉",
        }

        if self.octave in octave_as_str:
            octave = octave_as_str[self.octave]
        else:
            octave = str(self.octave)

        return f"{self.tone_name}{octave}{self.modifier}"

    def __repr__(self):
        return f"SPNNote(tone={self.tone_name}, octave={self.octave}, modifier={self.modifier})"

    def __int__(self):
        tone_as_int = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

        tone = tone_as_int[self.tone_name]
        tone_modified = tone + self.modifier.value
        octave = self.octave

        # Check if need to change octave
        if tone_modified < 0:
            octave -= 1
            tone_modified += 12
        elif tone_modified > 11:
            octave += 1
            tone_modified -= 12

        return octave * 12 + tone_modified

    @staticmethod
    def from_int(note_int):
        octave = note_int // 12
        tone = note_int % 12

        tone_as_pair = {
            0: ("C", NoteModifier.Natural),
            1: ("C", NoteModifier.Sharp),
            2: ("D", NoteModifier.Natural),
            3: ("D", NoteModifier.Sharp),
            4: ("E", NoteModifier.Natural),
            5: ("F", NoteModifier.Natural),
            6: ("F", NoteModifier.Sharp),
            7: ("G", NoteModifier.Natural),
            8: ("G", NoteModifier.Sharp),
            9: ("A", NoteModifier.Natural),
            10: ("A", NoteModifier.Sharp),
            11: ("B", NoteModifier.Natural),
        }

        (tone_name, modifier) = tone_as_pair[tone]

        return SPN(tone_name, octave, modifier)

    @staticmethod
    def from_str(note_str):
        # Parse a string into an SPN object
        note_re = re.compile(r"([A-G])([s#b♯♭]{0,2})(\d\d?)")

        # Get the match groups
        match = note_re.match(note_str)

        if match is None:
            raise ValueError(f"Invalid note string: {note_str}")

        number_of_groups = len(match.groups())

        if number_of_groups <= 1:
            raise ValueError(f"Invalid note string: {note_str}")
        elif number_of_groups == 2:
            tone_name = match.group(1)
            modifier = ""
            octave = int(match.group(2))
        else:
            tone_name = match.group(1)
            modifier = match.group(2)
            octave = int(match.group(3))

        # Normalize modifier
        modifier = (
            modifier.replace("#", "s")
            .replace("♭", "b")
            .replace("♯", "s")
            .replace("♮", "")
            .replace("n", "")
            .replace("N", "")
        )

        if modifier == "s":
            modifier = NoteModifier.Sharp
        elif modifier == "ss":
            modifier = NoteModifier.DoubleSharp
        elif modifier == "b":
            modifier = NoteModifier.Flat
        elif modifier == "bb":
            modifier = NoteModifier.DoubleFlat
        elif modifier == "":
            modifier = NoteModifier.Natural
        else:
            raise ValueError(f"Unknown note modifier: '{modifier}'")

        # Construct the normal way
        spn_unnormalized = SPN(tone_name, octave, modifier)

        # Get the note integer
        note_int = int(spn_unnormalized)

        # Return the normalized version (normalized as in matches key on piano)
        return SPN.from_int(note_int)

    @staticmethod
    def from_freq(freq: float):
        # https://en.wikipedia.org/wiki/Piano_key_frequencies (adapted for my key numberings)
        note_int = round(12 * math.log2(freq / 440) + 57)
        return SPN.from_int(note_int)

    # -- Operators
    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __ne__(self, other):
        return int(self) != int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __add__(self, other):
        return SPN.from_int(int(self) + other)

    # Gets semitones between two notes
    def __sub__(self, other):
        return int(self) - int(other)
