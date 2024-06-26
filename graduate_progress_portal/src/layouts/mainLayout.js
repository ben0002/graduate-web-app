import { Outlet, Link } from "react-router-dom";
import Header from '../shared/components/Header';
import Footer from "../shared/components/Footer";

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
