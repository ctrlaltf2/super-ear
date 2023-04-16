import React from "react";
import { PlayBackground } from "../components/PlayBackground";
import basePic from "../components/pics/blank-profile-picture-.png";
import{ ProgressBar } from "../components/ProgressBar";

function Dashboard(){
    return(
        <div className = "min-h-screen grid grid-cols-2 bg-gray-700">
                <PlayBackground />
            <div className = "text-center text-gray-200 text-4xl mt-[10%]">
                <p> Hello, User!</p>
                <img className = "w-1/4 aspect-square rounded-full mx-auto shadow-2xl drop-shadow-2xl mt-[5%] mb-[5%]" 
                alt = ""
                src = {basePic}/>
                <p> Current Rank: </p>
                    <p className = 'text-yellow-600 mt-[2%] mb-[2%]'> GOLD 3</p>
                <p> Progress to next Rank:</p>
                <div className = "ml-[25%] mr-[25%] h-8 w-1/2 mt-[2%] mb-[2%]">
                <ProgressBar progressPercentage={30}
                />
                </div>
            </div>
        </div>

    );
};

export default Dashboard;