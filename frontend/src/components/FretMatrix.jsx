import { FretNoteHighlight } from "./FretNoteHighlight";

export const FretMatrix = (props) => {
    const offset = stringNumToOffset();
    function stringNumToOffset(){
        if (props.stringNum == 0) {
            return "translate-y-[0%]";
        }
        else if (props.stringNum == 1) {
            return "translate-y-[108%]";
        }
        else if (props.stringNum == 2) {
            return "translate-y-[216%]";
        }
        else if (props.stringNum == 3) {
            return "translate-y-[324%]";
        }
        else if (props.stringNum == 4) {
            return "translate-y-[432%]";
        }
        else if (props.stringNum == 5) {
            return "translate-y-[543%]";
        }
    };


    const noteStats = new Map([
        ["A", 80],
        ["A#", 20],
        ["B", 10],
        ["C", 10], 
        ["C#", 10],
        ["D", 10],
        ["D#", 100],
        ["E", 60],
        ["F", 60],
        ["F#", 60],
        ["G", 60],
        ["G#", 10]]);
    const pos = [
        ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"],
        ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
        ["G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],
        ["D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"],
        ["A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],
        ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]];
    return (
    <div className="absolute inset-0 z-10 w-full h-full">
        <div className= {`flex ${offset}`}>
            <div className="w-[4.45%] translate-x-[122.5%]">
                <FretNoteHighlight 
                xOffset = "122.5%"
                percent = {noteStats.get(pos[props.stringNum][0])} />  
            </div>
            <div className="w-[4.45%] translate-x-[199%]">
                <FretNoteHighlight 
                    xOffset = "199%"
                    percent = {noteStats.get(pos[props.stringNum][1])}/>
            </div>
            <div className="w-[4.45%] translate-x-[284.2%]">
                <FretNoteHighlight 
                    xOffset = "284.2%"
                    percent = {noteStats.get(pos[props.stringNum][2])}/>
            </div>
            <div className="w-[4.45%] translate-x-[367.7%]">
                <FretNoteHighlight
                    xOffset ="369%"
                    percent = {noteStats.get(pos[props.stringNum][3])}/>
            </div>
            <div className="w-[4.45%] translate-x-[458%]">
                <FretNoteHighlight 
                        xOffset = "458%"
                        percent = {noteStats.get(pos[props.stringNum][4])}/>
            </div>
            <div className="w-[4.45%] translate-x-[539%]">
                <FretNoteHighlight 
                    xOffset = "539%"
                    percent = {noteStats.get(pos[props.stringNum][5])}/>
            </div>
            <div className="w-[4.45%] translate-x-[631%]">
                <FretNoteHighlight 
                    xOffset = "631%"
                    percent = {noteStats.get(pos[props.stringNum][6])}/>
            </div>
            <div className="w-[4.45%] translate-x-[709.7%]">
                <FretNoteHighlight 
                    xOffset = "709.7%"
                    percent = {noteStats.get(pos[props.stringNum][7])}/>
            </div>
            <div className="w-[4.45%] translate-x-[785.7%]">
                <FretNoteHighlight 
                    xOffset = "785.7%"
                    percent = {noteStats.get(pos[props.stringNum][8])}/>
            </div>
            <div className="w-[4.45%] translate-x-[863.2%]">
                <FretNoteHighlight 
                    xOffset = "863.2%"
                    percent = {noteStats.get(pos[props.stringNum][9])}/>
            </div>
            <div className="w-[4.45%] translate-x-[931.5%]">
                <FretNoteHighlight
                    xOffset = "931.5%"
                    percent = {noteStats.get(pos[props.stringNum][10])}/>
            </div>
            <div className="w-[4.45%] translate-x-[1002.5%]">
                <FretNoteHighlight 
                    xOffset = "1002.5%"
                    percent = {noteStats.get(pos[props.stringNum][11])}/>
            </div>
        </div>
    </div>
  );
};