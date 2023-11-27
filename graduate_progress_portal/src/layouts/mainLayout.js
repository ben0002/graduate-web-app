import { useEffect } from "react";
import { useSelector } from "react-redux";
import { Outlet, useNavigate } from "react-router-dom";

import Header from '../components/Header';
import Footer from "../components/Footer";
import '../assets/styling/global.css';

export default function MainLayout() {
    const user = useSelector(state => state.user)
    const navigate = useNavigate()

    useEffect(_ => {if(user == undefined) navigate('/')}, [user])

    return (
        <>
            <Header/>
            <Outlet/>
            <Footer/>
        </>
    );
}
