import { Outlet, Link, useLocation } from "react-router-dom";

import Header from '../components/Header';
import Footer from "../components/Footer";
import '../assets/styling/global.css';

export default function MainLayout() {
    const location = useLocation();

    return (
        <>
            <Header/>
            <Outlet/>
            <Footer/>
        </>
    );
}
