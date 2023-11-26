import {useEffect} from 'react';

export default function Login() {
    
    useEffect(_ => {
        async function getCurrentUser() {
            await fetch("https://bktp-gradpro-api.discovery.cs.vt.edu/api/login", {
                credentials: 'include', // To include cookies in the request
                headers: {
                    'Accept': 'application/json', // Explicitly tell the server that you want JSON
                }
            })
              .then((res) => res.json())
              .then(data => {
                if(data.redirect_url) window.location.href = data.redirect_url
                else{
                    console.log(data);
                }
              })
              .catch((err) => {console.log(1); console.log(err)})
                
          }
        getCurrentUser();      
    }, []);

    return (
        <>
            <h3>login with VT CAS:</h3>
        </>
    );
}