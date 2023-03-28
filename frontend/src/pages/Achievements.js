import React, {useEffect, useState} from "react";
import { AchievementSquare } from "../components/AchievementSquare";
import guitar from "../components/pics/guitar.png";

function getAchievementStatus(){
    return [false, false, false, false, false, false, false, false, false];
}
function getAchievementPercent(){
    return [0, 0, 0, 0, 0, 0, 0, 0, 0];
}

function Achievements(){
    
    useEffect(() => {checkAchievements()}, []);
    const [achievementStatus, setAchievementStatus] = useState(() => getAchievementStatus());
    const [achievementPercent, setAchievementPercent] = useState(() => getAchievementPercent()); 

    const changeStatusState = (index, val) => {
        setAchievementStatus(prevAchievementStatus => {
            return [...prevAchievementStatus.slice(0, index), 
                    val,
                    ...prevAchievementStatus.slice(index+1),]})
        }

    const changePercentState = (index, val) => {
        setAchievementPercent(prevAchievementPercent => {
            return [...prevAchievementPercent.slice(0, index), 
                    val,
                    ...prevAchievementPercent.slice(index+1),]})
    }

    const noteStats = new Map([
        ["A", "80%"],
        ["A#","80%"],
        ["B", "80%"],
        ["C", "30%"], 
        ["C#", "80%"],
        ["D", "90%"],
        ["D#", "100%"],
        ["E", "60%"],
        ["F", "60%"],
        ["F#", "60%"],
        ["G", "60%"]]);

    const recentGames = new Map([
            ["11:30 2/17/23", ["78%", "43"]],
            ["11:30 2/17/23", ["78%", "43"]],
            ["11:30 2/17/23", ["78%", "43"]],
            ["11:30 2/17/23", ["78%", "43"]],
            ["11:30 2/17/23", ["78%", "43"]], 
            ["11:30 2/17/23", ["78%", "43"]], 
            ["11:30 2/17/23", ["78%", "43"]], 
            ["11:30 2/17/23", ["78%", "43"]], 
            ["11:30 2/17/23", ["78%", "43"]], 
            ["11:30 2/17/23", ["78%", "43"]]]);
    
    function checkAchievements(){
        {/**Find Accuracies */}
        let maxAccuracy = 0;
        let totAccuracy = 0;
        for (let [key, value] of noteStats){
            let curInt = parseInt(value.substring(0, value.length-1));
            totAccuracy += curInt;
            maxAccuracy = Math.max(maxAccuracy, curInt);
        }
        totAccuracy = Math.floor(totAccuracy/12);

        {/**One Note Connoisseur */}
        changePercentState(3, Math.min(Math.floor((maxAccuracy/60) * 100), 100));
        if (maxAccuracy >= 70){
            changeStatusState(3, true);
        }
        else {
            changeStatusState(3, false);
        }
        {/**Sharp Ear, Sharper Ear, Sharpest Ear */}
        changePercentState(4, Math.min(Math.floor((totAccuracy/60) * 100), 100));
        changePercentState(5,Math.min(Math.floor((totAccuracy/70) * 100), 100));
        changePercentState(6, Math.min(Math.floor((totAccuracy/80) * 100), 100));

        if (totAccuracy >= 80){
            changeStatusState(4, true);
            changeStatusState(5, true);
            changeStatusState(6, true);
        }
        else if (totAccuracy >= 70){
            changeStatusState(4, true);
            changeStatusState(5, true);
            changeStatusState(6, false);
        }
        else if (totAccuracy >= 60){
            changeStatusState(4, true);
            changeStatusState(5, true);
            changeStatusState(6, false);
        }

        {/**Perfect Pitch*/}
        let maxSessAccuracy = 0;
        for (let [key, value] of recentGames){
            let curInt = parseInt(value[0].substring(0, value[0].length-1));
            maxSessAccuracy = Math.max(maxSessAccuracy, curInt);
        }

        changePercentState(7, Math.min(Math.floor((maxSessAccuracy/100) * 100), 100));
        if (maxSessAccuracy >= 100){
            changeStatusState(7, true);
        }
        else{
            changeStatusState(7, false);
        }
    } 

    return(
        <div className = "min-h-screen py-5 bg-gray-700 grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4">
            <AchievementSquare Unlocked = {achievementStatus[0]} unlockPercent={achievementPercent[0]} Title = "Dedicated" Descr="Play For a Total of 5 Hours" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[1]} unlockPercent={achievementPercent[1]} Title = "Quick Learner" Descr="Increase Your Accuracy By 5% In One Week" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[2]} unlockPercent={achievementPercent[2]} Title = "Dedicated II" Descr="Played For One Hour Today" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[3]} unlockPercent={achievementPercent[3]} Title = "One Note Connoisseur" Descr="Have an Accuracy Above 70% on a Note" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[4]} unlockPercent={achievementPercent[4]} Title = "Sharp Ear" Descr="Total Accuracy Above 60%" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[5]} unlockPercent={achievementPercent[5]} Title = "Sharper Ear" Descr="Total Accuracy Above 70%" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[6]} unlockPercent={achievementPercent[6]} Title = "Sharpest Ear" Descr="Total Accuracy Above 80%" Logo={guitar}/>
            <AchievementSquare Unlocked = {achievementStatus[7]} unlockPercent={achievementPercent[7]} Title = "Perfect Pitch" Descr="Get Every Note in a Session Correct" Logo={guitar}/>
        </div>
    );
};

export default Achievements;