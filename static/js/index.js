function main(){
    btnLogin = document.getElementById("btnLogin");
    btnLogin.addEventListener('click', login);
}

function login(){
    redirectTo("/authentication/login")
}

function redirectTo(fileName) {
    window.location.href=fileName;
}

main()