import {useEffect} from 'react';

export default function Login() {
    
    useEffect(_ => {
        async function getCurrentUser() {
            await fetch("http://localhost:8000/api/login", {mode: 'cors'})
              .then((res) => res.json())
              .catch((err) => {console.log(1); console.log(err)})
              .then(data => {
                if(data.redirect_url) window.location.href = data.redirect_url
                else{
                    console.log(data);
                }
              })
                
          }
        getCurrentUser();      
    }, []);

    return (
        <>
            <h3>login with VT CAS:</h3>
        </>
    );
}