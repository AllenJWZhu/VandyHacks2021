function login() {
 
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    var form = document.getElementById("submit_form");
 
    if (username.value == "") {
 
        alert("Please enter your username");
 
    } else if (password.value  == "") {
 
        alert("Please enter your password");
 
    } else if(username.value == "admin" && password.value == "123456") {

        window.location.href="index.html";
    
    } else {
 
        alert("Please enter the correct username or password!")
 
    }
}

