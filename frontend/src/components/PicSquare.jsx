import {useState } from 'react'
import { PicModal } from './PicModal';
import fretboard from './pics/fretboard-notes.png';
export const PicSquare = (props) => {
    const [modal, setModal] = useState(false)
    function handleClick() {
        setModal(true)
    }

    return (
        <>
        <PicModal 
            Title = {props.Title}
            open = {modal}
            close = {setModal}
        />

        <div className= "cursor-pointer shadow-2xl mx-[5%] my-[2%] rounded-lg bg-slate-800 hover:transition-all hover:bg-slate-600 w-[90%] h-[90%]" onClick = {() => handleClick()}>
            {<button type="button" onClick={() => props.onPress}></button>}
            {/*title*/}
            <div className= "text-gray-200 text-2xl text-center font-semibold">
                {props.Title}
            </div>
            {/*img*/}
            <img className = "w-[90%] my-[10%] mx-[5%]"
                src={fretboard} 
                alt="fretboard"/>
        </div>

        </>
        );
};