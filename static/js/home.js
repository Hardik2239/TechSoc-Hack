function clickCreate(){
    redirectTo("/create")
}

function clickBrowse(){
    redirectTo("/browse")
}

function redirectTo(fileName) {
    window.location.href=fileName;
}