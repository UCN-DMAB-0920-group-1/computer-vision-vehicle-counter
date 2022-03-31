export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function isLoggedIn() {
    return getCookie("loggedIn") === "true" ? true : false;
}

export function logout() {
    console.log("please change this cookie")
    document.cookie = "jwt=;"
    document.cookie = "loggedIn=; expires=Thu, 01 Jan 1970 00: 00: 00 UTC; path = /;"
}