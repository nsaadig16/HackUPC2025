import { React, use, useEffect, useState } from 'react'
import Button from './Button'
import Form from './Form'


const Container = () => {

    const [idea, setIdea] = useState(null)
    const [group, setGroup] = useState(0)
    // const [isVisible1, setIsVisible1] = useState(true)
    const [isVisible2, setIsVisible2] = useState(false)
    const [formVisible, setFormVisible] = useState(true)
    const [spaceActive, setSpaceActive] = useState(1)
    const [acceptedList, setAcceptedList] = useState([
        { name: "Museos", day: "Lunes", hour: "10:00" },
        { name: "Baile", day: "Martes", hour: "12:00" },
        { name: "Fútbol", day: "Miércoles", hour: "14:00" },
        { name: "Playas", day: "Jueves", hour: "16:00" },
        { name: "Montaña", day: "Viernes", hour: "18:00" },
        { name: "Gastronomía", day: "Sábado", hour: "20:00" },
        { name: "Arte", day: "Domingo", hour: "22:00" },
    ])

    const [imageResults, setImageResults] = useState("")

    useEffect(() => {
        setImageResults("https://images2.alphacoders.com/546/thumb-1920-546391.jpg")
    }, [])

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


                        <div className="container2 text-left h-full flex flex-col bg-white rounded-lg overflow-hidden shadow-lg">
                            {/* Sección superior con imagen de fondo blur (60% de altura) */}
                            <div className='flex flex-row w-full basis-[60%] relative min-h-[300px]'>
                                {/* Imagen de fondo con blur - SOLO en esta sección */}
                                <div className="absolute inset-0 z-0 overflow-hidden">
                                    <img
                                        src={imageResults}
                                        alt="background"
                                        className="w-full h-full object-cover filter blur-md"
                                    />
                                </div>

                                {/* Contenido sobre la imagen de fondo */}
                                <div className="relative z-10 flex flex-row w-full p-8 items-center">
                                    {/* Cuadrado con imagen nítida */}
                                    <div className="bg-white p-2 rounded-lg ml-5 shadow-md mr-6 flex-shrink-0">
                                        <img
                                            src={imageResults}
                                            alt="imagen principal"
                                            className=" w-72 h-72 object-cover rounded-md"
                                        />
                                    </div>

                                    {/* Texto grande al lado derecho */}
                                    <div className="text-white drop-shadow-md">
                                        <h1 className="text-4xl font-bold mb-2">Título Principal</h1>
                                        <p className="text-xl">Descripción o subtítulo aquí</p>
                                    </div>
                                </div>
                            </div>

                            {/* Sección inferior SIN blur (40% de altura) */}
                            <div className="flex flex-col w-full basis-[40%] bg-white p-6">
                                {/* Lista de información */}
                                <div className="w-full mb-6">
                                    <ul className="grid grid-cols-2 gap-4">
                                        <li className="flex items-center">
                                            <span className="font-semibold mr-2">Price:</span>
                                            <span>Valor 1</span>
                                        </li>
                                        <li className="flex items-center">
                                            <span className="font-semibold mr-2">Date:</span>
                                            <span>Valor 2</span>
                                        </li>
                                        <li className="flex items-center">
                                            <span className="font-semibold mr-2">Ubication:</span>
                                            <span>Valor 3</span>
                                        </li>
                                        <li className="flex items-center">
                                            <span className="font-semibold mr-2">Hour:</span>
                                            <span>Valor 4</span>
                                        </li>
                                    </ul>
                                </div>

                                {/* Botones en el centro inferior - Versión con iconos más claros */}
                                <div className="flex justify-center items-center space-x-6 w-full mt-auto">
                                    <button className="bg-green-50 hover:bg-green-100 text-green-600 font-bold py-3 px-8 rounded-full flex items-center transition-colors border border-green-100">
                                        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                        </svg>
                                        Aceptar
                                    </button>

                                    <button className="bg-red-50 hover:bg-red-100 text-red-600 font-bold py-3 px-8 rounded-full flex items-center transition-colors border border-red-100">
                                        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                        Rechazar
                                    </button>
                                </div>
                            </div>
                        </div>




                    </div>

                    <div className="basis-3/12 w-full flex flex-col h-full border-2">
                        <div className="flex flex-col w-full h-12 border-b-2">
                            <h2>Shedule Master </h2>
                        </div>

                        <div className="flex flex-col border-l-2 border-gray-300 h-full w-full">
                            {
                                acceptedList.map((item, index) => (
                                    <div key={index} className="flex flex-row justify-between items-center border-b-2 border-gray-300 p-2 rounded-md">
                                        <p>{item.day}-{item.hour}. {item.name}</p>
                                    </div>
                                ))
                            }
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
