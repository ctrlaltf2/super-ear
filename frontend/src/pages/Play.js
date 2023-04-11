import React from "react";
import {useState, useRef, useEffect } from 'react';
import {Oval} from 'react-loader-spinner';
import fretboard from '../components/pics/fretboard-notes.png';
import { FretMatrix } from '../components/FretMatrix';
import { HistoryBox } from '../components/HistoryBox';

function Play(){

    //state declaration
    const [curState, setCurState] = useState("connection_error");
    const [curNote, setCurNote] = useState(null);
    const [curAcc, setCurAcc] = useState([0, 0]);
    const [history, setHistory] = useState([]);
    const [counter, setCounter] = useState("00:00:00");

    //functions for history
    function addCorrectNote(){
        setHistory(prevHistory => prevHistory.concat(["00:00:00"], ["A"], ["A"]));
        const newAcc = curAcc.slice();
        newAcc[0] += 1;
        newAcc[1] += 1
        setCurAcc(newAcc);
    };
    function addIncorrectNote(){
        setHistory(prevHistory => prevHistory.concat(["00:00:00"], ["A"], ["B"]));
        const newAcc = curAcc.slice();
        newAcc[1] += 1
        setCurAcc(newAcc);
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
    }, [counter])

    //component lifecycle (ws connection/disconnection)
    const ws = useRef();
    if (!ws.current) {
      ws.current = new WebSocket('ws://172.81.131.131:8000/game_session');
    }

    useEffect(() => {

        ws.current.onopen = () => {
          console.log('connected')
        }
    
        ws.current.onmessage = (event) => {
            const json = JSON.parse(event.data);
            try {
                if ((json.event = "data")) {
                    console.log(json["type"])
                    console.log(json["payload"])
                    
                    if (json["type"] == "state") {
                        setCurState(json["payload"]);
                        setCurNote(null);
                    }
                    else if(json["type"] == "note played"){
                        setCurNote(json["payload"])

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
        const message = JSON.stringify({
            "type": "string_select",
            "payload": string,
        });
        ws.current.send(message);
    }


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
        <div className = "min-h-screen bg-black">
                <div className = "flex flex-col min-h-screen justify-center items-center text-8xl text-white">
                    <Oval
                        color="white"
                        secondaryColor="black"
                    />
                    <div className="flex flex-row justify-center items-center text-center pt-[5%] text-4xl w-full text-white opacity-70">
                    <div className="flex-1">
                        Accuracy
                        <div className="mt-[5%]">
                            {curAcc[0]} / {curAcc[1]}
                        </div>
                    </div>
                    <div className="flex-1">
                        Time Played
                        <div className="mt-[5%]">
                            {counter}
                        </div>
                    </div>
                    <div className="flex-1">
                        History
                        <div className="mt-[5%]">
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
                </div>
                </div>
            </div>
        );
    }
    else if (curState == "waiting_for_play"){
        return(
        <div className = "min-h-screen bg-black">
            <div className = "flex flex-col min-h-screen justify-center items-center text-8xl text-white">
                {curNote}
            <div className="flex flex-row justify-center items-center text-center pt-[5%] text-4xl w-full text-white opacity-70">
                    <div className="flex-1">
                        Accuracy
                        <div className="mt-[5%]">
                            {curAcc[0]} / {curAcc[1]}
                        </div>
                    </div>
                    <div className="flex-1">
                        Time Played
                        <div className="mt-[5%]">
                            {counter}
                        </div>
                    </div>
                    <div className="flex-1">
                        History
                        <div className="mt-[5%]">
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
                </div>
            </div>
        </div>
        );
    }
    else if (curState == "scoring"){
        return(
        <div className = "min-h-screen bg-black">
            
        </div>
        );
    }
    else if (curState == "remediating"){
        return(
        <div className = "min-h-screen bg-black">
            
        </div>
        );
    }
    else if (curState == "review_done"){
        return(
        <div className = "min-h-screen bg-black">
            
        </div>
        );
    }
    else if (curState == "connection_error"){
        return(
        <div className = "min-h-screen bg-black">
            <div className = "flex min-h-screen justify-center items-center text-8xl text-white">
                Can't Connect to Websocket, Please Reload
            </div>
        </div>
        );  
    }
};

export default Play;