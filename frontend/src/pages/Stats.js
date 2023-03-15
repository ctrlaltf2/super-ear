import React from "react";
import { StatsSquare } from "../components/StatsSquare";
import { GraphSquare } from "../components/GraphSquare";
import { PicSquare } from "../components/PicSquare";
function Stats(){

    const recentGames = [
        "11:30 2/17/23", "78%", "43",
        "11:30 2/17/23", "78%", "43",
        "11:30 2/17/23", "78%", "43",
        "11:30 2/17/23", "78%", "43",
        "11:30 2/17/23", "78%", "43", 
        "11:30 2/17/23", "78%", "43", 
        "11:30 2/17/23", "78%", "43", 
        "11:30 2/17/23", "78%", "43", 
        "11:30 2/17/23", "78%", "43", 
        "11:30 2/17/23", "78%", "43"];


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
        "G", "60%", "C"];
    
    const notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"];
    
    const noteConfusion = new Map([])
        
    for (let i of notes){
        for (let j of notes){
            noteConfusion.set(i + "-" + j, Math.random())
        }
        console.log(noteConfusion)
    }

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