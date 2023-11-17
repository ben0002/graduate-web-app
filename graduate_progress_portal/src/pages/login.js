import { Link } from "react-router-dom";


export default function Login() {
    return (
        <>
            <h3>login with VT CAS:</h3>
            <Link to="/student/progress">
                <button>Go to Student Progress</button>
            </Link>
        </>
    );
}