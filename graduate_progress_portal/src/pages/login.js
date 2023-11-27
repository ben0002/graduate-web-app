import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    useEffect(_ => {
        async function login() {
            await fetch("https://bktp-gradpro-api.discovery.cs.vt.edu/api/login", {
                credentials: 'include', // To include cookies in the request
                headers: {
                    'Accept': 'application/json', // Explicitly tell the server that you want JSON
                }
            })
            .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
            })
            .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else if(data.redirect_url) window.location.href = data.redirect_url;
                else{
                    console.log(data)
                    dispatch({type: 'populate_user', payload: data});
                    navigate('/student/progress')
                }
            })
            .catch((err) => console.error('Error:', err.message))    
        }
        login();      
    }, []);

    return (
        <>
            <h3>login with VT CAS:</h3>
        </>
    );
}