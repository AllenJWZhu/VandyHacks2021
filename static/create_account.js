function validate_account() {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var address = document.getElementById("email");
    var uname = document.getElementById("username");
    var pword = document.getElementById("password");
    var confirm_pword = document.getElementById("confirm_password");
    var form = document.getElementById("submit_form");
    console.log("Hello")

    if (address.value == "")
    { 
        alert('Email cannot be empty!');
    }
    else if (uname.value == "")
    {
        alert('Username cannot be empty!');
    }
    else if (pword.value == "")
    {
        alert('Please enter your password');
    }
    else if (confirm_pword.value == "") 
    {
        alert('Please enter your password again');
    }
    else if(email.value == "admin@gmail.com" && username.value == "admin" && password.value == "123456" && confirm_pword.value == "123456")
    {
        window.location.href="index";
    } 
    else 
    {
        alert("Please enter the correct username or password!")
    }
}
