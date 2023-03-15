import {NavLink} from "react-router-dom"

export const PlayButton = (props) => {
    return (
    <div class="flex justify-center items-center h-screen">
        <NavLink to="/play">
            <button class="w-24 h-24 rounded-full bg-blue-500 focus:outline-none">
                <i class="fa fa-play fa-2x text-white" id="play-btn"></i>
            </button>
            
        </NavLink>
	</div>
    );
    }