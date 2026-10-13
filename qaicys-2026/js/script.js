// =============================================
// QAICYS 2026 COUNTDOWN
// =============================================

const eventDate = new Date("August 13, 2026 09:00:00").getTime();


function updateCountdown() {

    const now = new Date().getTime();

    const distance = eventDate - now;


    // Event already started

    if (distance <= 0) {

        document.querySelector(".countdown").innerHTML =
            "<span class='event-live'>QAICYS 2026 IS LIVE</span>";

        return;
    }


    // Calculate time

    const days = Math.floor(
        distance / (1000 * 60 * 60 * 24)
    );

    const hours = Math.floor(
        (distance % (1000 * 60 * 60 * 24)) /
        (1000 * 60 * 60)
    );

    const minutes = Math.floor(
        (distance % (1000 * 60 * 60)) /
        (1000 * 60)
    );

    const seconds = Math.floor(
        (distance % (1000 * 60)) /
        1000
    );


    // Display

    document.getElementById("days").textContent =
        String(days).padStart(2, "0");

    document.getElementById("hours").textContent =
        String(hours).padStart(2, "0");

    document.getElementById("minutes").textContent =
        String(minutes).padStart(2, "0");

    document.getElementById("seconds").textContent =
        String(seconds).padStart(2, "0");
}


// Run immediately
updateCountdown();


// Update every second
setInterval(updateCountdown, 1000);