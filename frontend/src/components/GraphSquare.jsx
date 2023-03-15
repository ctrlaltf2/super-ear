import {useState } from 'react'
import { GraphModal } from './GraphModal';
import {LineGraph} from './LineGraph';




export const GraphSquare = (props) => {
    const [modal, setModal] = useState(false)
    function handleClick() {
        setModal(true)
    }
    
    return (
        <>
        <GraphModal 
            open = {modal}
            close = {setModal}
            Title = "Your Progress"
        />

        <div className = "cursor-pointer shadow-2xl mx-[5%] my-[2%] rounded-lg bg-slate-800 hover:transition-all hover:bg-slate-600 w-[90%] h-[90%]" onClick = {() => handleClick()}>
            {<button type="button" onClick={() => props.onPress}></button>}
            {/*title*/}
            <div className = "text-gray-200 text-2xl text-center font-semibold">
                {props.Title}
            </div>
            {/**Graph */}
            <div className = "pt-[6%]">
                <LineGraph /> 
            </div>








        </div>
    
        </>
        );
};