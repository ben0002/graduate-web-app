import { Outlet } from "react-router-dom";


export default function StudentLayout() {
    return (
        <>
            <h2>Student Layout:</h2>
            <Outlet/>
        </>
    );
}