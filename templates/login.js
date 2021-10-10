function login() {
 
    var username = document.getElementById("username");
    var password = document.getElementById("password");
    var isRmbPwd = document.getElementById("isRmbPwd").checked;
 
    if (username.value == "") {
 
        alert("Please enter your username");
 
    } else if (password.value  == "") {
 
        alert("Please enter your password");
 
    } else if(username.value == "admin" && password.value == "123456") {
        if (isRmbPwd == true) {   
            setCookie ("This is username", username.value.trim(), 7);
            setCookie (username.value.trim(), password.value.trim(), 7);
        }
        else {
            delCookie ("This is username");
            delCookie (username.value.trim());
        } 
        window.location.href="../main.html";
    
    } else {
 
        alert("Please enter the correct username or password!")
 
    }
}

