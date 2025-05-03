import React from 'react'
import logo from '../assets/svg/logoWhite.svg'
import world from '../assets/svg/world.svg'
import favourite from '../assets/svg/favourite.svg'
import profile from '../assets/svg/profile.svg'
import menubars from '../assets/svg/menubars.svg'
const Header = () => {


    const openPopup = () => {

    }

    return (
        <div>
            <div className="flex justify-between items-center bg-gray-800 p-4 px-7 text-white h-36">
                <div className='flex flex-row justify-between items-center w-full px-72'>


                    <div className="text-2xl font-bold">
                        <img src={logo} alt="Logo" className="w-36 inline-block mr-2 " />
                    </div>
                    <div className="flex space-x-4">
                        <span onClick={openPopup} className="hover:text-gray-400">
                            <img src={world} alt="Logo" className="w-5 inline-block mr-2 " />
                        </span>
                        <a href="https://www.skyscanner.es/profile/saved" className="hover:text-gray-400">
                            <img src={favourite} alt="Logo" className="w-5 inline-block mr-2 " />
                        </a>
                        <a href="https://www.skyscanner.es/profile" className="hover:text-gray-400">
                            <img src={profile} alt="Logo" className="w-5 inline-block mr-2 " />
                        </a>
                        <a href="https://www.skyscanner.es/profile" className="hover:text-gray-400">
                            <img src={menubars} alt="Logo" className="w-5 inline-block mr-2 " />
                        </a>
                    </div>

                </div>

            </div>
        </div>
    )
}

export default Header
