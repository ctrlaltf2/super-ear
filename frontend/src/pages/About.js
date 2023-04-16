import React from "react";
import { BiographySquare } from "../components/BiographySquare";
import basePic from "../components/pics/blank-profile-picture-.png";
import Oberti from "../components/pics/Oberti.png";

function About(){
    return(
        <div>

            <div class = "min-h-screen bg-gray-700 text-center text-white text-4xl pb-2">
                <h1 class = "pt-[1%]">
                    About
                </h1>
                <div className="flex flex-wrap bg-slate-800 py-[3%] px-[2%] w-[95%] ml-[2%] mt-[2%] opacity-90 rounded-xl shadow-md"> 
                <p class = "text-base"> The Super Ear is an interactive musical device that helps musicians become more in tune with the guitar. This project utilizes a small handheld tool that can help people develop ‘absolute pitch’ or more commonly known as perfect pitch. This is when a person can identify a note simply by listening to it. Being able to identify the location of different frequencies on the guitar’s fretboard is also very powerful, because a player can listen to songs and learn how to play them very quickly. This has become a lost skill for many due to the easily accessible resources on the internet that do not require a player to use any listening skills. Super Ear is trying to change that.
 </p>                 
                </div> 
                <h1 class = "pt-[3%] pb-[4%]">
                    Meet The Team
                </h1>
                <div class = "flex flex-wrap bg-slate-800 py-[3%] px-[2%] w-[95%] ml-[2%] opacity-90 rounded-xl shadow-md">
                    <BiographySquare 
                        Name = "Elizabeth Gilman" 
                        Pic = {basePic}
                        Role = "Hardware" 
                        Spec = "Hardware Engineer"
                        Creds = "Pitt 2023"
                        Bio = "Hardware Engineer. Developed the analog filter board. This six-order low pass filter was designed to remove the effects of harmonics and provide anti-aliasing for signal processing."
                        Contact = "EAG81@pitt.edu"
                />
                    <BiographySquare 
                        Name = "Shaoyu Pei" 
                        Pic = {basePic}
                        Role = "Hardware" 
                        Spec = "Hardware Engineer"
                        Creds = "Pitt 2023"
                        Bio = "Hardware Engineer. Developed the DSP module. This module samples the analog signal into digital data points which are then processed with FFT to detect the fundamental frequency of that signal."
                        Contact = "Shaoyu.Pei@pitt.edu"
                    />
                    <BiographySquare 
                        Name = "Caleb Troyer" 
                        Pic = {basePic}
                        Role = "Software" 
                        Spec = "Backend Engineer"
                        Creds = "Pitt 2023"
                        Bio = "Back End Engineer. Developed spaced repetition-based training algorithm to optimize learning. Created backend server as well as game logic and scheduling. Connects with DSP module as well as front end module. "
                        Contact = "caleb.troyer@pitt.edu"
                    />
                    <BiographySquare 
                        Name = "Rocky Oberti" 
                        Pic = {Oberti}
                        Role = "Software" 
                        Spec = "Frontend Engineer"
                        Creds = "Pitt 2023"
                        Bio = "Front End Engineer. Developed the UI of the system as well as the gamification system. Analyzed data to provide the user with useful stats and visualizations such as areas of improvement or their long term progress."
                        Contact = "WNO1@pitt.edu"
                    />
                </div>
            </div>



        
        
        

        </div>
    );
};

export default About;

