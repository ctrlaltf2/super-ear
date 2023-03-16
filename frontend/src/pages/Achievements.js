import React from "react";
import { AchievementSquare } from "../components/AchievementSquare";
import guitar from "../components/pics/guitar.png";
function Achievements(){
    return(
        <div className = "min-h-screen py-5 bg-gray-700 grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4">
            <AchievementSquare Unlocked = {true} unlockPercent={100} Title = "Dedicated" Descr="Play For a Total of 5 Hours" Logo={guitar}/>
            <AchievementSquare Unlocked = {true} unlockPercent={100} Title = "Quick Learner" Descr="Increase Your Accuracy By 5% In One Week" Logo={guitar}/>
            <AchievementSquare Unlocked = {true} unlockPercent={100} Title = "Dedicated II" Descr="Played For One Hour Today" Logo={guitar}/>
            <AchievementSquare Unlocked = {true} unlockPercent={100} Title = "One Note Connoisseur" Descr="Have an Accuracy Above 70% on a Note" Logo={guitar}/>
            <AchievementSquare Unlocked = {true} unlockPercent={100} Title = "Sharp Ear" Descr="Total Accuracy Above 60%" Logo={guitar}/>
            <AchievementSquare Unlocked = {false} unlockPercent={30} Title = "Sharper Ear" Descr="Total Accuracy Above 70%" Logo={guitar}/>
            <AchievementSquare Unlocked = {false} unlockPercent={20} Title = "Sharpest Ear" Descr="Total Accuracy Above 80%" Logo={guitar}/>
            <AchievementSquare Unlocked = {false} unlockPercent={50} Title = "Perfect Pitch" Descr="Get Every Note in a Session Correct" Logo={guitar}/>
        </div>
    );
};

export default Achievements;