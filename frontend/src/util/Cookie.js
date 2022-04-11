import jwt_decode from "jwt-decode";


export function getCookie(name) {
    const value = `; ${document.cookie}`;
    if (!value) return "";
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function isLoggedIn() {
    return getCookie("loggedIn") === "true" ? true : false;
}

export function logoutCookie() {
    document.cookie = "jwt=;"
    document.cookie = "loggedIn=; expires=Thu, 01 Jan 1970 00: 00: 00 UTC; path = /;"
}

export function getPayloadValue(key) {
    let token = getCookie("jwt");
    if (token.length > 0) {
        let json = jwt_decode(getCookie("jwt"));
        return json[key];
    } else return "no token found";
}