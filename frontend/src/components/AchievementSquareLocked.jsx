import {useState} from 'react';
import lock from "./pics/lock.png";
import {ProgressBar} from "./ProgressBar";

export const AchievementSquareLocked = (props) => {
    return (
        <>
        <div className = "drop-shadow-xl pb-[1%] pt-[1%] rounded-lg bg-slate-900 mx-auto w-[85%] mb-4">
            <div className = "text-gray-200 text-2xl text-center font-semibold">
                {props.Title}
            </div>
            <img className = "w-full h-[70%] mt-[1%]"
                src = {lock}
                alt = "lock" />
            <div className="w-[80%] h-[10%] mt-[5%] ml-[10%]">
                <div className='h-full w-full bg-gray-300 rounded-full'>
                    <div
                        style={{ width: `${props.unlockPercent}%`}}
                        className={'h-full bg-green-600 rounded-l-full'}>
                    </div>
                </div>
            </div>
        </div>
        </>
        );
}