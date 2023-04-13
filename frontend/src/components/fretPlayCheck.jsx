export const FretPlayCheck = (props) => {
    console.log(props);
    const color = ["bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600"];
    const opacity = ["opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0"];
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
    const pos = {        
        'A': [4, 9, 1, 6, 11, 4],
        'A#': [5, 10, 2, 7, 0, 5],
        'B': [6, 11, 3, 8, 1, 6],
        'C': [7, 0, 4, 9, 2, 7],
        'C#': [8, 1, 5, 10, 3, 8],
        'D': [9, 2, 6, 11, 4, 9],
        'D#': [10, 3, 7, 0, 5, 10],
        'E': [11, 4, 8, 1, 6, 11],
        'F': [0, 5, 9, 2, 7, 0],
        'F#': [1, 6, 10, 3, 8, 1],
        'G': [2, 7, 11, 4, 9, 2],
        'G#': [3, 8, 0, 5, 10, 3]};

    if ((props.expectedNote !== null) && (props.playedNote !== null)) {
        const expectedNotePos = pos[props.expectedNote][props.stringNum];
        const playedNotePos = pos[props.playedNote][props.stringNum];

        if (expectedNotePos == playedNotePos) {
            for (let i = 0; i < color.length; i++)
            {
                if (i == playedNotePos){
                    color[i] = "bg-green-600"
                    opacity[i] = "opacity-70"
                }
                else{
                    opacity[i] = "opacity-0"
                }
            }
        }
        else{
            for (let i = 0; i < color.length; i++)
            {
                if (i == playedNotePos){
                    color[i] = "bg-red-600"
                    opacity[i] = "opacity-70"
                }
                else if (i == expectedNotePos){
                    color[i] = "bg-blue-600"
                    opacity[i] = "opacity-70"
                }
                else{
                    opacity[i] = "opacity-0"
                }
            }
        }
}
    return (
    <div className="absolute inset-0 z-10 w-full h-full">
        <div className= {`flex ${offset}`}>
            {/**note 1 */}
            <div className="w-[4.45%] translate-x-[122.5%]">
                <div className={`w-full aspect-square ${color[0]} ${opacity[0]} rounded-full`}/>
            </div>
             {/**note 2 */}
            <div className="w-[4.45%] translate-x-[199%]">
                <div className={`w-full aspect-square ${color[1]} ${opacity[1]} rounded-full`}/>
            </div>
             {/**note 3 */}
            <div className="w-[4.45%] translate-x-[284.2%]">
                <div className={`w-full aspect-square ${color[2]} ${opacity[2]} rounded-full`}/>
            </div>
             {/**note 4 */}
            <div className="w-[4.45%] translate-x-[367.7%]">
                <div className={`w-full aspect-square ${color[3]} ${opacity[3]} rounded-full`}/>
            </div>
            {/**note 5 */}
            <div className="w-[4.45%] translate-x-[458%]">
                <div className={`w-full aspect-square ${color[4]} ${opacity[4]} rounded-full`}/>
            </div>
             {/**note 6 */}
            <div className="w-[4.45%] translate-x-[539%]">
                <div className={`w-full aspect-square ${color[5]} ${opacity[5]} rounded-full`}/>
            </div>
             {/**note 7 */}
            <div className="w-[4.45%] translate-x-[631%]">
                <div className={`w-full aspect-square ${color[6]} ${opacity[6]} rounded-full`}/>
            </div>
             {/**note 8 */}
            <div className="w-[4.45%] translate-x-[709.7%]">
                <div className={`w-full aspect-square ${color[7]} ${opacity[7]} rounded-full`}/>
            </div>
             {/**note 9 */}
            <div className="w-[4.45%] translate-x-[785.7%]">
                <div className={`w-full aspect-square ${color[8]} ${opacity[8]} rounded-full`}/>
            </div>
             {/**note 10 */}
            <div className="w-[4.45%] translate-x-[863.2%]">
                <div className={`w-full aspect-square ${color[9]} ${opacity[9]} rounded-full`}/>
            </div>
             {/**note 11 */}
            <div className="w-[4.45%] translate-x-[931.5%]">
                <div className={`w-full aspect-square ${color[10]} ${opacity[10]} rounded-full`}/>
            </div>
            {/**note 12 */}
            <div className="w-[4.45%] translate-x-[1002.5%]">
                <div className={`w-full aspect-square ${color[11]} ${opacity[11]} rounded-full`}/>
            </div>
        </div>
    </div>
    );
    };
