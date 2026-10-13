/* Single deployment setting for all frontend-to-backend API requests. */
window.QAICYS_CONFIG = Object.freeze({
    API_BASE_URL: ["localhost", "127.0.0.1"].includes(window.location.hostname)
        ? "http://127.0.0.1:8000"
        : "https://qaicys.todayworld.in"
});
