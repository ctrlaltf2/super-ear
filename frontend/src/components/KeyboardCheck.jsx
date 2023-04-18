export const KeyboardCheck = (props) => {
    const color = ["bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600", "bg-green-600"];
    const opacity = ["opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0", "opacity-0"];
   
    const pos = {        
        'A': 9,
        'A#': 10,
        'B': 11,
        'C': 0,
        'C#': 1,
        'D': 2,
        'D#': 3,
        'E': 4,
        'F': 5,
        'F#': 6,
        'G': 7,
        'G#': 8};

    if ((props.expectedNote !== null) && (props.playedNote !== null)) {
        const expectedNotePos = pos[props.expectedNote];
        const playedNotePos = pos[props.playedNote];

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
        <div className= {"flex translate-y-[500%]"}>
            {/**note 1 */}
            <div className="w-[4.45%] translate-x-[110%]">
                <div className={`w-full aspect-square ${color[0]} ${opacity[0]} rounded-full`}/>
            </div>
             {/**note 2 */}
            <div className="w-[4.45%] translate-y-[-270%] translate-x-[127%]">
                <div className={`w-full aspect-square ${color[1]} ${opacity[1]} rounded-full`}/>
            </div>
             {/**note 3 */}
            <div className="w-[4.45%] translate-x-[190%]">
                <div className={`w-full aspect-square ${color[2]} ${opacity[2]} rounded-full`}/>
            </div>
             {/**note 4 */}
            <div className="w-[4.45%] translate-y-[-270%] translate-x-[253%]">
                <div className={`w-full aspect-square ${color[3]} ${opacity[3]} rounded-full`}/>
            </div>
            {/**note 5 */}
            <div className="w-[4.45%] translate-x-[265%]">
                <div className={`w-full aspect-square ${color[4]} ${opacity[4]} rounded-full`}/>
            </div>
             {/**note 6 */}
            <div className="w-[4.45%] translate-x-[440%]">
                <div className={`w-full aspect-square ${color[5]} ${opacity[5]} rounded-full`}/>
            </div>
             {/**note 7 */}
            <div className="w-[4.45%] translate-y-[-270%] translate-x-[452%]">
                <div className={`w-full aspect-square ${color[6]} ${opacity[6]} rounded-full`}/>
            </div>
             {/**note 8 */}
            <div className="w-[4.45%] translate-x-[510%]">
                <div className={`w-full aspect-square ${color[7]} ${opacity[7]} rounded-full`}/>
            </div>
             {/**note 9 */}
            <div className="w-[4.45%] translate-y-[-270%] translate-x-[549%]">
                <div className={`w-full aspect-square ${color[8]} ${opacity[8]} rounded-full`}/>
            </div>
             {/**note 10 */}
            <div className="w-[4.45%] translate-x-[585%]">
                <div className={`w-full aspect-square ${color[9]} ${opacity[9]} rounded-full`}/>
            </div>
             {/**note 11 */}
            <div className="w-[4.45%] translate-y-[-270%] translate-x-[650%]">
                <div className={`w-full aspect-square ${color[10]} ${opacity[10]} rounded-full`}/>
            </div>
            {/**note 12 */}
            <div className="w-[4.45%] translate-x-[660%]">
                <div className={`w-full aspect-square ${color[11]} ${opacity[11]} rounded-full`}/>
            </div>
        </div>
    </div>
    );
    };
