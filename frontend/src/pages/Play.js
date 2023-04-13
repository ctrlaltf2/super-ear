import React from "react";
import {useState, useRef, useEffect } from 'react';
import {Oval} from 'react-loader-spinner';
import fretboard from '../components/pics/fretboard-notes.png';
import { HistoryBox } from '../components/HistoryBox';
import { FretPlayCheck } from "../components/fretPlayCheck";
import * as Tone from 'tone'

function Play(){

    //state declaration
    const [curState, setCurState] = useState("waiting_for_dsp");
    const [curNote, setCurNote] = useState(null);
    const [curAcc, setCurAcc] = useState([0, 0]);
    const [correct, setCorrect] = useState("");
    const [history, setHistory] = useState([]);
    const [counter, setCounter] = useState("00:00:00");
    const [stringNum, setStringNum] = useState();
    const [playedNote, setPlayedNote] = useState("");
    const [expectedNote, setExpectedNote] = useState("");

    //functions for history
    function addCorrectNote(){
        setHistory(prevHistory => prevHistory.concat([counter], [playedNote], [expectedNote]));
        const newAcc = curAcc.slice();
        newAcc[0] += 1;
        newAcc[1] += 1
        setCurAcc(newAcc);
        setCorrect = "Correct!"
    };
    function addIncorrectNote(){
        setHistory(prevHistory => prevHistory.concat([counter], [playedNote], [expectedNote]));
        const newAcc = curAcc.slice();
        newAcc[1] += 1
        setCurAcc(newAcc);
        setCorrect = "Incorrect, Keep Trying!"
    };

    //clock functions    
    function updateTimer(){
        let secs = 1 + parseInt(counter.slice(-2));
        let minutes = parseInt(counter.slice(3,5)); 
        let hours = parseInt(counter.slice(0, 2));
        if (secs >= 60){
            secs = 0;
            minutes += 1;
        }
        if (minutes >= 60){
            minutes = 0;
            hours += 1;
        }
        if (hours >= 99){
            hours = 0;
        }
        secs = secs.toString();
        if (secs.length == 1){
            secs = "0" + secs;
        }
        minutes = minutes.toString();
        if (minutes.length == 1){
            minutes = "0" + minutes;
        }
        hours = hours.toString();
        if (hours.length == 1){
            hours = "0" + hours;
        }
        setCounter(hours + ":" + minutes + ":" + secs)
    }
    useEffect(() =>{
            setTimeout(() => updateTimer(), 1000);
    }, [counter] )

    //component lifecycle (ws connection/disconnection)
    const ws = useRef();
    if (!ws.current) {
      ws.current = new WebSocket('ws://172.81.131.131:8000/game_session');
    }

    useEffect(() => {
        //create a synth and connect it to the main output (your speakers)
        const synth = new Tone.PolySynth().toDestination();

        const sampler = new Tone.Sampler({
            urls: {
                "F#1": "F%231.mp3",
                "C2": "C2.mp3",
                "F#2": "F%232.mp3",
                "C3": "C3.mp3",
                "F#3": "F%233.mp3",
                "A3": "A3.mp3",
                "C4": "C4.mp3",
                "F#4": "F%234.mp3",
                "C5": "C5.mp3",
                "C6": "C6.mp3",
            },
            release: 1,
            // baseUrl: `${window.location.origin}/guitar/`,
            baseUrl: `http://172.81.131.131:8000/guitar/`,
        }).toDestination();

        Tone.loaded().then(() => {
            console.log("loaded sampler");
        });

        //play a middle 'C' for the duration of an 8th note
        // synth.triggerAttackRelease("C4", "2n", "+0.3");

        // catch all

        ws.current.onopen = () => {
          console.log('connected')
        }
    
        ws.current.onmessage = (event) => {
            const json = JSON.parse(event.data);
            try {
                if ((json.event = "data")) {
                    console.log(json["type"])
                    console.log(json["payload"])

                    if (json["type"] === "state") {
                        setCurState(json["payload"]);
                        setExpectedNote(null);
                    } else if (json["type"] == "note played"){
                        let EN = json["payload"]["expected"];
                        EN = EN.substring(0, EN.length - 1);
                        let PN = json["payload"]["expected"];
                        PN = PN.substring(0, PN.length - 1);
                        setExpectedNote(EN)
                        setPlayedNote(PN)
                        if (EN == PN){
                            addCorrectNote()
                        }
                        else{
                            addIncorrectNote()
                        }
                    } else if(json["type"] === "should play") {
                        try { // why aren't exceptions documented
                            sampler.triggerAttackRelease(json["payload"], "2n", "+0.1");
                        } catch(err) {
                            console.warn("Error playing note: ", err);
                        }
                    }
                }
            } catch (err) {
                setCurState("connection_error");
            }
        };  
      }, [])
    
    const wsClose = () => {
       ws.current.close()
    }
    
    function stringSelector(string){
        setStringNum(string);
        setCounter("00:00:00");
        const message = JSON.stringify({
            "type": "string_select",
            "payload": string,
        });
        ws.current.send(message);
    }


    const gameStats = (
        <div className="grid grid-cols-3 w-full justify-center items-center text-center opacity-70">
        {/*History */}
        <div>
            <div className="text-white text-lg font-bold text-center">
                History
            </div>
            <div className="mt-[4%]">
            <div className = "grid grid-cols-3 text-center text-gray-200 text-sm font-light mb-1">
            {
                ["Time Played", "Played Note", "Expected Note"].map((elem) => {
                    return <h1>{elem}</h1>
                }
                )
            }
            </div>
                <HistoryBox history={history}/>
            </div>
        </div>
        {/*Accuracy and session time */}
        <div className="grid grid-cols-2 h-full justify-center items-center text-center text-gray-200 text-sm font-md">
            <div>
                Accuracy
                <div className="mt-[5%]">
                    {curAcc[0]} / {curAcc[1]}
                </div>
            </div>
            <div>
                Time Played
                <div className="mt-[5%]">
                    {counter}
                </div>
            </div>
        </div>
        {/**Fret Board */}
        {/*img*/}
        <div className="relative">
            <img className="w-full h-auto z-0"
                src={fretboard} 
                alt="fretboard">
            </img>
            <FretPlayCheck 
                stringNum = {stringNum}
                expectedNote = {expectedNote}
                playedNote = {playedNote}
            />
        </div>
    </div>
    );




    //Running
    if (curState == "waiting_for_dsp"){
        return(
            <div className = "min-h-screen bg-black">
                <div className = "flex min-h-screen justify-center items-center text-8xl text-white">
                        <div>
                            Please Connect To DSP
                        </div>
                        <Oval
                            color="white"
                            secondaryColor="black"
                        />
                </div>

        </div> 
        
    );
        }
    else if (curState == "string_select") {
        return(
        <div className = "min-h-screen bg-black">
            <h1 className="text-8xl text-white text-center"> Select A String</h1>
            <div className="relative w-[90%] py-[3%] mx-[5%]">
                                    
                <img className="w-full h-auto z-0"
                    src={fretboard} 
                    alt="fretboard">
                </img>
            </div>
            <div className='flex columns-2 items-center justify-center gap-x-4'>     
                <button onClick={() => stringSelector(0)} className="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                    E String
                </button>
                <button onClick={() => stringSelector(1)} className="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                    B String
                </button>
                <button onClick={() => stringSelector(2)} className="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                    G String
                </button>
                <button onClick={() => stringSelector(3)} className="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                    D String
                </button>
                <button onClick={() => stringSelector(4)} className="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                    A String
                </button>
                <button onClick={() => stringSelector(5)} className="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                    E String
                </button>
            </div>
        </div>
        );
    }
    else if (curState == "scheduling"){
        return(
                <div className = "min-h-screen grid grid-rows-2 bg-black justify-center items-center">
                    {/*game state and last note info*/}                    
                    <div className="grid grid-rows-3 items-center justify-center text-center w-[50%] ml-[25%]">
                        <div className="text-gray-200 text-8xl">
                            {correct}
                        </div>
                        <div className="text-gray-200 text-2xl grid grid-cols-2 items-center justify-center text-center">
                            <div>
                                Note Played: {playedNote}
                            </div>
                            <div>
                                Note Expected: {expectedNote}
                            </div>
                        </div>
                        <div className="text-lg text-gray-200 opacity-90 text-center items-center justify-center">
                            Scheduling Next Note...
                        </div>
                    </div>
                    {gameStats}
                </div>
        );
    }
    else if (curState == "waiting_for_play"){
        return(
            <div className = "min-h-screen grid grid-rows-2 bg-black justify-center items-center">
                    {/*game state and last note info*/}                    
                    <div className="grid grid-rows-3 items-center justify-center text-center w-[50%] ml-[25%]">
                        <div className="text-gray-200 text-8xl">
                            {correct}
                        </div>
                        <div className="text-gray-200 text-2xl grid grid-cols-2 items-center justify-center text-center">
                            <div>
                                Note Played: {playedNote}
                            </div>
                            <div>
                                Note Expected: {expectedNote}
                            </div>
                        </div>
                        <div className="text-lg text-gray-200 opacity-90 text-center">
                            Play The Note You Heard
                        </div>
                    </div>
                    {gameStats}
                </div>
        );
    }
    else if (curState == "scoring"){
        return(
                <div className = "min-h-screen grid grid-rows-2 bg-black justify-center items-center">
                    {/*game state and last note info*/}                    
                    <div className="grid grid-rows-3 items-center justify-center text-center w-[50%] ml-[25%]">
                        <div className="text-gray-200 text-8xl">
                            {correct}
                        </div>
                        <div className="text-gray-200 text-2xl grid grid-cols-2 items-center justify-center text-center">
                            <div>
                                Note Played: {playedNote}
                            </div>
                            <div>
                                Note Expected: {expectedNote}
                            </div>
                        </div>
                        <div className="text-lg text-gray-200 opacity-90 text-center">
                            Scoring...
                            <Oval
                            color="white"
                            secondaryColor="black"
                            />
                        </div>
                    </div>
                    {gameStats}
                </div>
        );
    }
    else if (curState == "remediating"){
        return(
                <div className = "min-h-screen grid grid-rows-2 bg-black justify-center items-center">
                    {/*game state and last note info*/}                    
                    <div className="grid grid-rows-3 items-center justify-center text-center w-[50%] ml-[25%]">
                        <div className="text-gray-200 text-8xl">
                            {correct}
                        </div>
                        <div className="text-gray-200 text-2xl grid grid-cols-2 items-center justify-center text-center">
                            <div>
                                Note Played: {playedNote}
                            </div>
                            <div>
                                Note Expected: {expectedNote}
                            </div>
                        </div>
                        <div className="text-lg text-gray-200 opacity-90 text-center">
                            Play The Note You Heard
                        </div>
                    </div>
                    {gameStats}
                </div>
        );
    }
    else if (curState == "review_done"){
        return(
                <div className = "min-h-screen grid grid-rows-2 bg-black justify-center items-center">
                    {/*game state and last note info*/}                    
                    <div className="grid grid-rows-3 items-center justify-center text-center w-[50%] ml-[25%]">
                        <div className="text-gray-200 text-8xl">
                            {correct}
                        </div>
                        <div className="text-gray-200 text-2xl grid grid-cols-2 items-center justify-center text-center">
                            <div>
                                Note Played: {playedNote}
                            </div>
                            <div>
                                Note Expected: {expectedNote}
                            </div>
                        </div>
                        <div className="text-lg text-gray-200 opacity-90 text-center">
                            Review Done!
                        </div>
                    </div>
                    {gameStats}
                </div>
        );
    }
    else if (curState == "connection_error"){
        return(
            <div className = "min-h-screen grid bg-black justify-center items-center text-8xl text-white text-center">
                Can't Connect To Websocket. Refresh The Page.
            </div>
        );  
    }
};

export default Play;
