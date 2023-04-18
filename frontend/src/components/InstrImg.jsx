import { FretPlayCheck } from "../components/fretPlayCheck";
import { KeyboardCheck } from "../components/KeyboardCheck";
import fretboard from '../components/pics/fretboard-notes.png';
import keyboard from '../components/pics/keyboard.png';

export const InstrImg = (props) => {
    if (props.instr === "guitar"){
        return(
        <div className="relative">
            <img className="w-full h-auto z-0"
                src={fretboard} 
                alt="fretboard">
            </img>
            <FretPlayCheck 
                stringNum = {props.stringNum}
                expectedNote = {props.expectedNote}
                playedNote = {props.playedNote}
            />
    </div>
        );
    }
    else if (props.instr === "piano"){
        return (
            <div className="relative">
                <img className="w-full h-auto z-0"
                    src={keyboard} 
                    alt="keyboard">
                </img>
                <KeyboardCheck 
                    expectedNote = {props.expectedNote}
                    playedNote = {props.playedNote}
                />
            </div>
        )
    }
};