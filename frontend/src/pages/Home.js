import React from 'react'
import Container from '../components/Container'
import Header from '../components/Header'
import Footer from '../components/Footer'

const Home = () => {
    return (
        <div className=' w-full h-screen max-h-screen overflow-y-auto'>
            <Header />
            <Container />
            <Footer />
        </div>
    )
}

export default Home
