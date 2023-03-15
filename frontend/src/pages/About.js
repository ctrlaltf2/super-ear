import React from "react";
import { BiographySquare } from "../components/BiographySquare";
import basePic from "../components/pics/blank-profile-picture-.png";

function About(){
    return(
        <div>

            <div class = "min-h-screen bg-gray-700 text-center text-white text-4xl pb-2">
                <h1 class = "pt-[1%]">
                    About
                </h1>
                <p class = "text-base pt-[3%]"> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. </p>
                
                <h1 class = "pt-[5%] pb-[4%]">
                    Meet The Team
                </h1>
                <div class = "flex flex-wrap">
                    <BiographySquare 
                        Name = "Elizabeth Gilman" 
                        Pic = {basePic}
                        Role = "Hardware" 
                        Spec = "Hardware"
                        Creds = "Pitt 2023"
                        Bio = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                        Contact = "wno1@pitt.edu"
                />
                    <BiographySquare 
                        Name = "Shaoyu Pei" 
                        Pic = {basePic}
                        Role = "Hardware" 
                        Spec = "Hardware"
                        Creds = "Pitt 2023"
                        Bio = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                        Contact = "wno1@pitt.edu"
                    />
                    <BiographySquare 
                        Name = "Caleb Troyer" 
                        Pic = {basePic}
                        Role = "Software" 
                        Spec = "Backend Engineer"
                        Creds = "Pitt 2023"
                        Bio = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                        Contact = "wno1@pitt.edu"
                    />
                    <BiographySquare 
                        Name = "Rocky Oberti" 
                        Pic = {basePic}
                        Role = "Software" 
                        Spec = "Frontend Engineer"
                        Creds = "Pitt 2023"
                        Bio = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
                        Contact = "wno1@pitt.edu"
                    />
                </div>
            </div>



        
        
        

        </div>
    );
};

export default About;

