import {NavLink} from "react-router-dom"


export const NavBarOption = (props) => {
    return (
        <NavLink 
            to={props.link} 
            className={({isActive}) => isActive ? 'bg-gray-900 text-white block px-3 py-2 rounded-md text-base font-medium': 'text-gray-300 hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium'
            }
            > {props.text} 
        </NavLink>
    );
}