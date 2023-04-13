import {NavLink} from "react-router-dom"
import guitar from "../components/pics/guitar.png";
import * as Tone from 'tone'

export const PlayButton = (props) => {
    return (

        
    <div className="flex justify-center items-center h-screen">
        <div className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-b from-blue-400 to-blue-800 rounded-full blur-xl opacity-50 group-hover:opacity-100 transition duration-1000 group-hover:duration-1000"></div>
            <NavLink to="/play">
                <button
                    onClick={async () => {
                        await Tone.start()
                        console.log('audio is ready')
                    }}
                    className="relative w-24 h-24 rounded-full bg-blue-500 shadow-sm group-hover:scale-110 duration-1000 group-hover:duration-1000">
                    <img className="group-hover:opacity-75 duration-1000 group-hover:duration-1000"
                        src={guitar}
                    >
                    </img>
                </button>
            </NavLink>
        </div>
	</div>
    );
    }
