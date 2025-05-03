import React from 'react'

const Button = ({ text, onClick }) => {
    return (
        <div>
            <button onClick={onClick} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full m-2 hover:bg-blue-400 transition duration-300 ease-in-out transform">
                {text}
            </button>
        </div>
    )
}

export default Button
