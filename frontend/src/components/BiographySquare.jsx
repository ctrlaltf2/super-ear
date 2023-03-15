import  {BiographyModal} from "../components/BiographyModal";
import {useState } from 'react'

export const BiographySquare = (props) => {

    const [modal, setModal] = useState(false)
    function handleClick() {
        setModal(true)
    }
    return (
        
        <>
         <BiographyModal
            name = {props.Name}
            pic = {props.Pic}
            bio = {props.Bio}
            college = {props.Creds}
            title = {props.Spec}
            contact = {props.Contact}
            open = {modal}
            close = {setModal}
           />

        <div class= "cursor-pointer shadow-2xl pb-[1%] pt-[1%] rounded-lg bg-slate-600 mx-auto hover:transition-all hover:bg-slate-500 w-full sm:w-4/10 md:w-4/10 lg:w-1/5 xl:w-1/5" onClick = {() => handleClick()}>
            <button type="button" onClick={() => props.onPress}></button>
            <img 
            class="w-1/2 rounded-full mx-auto shadow-2xl drop-shadow-2xl"
            src={props.Pic}
            alt=""
                      />
            <p class = "pt-5 pb-5"> {props.Name}</p>
            <p> {props.Role} </p>
            <p> {props.Creds}</p>
        </div>
        </>
        );
}