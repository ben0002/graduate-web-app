import { Outlet, Link } from "react-router-dom";

import Header from '../components/Header';
import Footer from "../components/Footer";
import '../assets/styling/global.css';


export default function MainLayout() {
    return (
        <>
            <Header/>
            <h1>Main Layout:</h1>
            <Link to="/student/progress">
                <button>Go to Student Progress</button>
            </Link>
            <Outlet/>
            <Footer/>
        </>
    );
}
