import { React, use, useEffect, useState } from 'react'
import Button from './Button'
import Form from './Form'

const Container = () => {

    const [idea, setIdea] = useState(null)
    const [group, setGroup] = useState(0)
    // const [isVisible1, setIsVisible1] = useState(true)
    const [isVisible2, setIsVisible2] = useState(true)
    const [formVisible, setFormVisible] = useState(true)

    useEffect(() => {
        if (group === 0) return
        // setIsVisible2(false)
        setFormVisible(true)
    }, [group])

    return (
        <div className="h-full mt-28">
            {/* <div className={`transition-opacity duration-500 ${isVisible1 ? "opacity-100" : "opacity-0 hidden"}`}>
                <div className="flex flex-col justify-center items-center align-middle font-bold">
                    <h1 className="text-4xl">Plan your trip</h1>
                    <p className="text-3xl">Do you have any idea of the travel plan?</p>
                    <div className="flex flex-row justify-between">
                        <Button text="Yes, i actually have an idea" onClick={() => { setIsVisible1(false); setIsVisible2(true); setIdea(true) }} />
                        <Button text="No, i need help with the plan" onClick={() => { setIsVisible1(false); setIsVisible2(true); setIdea(false) }} />
                    </div>
                </div>
            </div> */}

            <div className={`transition-opacity duration-500 ${isVisible2 ? "opacity-100" : "opacity-0 hidden"}`}>
                <div className="flex flex-col justify-center items-center align-middle font-bold">
                    <div className="flex-basis-4/5">

                    </div>

                    <div className="flex-basis-1/5">

                    </div>

                </div>
            </div>

            <div className={`transition-opacity duration-500 ${formVisible ? "opacity-100" : "opacity-0"}`}>
                <Form Type={group} />
            </div>

        </div>
    )
}

export default Container
