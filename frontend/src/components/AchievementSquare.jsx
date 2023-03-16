import  {AchievementModal} from "../components/AchievementModal";
import { AchievementSquareLocked } from "./AchievementSquareLocked";
import { AchievementSquareUnlocked } from "./AchievementSquareUnlocked";
import {useState} from 'react'

export const AchievementSquare = (props) => {

    const [modal, setModal] = useState(false)
    function handleClick() {
        setModal(true)
    }
    const unlocked = props.Unlocked;
    if (unlocked){
        return <AchievementSquareUnlocked
        Title = {props.Title}
        Logo = {props.Logo}
        Descr = {props.Descr}
        
        />;
    }
    return <AchievementSquareLocked 
    unlockPercent={props.unlockPercent}
    Title = {props.Title}/>;
}