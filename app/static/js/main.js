// Get the HTML element that displays the time remaining
var timeRemainingElement = document.getElementById("time-remaining");

// Update the time remaining every second
setInterval(function() {
    // Get the time remaining from the HTML element
    var timeRemaining = parseInt(timeRemainingElement.innerHTML.replace("Time remaining: ", "").replace(" seconds", ""));

    // Subtract 1 second from the time remaining
    timeRemaining -= 1;
    if (timeRemaining < 0) {
        timeRemaining = 0;
    }

    // Update the HTML element with the new time remaining
    timeRemainingElement.innerHTML = "Time remaining: " + timeRemaining + " seconds";
}, 1000);