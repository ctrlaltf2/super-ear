import { Dialog, Transition } from '@headlessui/react'
import { Fragment, useRef } from 'react'

export const AchievementModal = (props) => {
    const cancelButtonRef = useRef(null)
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
                        <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-slate-500 shadow-2xl transition-all p-8 sm:my-8 sm:w-11/12 sm:max-w-3xl">
                                {/*contents flexbox*/}
                                <div className="flex items-center space-x-10 w-full h-full">
                                    
                                    {/*bio picture*/}   
                                    <div className="align-center w-full">                         
                                        <img className="w-full aspect-square rounded-full mx-auto shadow-2xl drop-shadow-2xl" 
                                                src={props.pic} />
                                    </div>  
                                    {/*bio text*/}
                                    <div className="text-center bg-slate-600 shadow-2xl drop-shadow-2xl rounded-xl p-3">
                                        {/*Name */}
                                        <Dialog.Title as="h3" className="text-4xl font-medium leading-0 text-gray-200 ">
                                            {props.name}
                                        </Dialog.Title> 
                                        <div className="flex flex-no-wrap p-1 pt-4 justify-center text-sm font-normal text-gray-200 space-x-11">
                                                <p>{props.college} </p>
                                                <p>{props.title}</p>
                                                <p>{props.contact}</p> 
                                        </div>
                                        {/*body formatting */}
                                        <div className="mt-2">
                                            <p className="text-sm font-light text-gray-200 w-full">
                                                {props.bio}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                        </Dialog.Panel>
                        </Transition.Child>
                    </div>
                    </div>
                </Dialog>
            </Transition.Root>
    );
};