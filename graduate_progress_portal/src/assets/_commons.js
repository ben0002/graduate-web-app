
export function apiRequest(endpoint, method, body){
    return fetch(`//bktp-gradpro-api2.discovery.cs.vt.edu/${endpoint}`, {
        method: method,
        credentials: 'include', // To include cookies in the request
        headers: {
            'Accept': 'application/json', // Explicitly tell the server that you want JSON
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
    })
}

export function apiGetRequest(endpoint){
    return fetch(`//bktp-gradpro-api2.discovery.cs.vt.edu/${endpoint}`, {
        credentials: 'include', // To include cookies in the request
        headers: {
            'Accept': 'application/json', // Explicitly tell the server that you want JSON
            'Content-Type': 'application/json',
        }
    })
}

export function isNumeric(str) {
    if (typeof str != "string") return false // we only process strings!  
    return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
           !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
  }

  export const terms = ["Spring", "Summer", "Fall", "Winter"]