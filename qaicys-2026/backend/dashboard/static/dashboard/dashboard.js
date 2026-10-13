(function () {
    "use strict";

    const eventList = document.getElementById("eventList");
    const selectedEvent = document.getElementById("selectedEvent");
    const countElement = document.getElementById("registrationCount");
    const searchInput = document.getElementById("dashboardSearch");
    const exportButton = document.getElementById("exportRegistrations");
    const tableContainer = document.getElementById("registrationTable");
    const message = document.getElementById("dashboardMessage");
    let selectedSlug = "";
    let searchTimer;

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>'"]/g, char => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
        })[char]);
    }

    function label(field, customLabels = {}) {
        if (customLabels[field]) return customLabels[field];
        if (field === "created_at") return "Registered At";
        return field.replaceAll("_", " ").replace(/\b\w/g, char => char.toUpperCase());
    }

    function displayValue(field, value) {
        if (field === "created_at" && value) return new Date(value).toLocaleString();
        if (typeof value === "boolean") return value ? "Yes" : "No";
        return value || "—";
    }

    function csrfToken() {
        return document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1] || "";
    }

    async function request(url, options = {}) {
        const response = await fetch(url, {credentials: "same-origin", ...options});
        if (response.status === 401 || response.status === 403) {
            window.location.href = "/manager/login/";
            throw new Error("Your manager session has expired.");
        }
        const data = await response.json();
        if (!response.ok) throw new Error(data.errors?.non_field_errors?.[0] || "Unable to complete the request.");
        return data;
    }

    async function loadEvents() {
        message.textContent = "Loading events…";
        try {
            const data = await request("/api/dashboard/events/");
            eventList.innerHTML = data.events.map(event => `
                <button class="event-option" type="button" data-event="${escapeHTML(event.slug)}">
                    <span>${escapeHTML(event.name)}</span><span class="event-count">${event.count}</span>
                </button>`).join("");
            message.textContent = "";
            if (data.events.length) {
                const target = data.events.some(event => event.slug === selectedSlug)
                    ? selectedSlug
                    : data.events[0].slug;
                await selectEvent(target);
            }
        } catch (error) { message.textContent = error.message; message.className = "manager-message error"; }
    }

    async function selectEvent(slug) {
        selectedSlug = slug;
        searchInput.disabled = false;
        exportButton.disabled = false;
        document.querySelectorAll(".event-option").forEach(button => button.classList.toggle("active", button.dataset.event === slug));
        message.textContent = "Loading registrations…";
        tableContainer.innerHTML = "";
        try {
            const query = searchInput.value.trim() ? `?search=${encodeURIComponent(searchInput.value.trim())}` : "";
            const data = await request(`/api/dashboard/events/${slug}/${query}`);
            selectedEvent.textContent = data.event.name;
            countElement.textContent = `${data.count} registration${data.count === 1 ? "" : "s"}`;
            renderTable(data);
            message.textContent = "";
        } catch (error) { message.textContent = error.message; message.className = "manager-message error"; }
    }

    function renderTable(data) {
        if (!data.registrations.length) {
            tableContainer.innerHTML = '<div class="empty-state">No registrations found for this event.</div>';
            return;
        }
        tableContainer.innerHTML = `<table class="registration-table"><thead><tr>
            ${data.columns.map(column => `<th>${escapeHTML(label(column, data.column_labels))}</th>`).join("")}<th>Action</th>
            </tr></thead><tbody>${data.registrations.map(row => `<tr>
            ${data.columns.map(column => `<td>${escapeHTML(displayValue(column, row[column]))}</td>`).join("")}
            <td><button type="button" class="delete-registration" data-id="${row.id}">DELETE</button></td>
            </tr>`).join("")}</tbody></table>`;
    }

    eventList.addEventListener("click", event => {
        const button = event.target.closest("[data-event]");
        if (button) selectEvent(button.dataset.event);
    });

    searchInput.addEventListener("input", () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => selectedSlug && selectEvent(selectedSlug), 300);
    });

    exportButton.addEventListener("click", async () => {
        if (!selectedSlug) return;
        const originalText = exportButton.textContent;
        exportButton.disabled = true;
        exportButton.textContent = "EXPORTING…";
        message.className = "manager-message";
        message.textContent = "Preparing the Excel file…";
        try {
            const response = await fetch(`/api/dashboard/events/${selectedSlug}/export/`, {
                credentials: "same-origin"
            });
            if (response.status === 401 || response.status === 403) {
                window.location.href = "/manager/login/";
                return;
            }
            if (!response.ok) throw new Error("Unable to export the registrations.");

            const disposition = response.headers.get("Content-Disposition") || "";
            const filenameMatch = disposition.match(/filename="?([^";]+)"?/i);
            const filename = filenameMatch?.[1] || `qaicys-2026-${selectedSlug}-registrations.xlsx`;
            const downloadUrl = URL.createObjectURL(await response.blob());
            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
            message.textContent = "Excel file downloaded.";
        } catch (error) {
            message.textContent = error.message;
            message.className = "manager-message error";
        } finally {
            exportButton.textContent = originalText;
            exportButton.disabled = !selectedSlug;
        }
    });

    tableContainer.addEventListener("click", async event => {
        const button = event.target.closest(".delete-registration");
        if (!button || !window.confirm("Delete this registration permanently?")) return;
        button.disabled = true;
        try {
            await request(`/api/dashboard/events/${selectedSlug}/${button.dataset.id}/`, {
                method: "DELETE", headers: {"X-CSRFToken": csrfToken()}
            });
            await loadEvents();
        } catch (error) { message.textContent = error.message; button.disabled = false; }
    });

    loadEvents();
})();
