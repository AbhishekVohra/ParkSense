// script.js

let imageUpdateInterval;

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    }).then(response => response.json()).then(data => {
        if (data.status === "success") {
            document.getElementById("loginForm").style.display = "none";
            document.getElementById("dashboard").style.display = "block";

            // Start updating the parking status image every 1.5 seconds
            imageUpdateInterval = setInterval(updateParkingStatusImage, 1500);
            // Start updating the nearest parking spot info
            setInterval(updateNearestParkingSpot, 1500);
        } else {
            alert("Invalid login");
        }
    });
}

function refreshParkingStatus() {
    updateParkingStatusImage(); // Call the function that updates the parking image
}

function updateParkingStatusImage() {
    const parkingImage = document.getElementById("parkingImage");
    
    // Set the placeholder image before fetching the new one
    parkingImage.src = "loading.jpg";

    const timestamp = new Date().getTime();
    const newImageSrc = "http://127.0.0.1:5000/get_latest_parking_image?timestamp=" + timestamp;

    fetch(newImageSrc)
        .then(response => response.blob())
        .then(blob => {
            // Create a local URL for the blob and set it as the new source
            const url = URL.createObjectURL(blob);
            parkingImage.src = url;
        })
        .catch(() => {
            // In case of an error, you can set an error image or handle it as needed
            parkingImage.src = "loading.jpg"; // Replace with an actual error image path if needed
        });
}

function updateNearestParkingSpot() {
    fetch('http://127.0.0.1:5000/get_nearest_spot')
        .then(response => response.json())
        .then(data => {
            document.getElementById("nearestSpot").innerText = "Nearest Spot: " + data.nearest_spot;
        });
}

function bookSlot() {
    const slotNumber = document.getElementById("parkingSlot").value;
    const username = document.getElementById("username").value;

    // Check if the slot number is valid (within the range 1-69)
    if (isNaN(slotNumber) || slotNumber < 1 || slotNumber > 69) {
        alert("Invalid slot number. Please enter a number between 1 and 69.");
        return;
    }

    // Proceed with the booking
    fetch('http://127.0.0.1:5000/book_slot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ slot: "slot" + slotNumber, username }) // Prefixing with "slot"
    }).then(response => response.json()).then(data => {
        if (data.status === "success") {
            // Redirect to the booking confirmation page with details
            const currentTime = new Date().toLocaleString();
            window.location.href = `booking_confirmation.html?slot=${slotNumber}&user=${username}&time=${encodeURIComponent(currentTime)}`;
        } else if (data.status === "already booked") {
            alert("Slot already booked");
        } else {
            alert("Error: Unable to book the slot.");
        }
    });
}

// Add any additional JavaScript functions or event handlers here if needed
