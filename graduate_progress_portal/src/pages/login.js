import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

function getStuInfo(){
    return fetch("https://bktp-gradpro-api2.discovery.cs.vt.edu/students/login_info", {
        credentials: 'include', // To include cookies in the request
        headers: {
            'Accept': 'application/json', // Explicitly tell the server that you want JSON
        }
    })
}

export default function Login() {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    useEffect(_ => {
        function login() {
            fetch("https://bktp-gradpro-api.discovery.cs.vt.edu/login", {
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
                    getStuInfo()
                    .then(res => {
                        if(res.ok) return res.json();
                        else console.log(res.status);
                    })
                    .then(data => {
                        if (data == undefined) console.error('Error: Non ok http response');
                        else if(data.redirect_url) window.location.href = data.redirect_url;
                        else{
                            console.log(data)
                            dispatch({type: 'pop_user', payload: {data: data, type: 'student'}});
                            navigate('/student/progress')
                        }
                    })
                    .catch((err) => console.error('Error:', err.message))
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