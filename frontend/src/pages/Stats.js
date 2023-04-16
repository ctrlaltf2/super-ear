import React from "react";
import { StatsSquare } from "../components/StatsSquare";
import { GraphSquare } from "../components/GraphSquare";
import { PicSquare } from "../components/PicSquare";
function Stats(){

    const recentGames = [
        "11:30 7/17/23", "78%", "30",
        "10:30 7/15/23", "80%", "30",
        "10:23 7/15/23", "68%", "30",
        "10:30 7/13/23", "77%", "25",
        "09:20 7/12/23", "73%", "30", 
        "10:09 7/11/23", "70%", "45", 
        "08:54 7/10/23", "69%", "40", 
        "14:50 7/06/23", "90%", "50", 
        "19:32 7/06/23", "60%", "60", 
        "11:31 7/05/23", "70%", "70"];


  
    
    const notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"];
    
    const noteConfusion = new Map([])
        
    for (let i of notes){
        for (let j of notes){
            noteConfusion.set(i + "-" + j, Math.random())
        }
        console.log(noteConfusion)
    }

    const noteStats = [
    "A", "78%", "B",
    "A#", "40%", "A",
    "B", "30%", "A",
    "C", "20%", "C#",
    "C#", "10%", "D",
    "D", "5%", "C#",
    "D#", "80%", "E",
    "E", "50%", "F",
    "F", "30%", "G",
    "F#", "40%", "A",
    "G", "60%", "C",
    "G#", "10%", "C"]; 

    return(
        <div className = "min-h-screen bg-gray-700 grid sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2">
                    <StatsSquare 
                    Title = "Recent Games"
                    ColTitles = {["Time", "Accuracy", "Notes Tested"]}
                    ColTitlesModal = {["Time", "Accuracy", "Notes Tested"]}
                    stats = {recentGames.slice(0, 15)}
                    statsListModal = {recentGames}
                    numColsModal = {3}
                    numCols = {3}
                    />
                    <GraphSquare 
                    Title = "Your Progress"
                    />
                    <StatsSquare 
                    Title = "Stats on Notes"
                    ColTitles = {["Note", "Accuracy", "Most Confused For"]}
                    ColTitlesModal = {["Note", "Accuracy", "Most Confused For"]}
                    stats = {noteStats.slice(0, 15)}
                    statsListModal = {noteStats}
                    numColsModal = {3}
                    numCols = {3}
                    />
                    <PicSquare 
                    Title = "Areas of Improvement"
                    noteMatrix = {noteConfusion}
                     />
        </div>
    );
};

export default Stats;