(function () {
    "use strict";

    const individualFields = [
        {name: "name", label: "Name"},
        {name: "year_of_study", label: "Year of Study", type: "select", options: ["I Year", "II Year", "III Year"]},
        {name: "department", label: "Department"},
        {name: "registration_number", label: "Registration Number", registration: true},
        {name: "whatsapp_number", label: "Whatsapp Number", type: "tel"},
        {name: "email", label: "Mail ID", type: "email"}
    ];

    function additionalParticipantFields(number, required = true) {
        const prefix = `participant_${number}`;
        return [
            {name: `${prefix}_name`, label: "Name", required},
            {name: `${prefix}_year_of_study`, label: "Year of Study", type: "select", options: ["I Year", "II Year", "III Year"], required},
            {name: `${prefix}_department`, label: "Department", required},
            {name: `${prefix}_registration_number`, label: "Registration Number", registration: true, required},
            {name: `${prefix}_whatsapp_number`, label: "Whatsapp Number", type: "tel", required},
            {name: `${prefix}_email`, label: "Mail ID", type: "email", required}
        ];
    }

    const eventConfigs = {
        "pitch-perfect": {title: "Pitch Perfect", endpoint: "pitch-perfect", listPage: "technical.html", sections: [{title: "Team Details", fields: [{name: "team_name", label: "Team Name"}]}, {title: "Participant 1 Details", fields: individualFields}, {title: "Participant 2 Details", fields: additionalParticipantFields(2)}]},
        "promptopia": {title: "Promptoopia", endpoint: "promptoopia", listPage: "technical.html", sections: [{title: "Participant Details", fields: individualFields}]},
        "pixel-cipher": {title: "Pixel Cipher", endpoint: "pixel-cipher", listPage: "technical.html", sections: [{title: "Participant Details", fields: individualFields}]},
        "synapse": {title: "Synapse", endpoint: "synapse", listPage: "technical.html", sections: [{title: "Team Details", fields: [{name: "team_name", label: "Team Name"}]}, {title: "Participant 1 Details", fields: individualFields}, {title: "Participant 2 Details", fields: additionalParticipantFields(2)}]},
        "henna-hues": {title: "Henna Hues", endpoint: "henna-hues", listPage: "nontechnical.html", sections: [{title: "Team Details", fields: [{name: "team_name", label: "Team Name"}]}, {title: "Participant 1 — Artist Details", fields: individualFields}, {title: "Participant 2 — Model Details", fields: additionalParticipantFields(2)}]},
        "palette-pop": {title: "Palette Pop", endpoint: "palette-pop", listPage: "nontechnical.html", sections: [{title: "Team Details", fields: [{name: "team_name", label: "Team Name"}]}, {title: "Participant 1 — Artist Details", fields: individualFields}, {title: "Participant 2 — Model Details", fields: additionalParticipantFields(2)}]},
        "clickcraft": {title: "Click Craft", endpoint: "click-craft", listPage: "nontechnical.html", sections: [{title: "Participant Details", fields: individualFields}]},
        "unscripted": {title: "Unscripted", endpoint: "unscripted", listPage: "nontechnical.html", sections: [
            {title: "Team Details", fields: [{name: "team_name", label: "Team Name"}, {name: "team_size", label: "Number of Participants", type: "select", options: ["1", "2", "3", "4", "5"]}]},
            {title: "Participant 1 Details", participantNumber: 1, fields: individualFields},
            ...[2, 3, 4, 5].map(number => ({title: `Participant ${number} Details`, participantNumber: number, fields: additionalParticipantFields(number, false)}))
        ]},
        "the-verdict": {title: "The Verdict", endpoint: "the-verdict", listPage: "nontechnical.html", sections: [{title: "Participant Details", fields: [...individualFields, {name: "language", label: "Language", type: "select", options: ["English", "Tamil"]}]}]},
        "estrella": {title: "Estrella — Star of the Event", endpoint: "estrella", listPage: "nontechnical.html", sections: [{title: "Participant Details", fields: [...individualFields,
            {name: "participated_in_technical_or_non_technical_event", label: "Have you participated in at least one technical or non-technical event?", type: "select", options: [{value: "", label: "Select an option"}, {value: "true", label: "Yes"}, {value: "false", label: "No"}]},
            {name: "technical_or_non_technical_events", label: "If yes, mention the technical or non-technical event(s)", type: "textarea", conditional: true, required: false}
        ]}]},
        "bid-byte": {title: "Bid Byte", endpoint: "bid-byte", listPage: "technical.html", sections: [
            {title: "Team Details", fields: [{name: "team_name", label: "Team Name"}]},
            {title: "Team Lead Details", fields: [
                {name: "team_lead_name", label: "Team Lead Name"}, {name: "team_lead", label: "Team Lead"},
                {name: "team_lead_registration_number", label: "Team Lead Register Number", registration: true},
                {name: "team_lead_phone_number", label: "Team Lead Phone Number", type: "tel"}, {name: "team_lead_email", label: "Team Lead Email", type: "email"}
            ]},
            {title: "Member 1 Details", fields: memberFields("member_1", "Member 1", "phone_number", "year_department")},
            {title: "Member 2 Details", fields: memberFields("member_2", "Member 2", "phone_number", "year_department")}
        ]},
        "battlezone": {title: "Battle Zone — E-Sports", endpoint: "battle-zone", listPage: "nontechnical.html", sections: [
            {title: "Team Details", fields: [{name: "team_name", label: "Team Name"}]},
            battleMemberSection("team_lead", "Team Lead"), battleMemberSection("member_1", "Team Member 1"),
            battleMemberSection("member_2", "Team Member 2"), battleMemberSection("member_3", "Team Member 3")
        ]}
    };

    function memberFields(prefix, label, phoneSuffix, departmentSuffix) {
        return [
            {name: `${prefix}_name`, label: `${label} Name`},
            {name: `${prefix}_registration_number`, label: `${label} Register Number`, registration: true},
            {name: `${prefix}_${phoneSuffix}`, label: `${label} Phone Number`, type: "tel"},
            {name: `${prefix}_email`, label: `${label} Email`, type: "email"},
            {name: `${prefix}_${departmentSuffix}`, label: `${label} Year & Department`}
        ];
    }

    function battleMemberSection(prefix, label) {
        return {title: `${label} Details`, fields: [
            {name: `${prefix}_name`, label: `${label} Name`},
            {name: `${prefix}_registration_number`, label: "Register Number", registration: true},
            {name: `${prefix}_contact_number`, label: "Contact Number", type: "tel"},
            {name: `${prefix}_email`, label: "E-Mail", type: "email"},
            {name: `${prefix}_department_year`, label: "Department & Year"}
        ]};
    }

    const eventId = new URLSearchParams(window.location.search).get("event");
    const config = eventConfigs[eventId];
    const form = document.getElementById("registrationForm");
    const fieldsContainer = document.getElementById("formFields");
    const title = document.getElementById("registrationTitle");
    const message = document.getElementById("formMessage");
    const submitButton = document.getElementById("submitRegistration");
    const backLink = document.getElementById("backToEvent");
    let validNumbers = null;
    let submitting = false;

    if (!config) {
        title.textContent = "EVENT NOT FOUND";
        form.hidden = true;
        backLink.href = "events.html";
        return;
    }

    document.title = `${config.title} Registration | QAICYS 2026`;
    title.textContent = config.title;
    backLink.href = config.listPage;
    fieldsContainer.innerHTML = config.sections.map(renderSection).join("");

    function renderSection(section) {
        const participantAttribute = section.participantNumber ? ` data-participant-section="${section.participantNumber}"` : "";
        const hidden = section.participantNumber > 1 ? " hidden" : "";
        return `<section class="form-section"${participantAttribute}${hidden}><h2>${escapeHTML(section.title)}</h2><div class="form-grid">
            ${section.fields.map(renderField).join("")}</div></section>`;
    }

    function renderField(field) {
        const required = field.required !== false;
        const options = field.options || [];
        let control;
        if (field.type === "select") {
            const normalized = options.map(option => typeof option === "string" ? {value: option, label: option} : option);
            const first = normalized[0]?.value === "" ? "" : '<option value="">Select an option</option>';
            control = `<select id="${field.name}" name="${field.name}" ${required ? "required" : ""}>${first}${normalized.map(option => `<option value="${escapeHTML(option.value)}">${escapeHTML(option.label)}</option>`).join("")}</select>`;
        } else if (field.type === "textarea") {
            control = `<textarea id="${field.name}" name="${field.name}" ${required ? "required" : ""}></textarea>`;
        } else {
            const attrs = field.registration ? 'autocomplete="off" autocapitalize="characters" spellcheck="false"' : "";
            control = `<input id="${field.name}" name="${field.name}" type="${field.type || "text"}" ${required ? "required" : ""} ${attrs}>`;
        }
        return `<div class="form-group${field.conditional ? " conditional-field full-width" : ""}" data-field="${field.name}" ${field.conditional ? "hidden" : ""}>
            <label for="${field.name}">${escapeHTML(field.label)}${required ? ' <span class="required-mark">*</span>' : ""}</label>
            ${control}<p class="field-feedback" aria-live="polite"></p></div>`;
    }

    function escapeHTML(value) {
        return String(value).replace(/[&<>'"]/g, char => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"})[char]);
    }

    function normalizeNumber(value) { return String(value).trim().toUpperCase(); }

    function collectNumbers(node, result = []) {
        if (Array.isArray(node)) result.push(...node);
        else if (node && typeof node === "object") Object.values(node).forEach(value => collectNumbers(value, result));
        return result;
    }

    async function loadRegistrationNumbers() {
        try {
            const response = await fetch("../registration-numbers.json", {cache: "no-cache"});
            if (!response.ok) throw new Error("Number list unavailable");
            const data = await response.json();
            validNumbers = new Set(collectNumbers(data).map(normalizeNumber));
        } catch (error) {
            validNumbers = null;
        }
    }

    function setFieldState(name, state, text) {
        const group = form.querySelector(`[data-field="${name}"]`);
        if (!group) return;
        group.classList.toggle("has-error", state === "error");
        group.classList.toggle("is-valid", state === "valid");
        group.querySelector(".field-feedback").textContent = text || "";
    }

    function validateRegistrationInput(input) {
        const number = normalizeNumber(input.value);
        input.value = number;
        if (!number) { setFieldState(input.name, "error", "Registration number is required."); return false; }
        if (validNumbers && !validNumbers.has(number)) { setFieldState(input.name, "error", "Invalid registration number."); return false; }
        if (!validNumbers) { setFieldState(input.name, "", "The server will verify this number on submission."); return true; }
        setFieldState(input.name, "valid", "✓ Valid registration number");
        return true;
    }

    form.querySelectorAll("[name$='registration_number']").forEach(input => {
        input.addEventListener("blur", () => validateRegistrationInput(input));
        input.addEventListener("input", () => setFieldState(input.name, "", ""));
    });

    const eventParticipation = form.elements.participated_in_technical_or_non_technical_event;
    if (eventParticipation) {
        eventParticipation.addEventListener("change", () => {
            const group = form.querySelector("[data-field='technical_or_non_technical_events']");
            const input = form.elements.technical_or_non_technical_events;
            const show = eventParticipation.value === "true";
            group.hidden = !show;
            input.required = show;
            if (!show) { input.value = ""; setFieldState("technical_or_non_technical_events", "", ""); }
        });
    }

    const teamSize = form.elements.team_size;
    if (teamSize) {
        teamSize.addEventListener("change", () => {
            const selectedSize = Number(teamSize.value || 1);
            form.querySelectorAll("[data-participant-section]").forEach(section => {
                const participantNumber = Number(section.dataset.participantSection);
                const active = participantNumber <= selectedSize;
                section.hidden = !active;
                section.querySelectorAll("input, select, textarea").forEach(input => {
                    input.required = active;
                    input.disabled = !active;
                    if (!active) {
                        input.value = "";
                        setFieldState(input.name, "", "");
                    }
                });
            });
        });
        teamSize.dispatchEvent(new Event("change"));
    }

    function validateForm() {
        let valid = true;
        form.querySelectorAll("[required]").forEach(input => {
            if (!input.value.trim()) { setFieldState(input.name, "error", "This field is required."); valid = false; }
            else if (input.type === "email" && !input.validity.valid) { setFieldState(input.name, "error", "Enter a valid email address."); valid = false; }
            else if (!input.name.endsWith("registration_number")) setFieldState(input.name, "", "");
        });

        const registrationInputs = [...form.querySelectorAll("[name$='registration_number']:not(:disabled)")];
        registrationInputs.forEach(input => {
            if (!validateRegistrationInput(input)) valid = false;
        });
        const numbers = registrationInputs.map(input => normalizeNumber(input.value));
        const duplicates = numbers.filter((number, index) => number && numbers.indexOf(number) !== index);
        if (duplicates.length) {
            registrationInputs.filter(input => duplicates.includes(normalizeNumber(input.value))).forEach(input => setFieldState(input.name, "error", "A registration number cannot be used twice in the same team."));
            valid = false;
        }
        return valid;
    }

    function payloadFromForm() {
        const payload = Object.fromEntries(new FormData(form).entries());
        if (Object.hasOwn(payload, "participated_in_technical_or_non_technical_event")) {
            payload.participated_in_technical_or_non_technical_event = payload.participated_in_technical_or_non_technical_event === "true";
        }
        return payload;
    }

    function showBackendErrors(errors) {
        Object.entries(errors || {}).forEach(([field, messages]) => {
            if (form.elements[field]) setFieldState(field, "error", Array.isArray(messages) ? messages[0] : messages);
        });
    }

    form.addEventListener("submit", async event => {
        event.preventDefault();
        if (submitting || !validateForm()) {
            message.className = "form-message error";
            message.textContent = "Please correct the highlighted fields before submitting.";
            form.querySelector(".has-error input, .has-error select, .has-error textarea")?.focus();
            return;
        }
        submitting = true;
        submitButton.disabled = true;
        submitButton.textContent = "SUBMITTING…";
        message.className = "form-message";
        message.textContent = "";
        try {
            const baseUrl = (window.QAICYS_CONFIG?.API_BASE_URL || "").replace(/\/$/, "");
            const response = await fetch(`${baseUrl}/api/registration/${config.endpoint}/`, {
                method: "POST", headers: {"Content-Type": "application/json", "Accept": "application/json"},
                body: JSON.stringify(payloadFromForm())
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok) {
                showBackendErrors(data.errors);
                const nonFieldError = data.errors?.non_field_errors?.[0];
                throw new Error(nonFieldError || "Your registration could not be submitted. Check the highlighted fields.");
            }
            message.className = "form-message success";
            message.textContent = data.message || "Registration submitted successfully.";
            form.reset();
            form.querySelectorAll(".form-group").forEach(group => group.classList.remove("has-error", "is-valid"));
            form.querySelectorAll(".field-feedback").forEach(feedback => feedback.textContent = "");
            if (eventParticipation) eventParticipation.dispatchEvent(new Event("change"));
            message.scrollIntoView({behavior: "smooth", block: "center"});
        } catch (error) {
            message.className = "form-message error";
            message.textContent = error.message === "Failed to fetch" ? "Unable to reach the registration server. Please try again shortly." : error.message;
        } finally {
            submitting = false;
            submitButton.disabled = false;
            submitButton.textContent = "SUBMIT REGISTRATION →";
        }
    });

    loadRegistrationNumbers();
})();
