import {useState } from 'react'
import { StatsModal } from './StatsModal';

export const StatsSquare = (props) => {
    const [modal, setModal] = useState(false)
    function handleClick() {
        setModal(true)
    }
    const numCols = props.numCols
    const titleList = props.ColTitles
    const statsList = props.stats
    return (
        <>
        <StatsModal 
            Title = {props.Title}
            ColTitles = {props.ColTitlesModal}
            numCols = {props.numColsModal}
            statsList = {props.statsListModal}
            open = {modal}
            close = {setModal}
        />

        <div className = "cursor-pointer shadow-2xl mx-[5%] my-[2%] rounded-lg bg-slate-800 hover:transition-all hover:bg-slate-600 w-[90%] h-[90%]" onClick = {() => handleClick()}>
            {<button type="button" onClick={() => props.onPress}></button>}
            {/*title*/}
            <div className = "text-gray-200 text-2xl text-center font-semibold">
                {props.Title}
            </div>
            {/*stat tables*/}
            {/* column titles */}
            <div className = {`grid grid-cols-3 text-center text-gray-200 text-md font-medium mt-[5%] mb-1`}>
                {
                    titleList.map((elem) => {
                        return <h1>{elem}</h1>
                    }
                    )
                }
                                {
                    statsList.map((elem, index) => {
                        return <p className = "text-sm font-light my-[4%]" key={index}>{elem}</p>
                    }
                    )
                }
            </div>
        </div>

        </>
        );
};