import { Outlet } from "react-router-dom";
import '../assets/styling/students.css';

export default function StudentLayout() {
    return (
        <div className="student-page-background">
        <Outlet/>
        </div>
    );
}