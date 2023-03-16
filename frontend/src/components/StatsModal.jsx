import { Dialog, Transition } from '@headlessui/react'
import { Fragment, useRef } from 'react'

export const StatsModal = (props) => {
    const cancelButtonRef = useRef(null)
    //const numCols = props.numCols
    const titleList = props.ColTitles
    const statsList = props.statsList

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
                                    {/*Title*/}
                                    <div className = "text-center text-gray-200 text-2xl text-center font-semibold">
                                        {props.Title}
                                    </div>
                                    {/* Stat Table*/}
                                    <div class = {`grid grid-cols-3 text-center text-gray-200 text-md font-medium mt-5 bg-slate-500 px-2 py-4 rounded-2xl shadow-2xl`}>
                                    {
                                        titleList.map((elem) => {
                                            return <h1>{elem}</h1>
                                        }
                                        )
                                    }
                                                    {
                                        statsList.map((elem, index) => {
                                            return <p class = "text-sm font-light my-[2%]" key={index}>{elem}</p>
                                        }
                                        )
                                    }
                                    </div>
                        </Dialog.Panel>
                        </Transition.Child>
                    </div>
                    </div>
                </Dialog>
            </Transition.Root>
    );
};
