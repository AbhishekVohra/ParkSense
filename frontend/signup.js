document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = {
        fullname: document.getElementById('fullname').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value
    };

    // Send the email
    Email.send({
        Host: "smtp25.elasticemail.com",
        Username: "parksense.info@gmail.com",
        Password: "31BBE03802991686BDC83871E0961BB46D00",
        To: 'vverma_be20@thapar.edu',
        From: "parksense.info@gmail.com",
        Subject: "New Signup",
        Body: `Full Name: ${formData.fullname}<br>
               Phone: ${formData.phone}<br>
               Email: ${formData.email}<br>
               Age: ${formData.age}<br>
               Gender: ${formData.gender}`
    }).then(
        message => alert(message),
        console.log("message sent"),
        // console.log(Body)
    );
});
