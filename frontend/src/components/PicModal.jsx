import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useRef } from 'react';
import {FretMatrix } from './FretMatrix';
import fretboard from './pics/fretboard-notes.png';

export const PicModal = (props) => {
    const cancelButtonRef = useRef(null)
    function clickHandler(string){
        props.changeString(string)
    }
    return(
        <Transition.Root show={props.open} as={Fragment}>
                <Dialog as="div" className="relative z-10" initialFocus={cancelButtonRef} onClose={props.close}>
                    <Transition.Child
                    as={Fragment}
                    enter="ease-out duration-300"
                    enterFrom="opacity-0"
                    enterTo="opacity-100"
                    leave="ease-in duration-200"
                    leaveFrom="opacity-100"
                    leaveTo="opacity-0"
                    >
                    <div className="fixed inset-0 bg-gray-700 bg-opacity-75 transition-opacity" />
                    </Transition.Child>

                    <div className="fixed inset-0 z-10 overflow-y-auto">
                    <div className="flex min-h-full items-center justify-center p-4 text-center sm:items-center sm:p-0">
                        <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                        enterTo="opacity-100 translate-y-0 sm:scale-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100 translate-y-0 sm:scale-100"
                        leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                        >
                    
                        {/*Dialog Panel*/}
                        <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-slate-700 shadow-2xl transition-all p-8 sm:my-8 sm:w-11/12 sm:max-w-3xl">
                                {/*contents flexbox*/}
                                <>  
                                {/*Title*/}
                                <div className = "text-center text-gray-200 text-2xl text-center font-semibold">
                                        {props.Title}
                                </div>
                                {/*fret matrix */}
                                <div className="relative w-[90%] my-[5%] mx-[5%]">
                                    
                                    <img className="w-full h-auto z-0"
                                        src={fretboard} 
                                        alt="fretboard">
                                    </img>
                                <FretMatrix 
                                    offset = {props.offset}
                                    stringNum = {props.stringNum} />
                                </div>
                                <div className='flex columns-2 items-center justify-center gap-x-4'>     
                                <button onClick={() => clickHandler(0)} class="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                                    E String
                                </button>
                                <button onClick={() => clickHandler(1)} class="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                                    B String
                                </button>
                                <button onClick={() => clickHandler(2)} class="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                                    G String
                                </button>
                                <button onClick={() => clickHandler(3)} class="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                                    D String
                                </button>
                                <button onClick={() => clickHandler(4)} class="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                                    A String
                                </button>
                                <button onClick={() => clickHandler(5)} class="bg-transparent hover:bg-blue-500 text-gray-200 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded">
                                    E String
                                </button>
                                </div>
                                </>
                        </Dialog.Panel>
                        </Transition.Child>
                    </div>
                    </div>
                </Dialog>
            </Transition.Root>
    );
};