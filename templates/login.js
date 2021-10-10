function login() {
 
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    var isRmbPwd = document.getElementById("isRmbPwd").checked;
 
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

