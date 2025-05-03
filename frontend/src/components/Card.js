import React from 'react'
import userimg from '../assets/images/usuario.png'

const Card = ({ Nom, Destins, Interessos }) => {
    return (
        <div className="bg-gray-200 rounded-md shadow-md p-4 m-2">
            <div className="flex flex-row gap-4">

                <img alt='userImg' src={userimg} className='w-8'></img>
                <h3 className="text-lx font-semibold">{Nom}</h3>
            </div>
            <p className="text-sm text-gray-600">Destins: {Destins}</p>
            <p className="text-sm text-gray-600">Interessos: {Interessos}</p>
        </div>
    )
}

export default Card