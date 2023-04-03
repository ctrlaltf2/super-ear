import React from "react";
import {useState, useRef, useEffect } from 'react';
import {Oval} from 'react-loader-spinner';
import fretboard from '../components/pics/fretboard-notes.png';
import { FretMatrix } from '../components/FretMatrix';

function Play(){

    //state declaration
    const [curState, setCurState] = useState("connection_error");

    
    //component lifecycle (ws connection/disconnection)
    const ws = useRef();
    if (!ws.current) {
      ws.current = new WebSocket('ws://localhost:8000/game_session');
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
                <div className = "flex min-h-screen justify-center items-center text-8xl text-white">
                    <Oval
                        color="white"
                        secondaryColor="black"
                    />
                </div>
            </div>
        );
    }
    else if (curState == "waiting_for_play"){
        return(
        <div className = "min-h-screen bg-black">
            <div className = "flex min-h-screen justify-center items-center text-8xl text-white">
                Waiting For User To Play
                <Oval
                    color="white"
                    secondaryColor="black"
                />
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