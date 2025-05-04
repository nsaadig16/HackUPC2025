import { useState } from 'react';
import { travel } from '../services/services';

const Form = ({ onCompleteAction }) => {
    // Estados para los inputs
    const [origin, setOrigin] = useState('');
    const [username, setUsername] = useState('');
    const [destinations, setDestinations] = useState([]);
    const [destinationInput, setDestinationInput] = useState('');
    const [interestsInput, setInterestsInput] = useState('');
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
    const [interests, setInterests] = useState([]);
    const [rentHotel, setRentHotel] = useState(false);
    const [rentCar, setRentCar] = useState(false);
    const [pressupost, setPressupost] = useState('');


    // Añadir destino
    const addDestination = (e) => {
        e.preventDefault();
        if (destinationInput.trim() && !destinations.includes(destinationInput)) {
            setDestinations([...destinations, destinationInput]);
            setDestinationInput('');
        }
    };

    // Eliminar destino
    const removeDestination = (index) => {
        setDestinations(destinations.filter((_, i) => i !== index));
    };

    // Añadir interes
    const addInterests = (e) => {
        e.preventDefault();
        if (interestsInput.trim() && !interests.includes(interestsInput)) {
            setInterests([...interests, interestsInput]);
            setInterestsInput('');
        }
    };

    // Eliminar interés
    const removeInterests = (index) => {
        setInterests(interests.filter((_, i) => i !== index));
    };

    // Manejar envío del formulario
    const handleSubmit = (e) => {
        e.preventDefault();

        const [anio1, mes1, dia1] = dateFrom.split("-");
        const from = `${dia1}-${mes1}-${anio1}`;

        const [anio, mes, dia] = dateTo.split("-");
        const to = `${dia}-${mes}-${anio}`;

        console.log(from, to);
        var struct = {
            username,
            origin,
            destinations,
            disponibility: [from, to],
            max_price: pressupost,
            interests,
            hotel: rentHotel,
            hire_car: rentCar,
            lenguage: '',

        }
        travel(struct)
            .then((res) => {
                console.log('Data fetched:', res);
                // Aquí puedes hacer algo con los datos obtenidos
                // Por ejemplo, puedes guardar los datos en el estado o en un contexto global
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
                // Manejar el error aquí
            });
        // Reiniciar el formulario

        onCompleteAction({ resull: 'success' });
    };

    return (
        <form onSubmit={handleSubmit} className="items-center align-middle scroll-y-auto mx-72 bg-white rounded-lg text-left">
            <h2 className="text-2xl font-bold mb-6 mt-7">Tell us your preferences</h2>

            {/* Origen */}
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Username</label>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
            </div>

            {/* Origen */}
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Origin</label>
                <input
                    type="text"
                    value={origin}
                    onChange={(e) => setOrigin(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
            </div>

            {/* Destinos */}
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Destination</label>
                <div className="flex flex-wrap gap-2 mb-2">
                    {destinations.map((dest, index) => (
                        <div key={index} className="flex items-center bg-blue-100 rounded-full px-3 py-1">
                            <button
                                type="button"
                                onClick={() => removeDestination(index)}
                                className="mr-1 text-blue-600 hover:text-blue-800"
                            >
                                ×
                            </button>
                            <span className="text-sm">{dest}</span>
                        </div>
                    ))}
                </div>
                <div className="flex">
                    <input
                        type="text"
                        value={destinationInput}
                        onChange={(e) => setDestinationInput(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Add destinations"
                    />
                    <button
                        onClick={addDestination}
                        className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600"
                    >
                        +
                    </button>
                </div>
            </div>

            {/* Fechas */}
            <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                    <label className="block text-gray-700 mb-2">From</label>
                    <input
                        type="date"
                        value={dateFrom}
                        onChange={(e) => setDateFrom(String(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
                <div>
                    <label className="block text-gray-700 mb-2">To</label>
                    <input
                        type="date"
                        value={dateTo}
                        onChange={(e) => setDateTo(String(e.target.value))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
            </div>
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Pressupost</label>
                <input
                    type="text"
                    value={pressupost}
                    onChange={(e) => setPressupost(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                />
            </div>
            {/* Intereses */}
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Interests</label>
                <div className="flex flex-wrap gap-2 mb-2">
                    {interests.map((inter, index) => (
                        <div key={index} className="flex items-center bg-blue-100 rounded-full px-3 py-1">
                            <button
                                type="button"
                                onClick={() => removeInterests(index)}
                                className="mr-1 text-blue-600 hover:text-blue-800"
                            >
                                ×
                            </button>
                            <span className="text-sm">{inter}</span>
                        </div>
                    ))}
                </div>
                <div className="flex">
                    <input
                        type="text"
                        value={interestsInput}
                        onChange={(e) => setInterestsInput(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Add interest"
                    />
                    <button
                        onClick={addInterests}
                        className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600"
                    >
                        +
                    </button>
                </div>

                <div className="space-y-2 mt-3">
                    <label className="flex items-center gap-2">
                        <input type="checkbox"
                            onChange={(e) => setRentHotel(e.target.checked)}
                            className="h-4 w-4"
                        />
                        Book a hotel room
                    </label>
                    <label className="flex items-center gap-2">
                        <input type="checkbox"
                            onChange={(e) => setRentCar(e.target.checked)}
                            className="h-4 w-4" />
                        Rent a car
                    </label>
                </div>
            </div>



            <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
                Planificar Viaje
            </button>
        </form>
    );
};

export default Form;