import { React, use, useEffect, useState } from 'react'
import Button from './Button'
import Form from './Form'

const Container = () => {

    const [idea, setIdea] = useState(null)
    const [group, setGroup] = useState(0)
    // const [isVisible1, setIsVisible1] = useState(true)
    const [isVisible2, setIsVisible2] = useState(true)
    const [formVisible, setFormVisible] = useState(false)
    const [spaceActive, setSpaceActive] = useState(1)

    useEffect(() => {
        if (group === 0) return
        // setIsVisible2(false)
        setFormVisible(true)
    }, [group])

    return (
        <div className="h-full">

            <div className={`transition-opacity duration-500 h-full ${isVisible2 ? "opacity-100" : "opacity-0 hidden"}`}>
                <div className="flex flex-row justify-center items-center h-full">
                    <div className="basis-9/12 w-full h-full">
                        <div className="flex flex-row w-full">
                            <div className="w-28 h-12">
                                <button onClick={() => { setSpaceActive(1); }}
                                    className={`ml-5 h-full w-24 text-xl ${spaceActive === 1 ? "text-blue-700 border-b-2 border-blue-700" : "text-black border-none hover:text-gray-700 hover:border-b-2 hover:border-gray-700"}`}
                                >
                                    Resultats
                                </button>
                            </div>

                            <div className="w-28 h-12">
                                <button onClick={() => { setSpaceActive(2); }}
                                    className={`h-full text-xl w-24 ${spaceActive === 1 ? "text-black border-none" : "text-blue-700"} border-blue-700 border-b-2 hover:text-gray-700 hover:border-b-2 hover:border-gray-700`}
                                >
                                    Grup
                                </button>
                            </div>
                        </div>
                        <div className="container2 text-left h-full bg-green-300">
                            <p>

                            </p>
                        </div>
                    </div>

                    <div className="basis-3/12 w-full flex flex-col h-full border-2">
                        <div className="flex flex-col w-full h-12">
                            <h2>Shedule Master </h2>
                        </div>

                        <div className="flex flex-col border-l-2 border-gray-300 h-full bg-red-300 w-full">

                        </div>
                    </div>

                </div>
            </div>

            <div className={`transition-opacity duration-500 ${formVisible ? "opacity-100" : "opacity-0 hidden"}`}>
                <Form Type={group} />
            </div>

        </div >
    )
}

export default Container
