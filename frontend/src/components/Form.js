import { useState } from 'react';

const Form = () => {
    // Estados para los inputs
    const [origin, setOrigin] = useState('');
    const [destinations, setDestinations] = useState([]);
    const [destinationInput, setDestinationInput] = useState('');
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
    const [interests, setInterests] = useState([]);
    const [groupMembers, setGroupMembers] = useState([]);
    const [memberInput, setMemberInput] = useState('');

    // Opciones de intereses
    const interestOptions = ['Museos', 'Baile', 'Fútbol', 'Playas', 'Montaña', 'Gastronomía', 'Arte', 'Música'];

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

    // Añadir miembro
    const addMember = (e) => {
        e.preventDefault();
        if (memberInput.trim() && !groupMembers.includes(memberInput)) {
            setGroupMembers([...groupMembers, memberInput]);
            setMemberInput('');
        }
    };

    // Eliminar miembro
    const removeMember = (index) => {
        setGroupMembers(groupMembers.filter((_, i) => i !== index));
    };

    // Manejar envío del formulario
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log({
            origin,
            destinations,
            dates: { from: dateFrom, to: dateTo },
            interests,
            groupMembers
        });
    };

    return (
        <form onSubmit={handleSubmit} className="items-center align-middle mx-72 bg-white rounded-lg text-left">
            <h2 className="text-2xl font-bold mb-6 ">Tell us your preferences</h2>

            {/* Origen */}
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Origen</label>
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
                <label className="block text-gray-700 mb-2">Destinos</label>
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
                        placeholder="Añadir destino"
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
                    <label className="block text-gray-700 mb-2">Desde</label>
                    <input
                        type="date"
                        value={dateFrom}
                        onChange={(e) => setDateFrom(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
                <div>
                    <label className="block text-gray-700 mb-2">Hasta</label>
                    <input
                        type="date"
                        value={dateTo}
                        onChange={(e) => setDateTo(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        required
                    />
                </div>
            </div>

            {/* Intereses */}
            <div className="mb-4">
                <label className="block text-gray-700 mb-2">Intereses</label>
                <div className="grid grid-cols-2 gap-2">
                    {interestOptions.map((interest) => (
                        <label key={interest} className="flex items-center">
                            <input
                                type="checkbox"
                                checked={interests.includes(interest)}
                                onChange={(e) => {
                                    if (e.target.checked) {
                                        setInterests([...interests, interest]);
                                    } else {
                                        setInterests(interests.filter(i => i !== interest));
                                    }
                                }}
                                className="mr-2"
                            />
                            <span>{interest}</span>
                        </label>
                    ))}
                </div>
            </div>

            {/* Miembros del grupo */}
            <div className="mb-6">
                <label className="block text-gray-700 mb-2">Miembros del grupo</label>
                <div className="flex flex-wrap gap-2 mb-2">
                    {groupMembers.map((member, index) => (
                        <div key={index} className="flex items-center bg-blue-100 rounded-full px-3 py-1">
                            <button
                                type="button"
                                onClick={() => removeMember(index)}
                                className="mr-1 text-blue-600 hover:text-blue-800"
                            >
                                ×
                            </button>
                            <span className="text-sm">{member}</span>
                        </div>
                    ))}
                </div>
                <div className="flex">
                    <input
                        type="text"
                        value={memberInput}
                        onChange={(e) => setMemberInput(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Añadir miembro"
                    />
                    <button
                        onClick={addMember}
                        className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600"
                    >
                        +
                    </button>
                </div>
            </div>

            {/* Botón de envío */}
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