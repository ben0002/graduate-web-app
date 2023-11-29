import { useEffect } from "react";
import { useSelector } from "react-redux";
import { Outlet, useNavigate } from "react-router-dom";

import Header from '../components/Header';
import Footer from "../components/Footer";
import '../assets/styling/global.css';

export default function MainLayout() {
    const state = useSelector(state => state)
    const navigate = useNavigate()

    useEffect(_ => {if(state.user == undefined || state.student == undefined) navigate('/')}, [state])

    return (
        <>
            <Header/>
            <Outlet/>
            <Footer/>
        </>
    );
}
