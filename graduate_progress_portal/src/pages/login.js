import {useEffect} from 'react';

export default function Login() {
    
    useEffect(_ => {
        async function getCurrentUser() {
            await fetch("https://bktp-gradpro.discovery.cs.vt.edu/api/login")
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