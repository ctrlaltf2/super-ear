import  {AchievementModal} from "../components/AchievementModal";
import {useState} from 'react'
import classNames from 'classnames';

export const AchievementSquareUnlocked = (props) => {

    const [modal, setModal] = useState(false)
    function handleClick() {
        setModal(true)
    }
    return (
        <>
         <AchievementModal
            name = {props.Name}
            pic = {props.Pic}
            bio = {props.Bio}
            college = {props.Creds}
            title = {props.Spec}
            contact = {props.Contact}
            open = {modal}
            close = {setModal}
           />

        <div className = "cursor-pointer drop-shadow-xl pb-[1%] pt-[1%] rounded-lg bg-slate-800 mx-auto hover:transition-all hover:bg-slate-700 transition ease-in-out delay-150 hover:shadow-lg hover:shadow-yellow-600 w-[85%] mb-4"
                        onClick = {() => handleClick()}
        
        >
            <button type="button" onClick={() => props.onPress}></button>
            <div className = "text-gray-200 text-2xl text-center font-semibold">
                {props.Title}
            </div>
            <img className = "w-full pt-[7%]"
                src = {props.Logo}
                alt = "achievement logo" />
            <div className = 'text-gray-200 text-xl text-center font-normal pt-[15%]'>
                {props.Descr}
            </div>
        </div>
        </>
        );
}