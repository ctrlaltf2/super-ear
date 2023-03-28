export const FretNoteHighlight = (props) => {
    const color = percentToColor()
    function percentToColor(){
        if (props.percent <= 10) {
            return ["bg-red-600", "opacity-80"];
        }
        else if (props.percent <= 20) {
            return ["bg-red-600", "opacity-70"];
        }
        else if (props.percent <= 20) {
            return ["bg-red-500", "opacity-60"];
        }
        else if (props.percent <= 30) {
            return ["bg-red-300", "opacity-50"];
        }
        else if (props.percent <= 40) {
            return ["bg-red-300", "opacity-40"];
        }
        else if (props.percent <= 50) {
            return ["bg-red-300", "opacity-30"];
        }
        else if (props.percent <= 60) {
            return ["bg-green-600", "opacity-50"];
        }
        else if (props.percent <= 70) {
            return ["bg-green-600", "opacity-60"];
        }
        else if (props.percent <= 80) {
            return ["bg-green-600", "opacity-70"];
        }
        else {
            return ["bg-green-600", "opacity-80"];
        }

    };
    return (
        <tooltip title={(props.percent).toString().concat("%")} className="bg-slate-700">
            <div className={`w-full aspect-square ${color[0]} ${color[1]} rounded-full`}/>
        </tooltip>

  );
};