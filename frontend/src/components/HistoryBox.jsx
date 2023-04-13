export const HistoryBox = (props) => {
    return(
        <div className = "grid grid-cols-2 text-center text-gray-200 text-sm font-light mb-1 overflow-y-auto h-24">
        {
            props.history.map((elem, index) => 
            {
                return <p className = "text-sm font-light my-[4%]" key={index}>{elem}</p>
            }
            )
        }
        </div>            
    );
};