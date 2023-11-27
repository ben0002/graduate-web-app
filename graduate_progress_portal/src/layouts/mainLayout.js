import { Outlet, Link } from "react-router-dom";
import Header from '../shared/components/Header';
import Footer from "../shared/components/Footer";

export default function MainLayout() {
    return (
        <>
            <Header/>
            <Outlet/>
            <Footer/>
        </>
    );
}
