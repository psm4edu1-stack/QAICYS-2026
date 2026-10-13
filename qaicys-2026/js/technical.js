/* =========================================================
   QAICYS 2026
   REGISTRATION PAGE
   register.js
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       1. EVENT DATA
    ===================================================== */

    const EVENT_DATA = {

        technical: [
            {
                value: "pitch-perfect",
                name: "PITCH PERFECT",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "bid-byte",
                name: "BID BYTE",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "promptopia",
                name: "PROMPTOPIA",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "pixel-cipher",
                name: "PIXEL CIPHER",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "synapse",
                name: "SYNAPSE",
                minParticipants: 1,
                maxParticipants: 1
            }
        ],


        "non-technical": [
            {
                value: "henna-hues",
                name: "HENNA HUES",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "palette-pop",
                name: "PALETTE POP",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "the-verdict",
                name: "THE VERDICT",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "clickcraft",
                name: "CLICKCRAFT",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "unscripted",
                name: "UNSCRIPTED",

                // You specifically gave this rule:
                // minimum 2 and maximum 4

                minParticipants: 2,
                maxParticipants: 4
            },

            {
                value: "estrella",
                name: "ESTRELLA",
                minParticipants: 1,
                maxParticipants: 1
            },

            {
                value: "battlezone",
                name: "BATTLEZONE",
                minParticipants: 1,
                maxParticipants: 1
            }
        ]
    };


    /* =====================================================
       2. DEPARTMENTS
    ===================================================== */

    const DEPARTMENTS = [

        "B.Com(General)",
        "B.Com(CA)",
        "B.Com(PA)",

        "BBA(General)",
        "BBA(DM)",
        "BBA(BA)",

        "PSYCHOLOGY",
        "VISCOM",
        "CDFT",

        "CS(DSA)",
        "CS(FINTECH)",

        "M.Sc.,CS",
        "M.Comm"

    ];


    /* =====================================================
       3. GET MAIN ELEMENTS
    ===================================================== */

    const category1 =
        document.getElementById("category1");

    const event1 =
        document.getElementById("event1");


    /* =====================================================
       SAFETY CHECK
    ===================================================== */

    if (!category1) {

        console.error(
            'ERROR: Element with id="category1" not found.'
        );

    }


    if (!event1) {

        console.error(
            'ERROR: Element with id="event1" not found.'
        );

    }


    if (!category1 || !event1) {

        return;

    }


    /* =====================================================
       4. POPULATE EVENT DROPDOWN
    ===================================================== */

    function populateEventDropdown(
        categorySelect,
        eventSelect
    ) {

        const category =
            categorySelect.value;


        /* Reset */

        eventSelect.innerHTML = "";


        /* No category */

        if (!category) {

            eventSelect.disabled = true;

            eventSelect.innerHTML = `
                <option value="">
                    Select category first
                </option>
            `;

            return;

        }


        /* Get correct event array */

        const events =
            EVENT_DATA[category];


        /* Invalid category */

        if (!events) {

            eventSelect.disabled = true;

            eventSelect.innerHTML = `
                <option value="">
                    No events available
                </option>
            `;

            return;

        }


        /* Enable event dropdown */

        eventSelect.disabled = false;


        /* Default option */

        const firstOption =
            document.createElement("option");

        firstOption.value = "";

        firstOption.textContent =
            "Select Event";

        firstOption.selected = true;


        eventSelect.appendChild(
            firstOption
        );


        /* Add events */

        events.forEach(event => {

            const option =
                document.createElement("option");


            option.value =
                event.value;


            option.textContent =
                event.name;


            option.dataset.min =
                event.minParticipants;


            option.dataset.max =
                event.maxParticipants;


            eventSelect.appendChild(
                option
            );

        });

    }


    /* =====================================================
       5. CATEGORY 01 CHANGE
    ===================================================== */

    category1.addEventListener(
        "change",
        () => {

            populateEventDropdown(
                category1,
                event1
            );

        }
    );


    /* =====================================================
       6. EVENT 01 CHANGE
    ===================================================== */

    event1.addEventListener(
        "change",
        () => {

            const eventValue =
                event1.value;


            if (!eventValue) {

                return;

            }


            const eventDetails =
                getEventDetails(eventValue);


            if (!eventDetails) {

                return;

            }


            console.log(
                "Selected Event:",
                eventDetails.name
            );


            console.log(
                "Minimum Participants:",
                eventDetails.minParticipants
            );


            console.log(
                "Maximum Participants:",
                eventDetails.maxParticipants
            );


            /* Update participant system */

            setupParticipants(
                eventDetails
            );

        }
    );


    /* =====================================================
       7. GET EVENT DETAILS
    ===================================================== */

    function getEventDetails(eventValue) {

        const allEvents = [

            ...EVENT_DATA.technical,

            ...EVENT_DATA["non-technical"]

        ];


        return allEvents.find(
            event =>
                event.value === eventValue
        );

    }


    /* =====================================================
       8. PARTICIPANT SYSTEM
    ===================================================== */

    function setupParticipants(eventDetails) {

        /*
           This function works only if your HTML
           contains:

           id="participantSection"
           id="participantsContainer"
           id="addParticipantBtn"
           id="participantCount"

        */


        const participantSection =
            document.getElementById(
                "participantSection"
            );


        const participantsContainer =
            document.getElementById(
                "participantsContainer"
            );


        const addParticipantBtn =
            document.getElementById(
                "addParticipantBtn"
            );


        const participantCount =
            document.getElementById(
                "participantCount"
            );


        /* If participant HTML isn't available yet */

        if (
            !participantSection ||
            !participantsContainer
        ) {

            return;

        }


        participantSection.style.display =
            "block";


        /* Remove old participant forms */

        participantsContainer.innerHTML = "";


        /* Minimum participants */

        const minimum =
            eventDetails.minParticipants;


        const maximum =
            eventDetails.maxParticipants;


        /* Create default participant boxes */

        for (
            let i = 1;
            i <= minimum;
            i++
        ) {

            participantsContainer.appendChild(
                createParticipantForm(i)
            );

        }


        updateParticipantCount(
            participantsContainer,
            participantCount,
            maximum
        );


        /* Individual event */

        if (
            minimum === 1 &&
            maximum === 1
        ) {

            if (addParticipantBtn) {

                addParticipantBtn.style.display =
                    "none";

            }

            return;

        }


        /* Team event */

        if (addParticipantBtn) {

            addParticipantBtn.style.display =
                "inline-flex";


            addParticipantBtn.dataset.max =
                maximum;


            /*
               Remove previous event listener
               by cloning button.
            */

            const newButton =
                addParticipantBtn.cloneNode(true);


            addParticipantBtn.replaceWith(
                newButton
            );


            newButton.addEventListener(
                "click",
                () => {

                    const currentCount =
                        participantsContainer
                            .querySelectorAll(
                                ".participant-card"
                            )
                            .length;


                    /* STOP at maximum */

                    if (
                        currentCount >= maximum
                    ) {

                        return;

                    }


                    const newNumber =
                        currentCount + 1;


                    participantsContainer
                        .appendChild(

                            createParticipantForm(
                                newNumber
                            )

                        );


                    updateParticipantCount(
                        participantsContainer,
                        participantCount,
                        maximum
                    );


                    /* Hide button at max */

                    if (
                        newNumber >= maximum
                    ) {

                        newButton.style.display =
                            "none";

                    }

                }
            );

        }

    }


    /* =====================================================
       9. CREATE PARTICIPANT FORM
    ===================================================== */

    function createParticipantForm(number) {

        const participant =
            document.createElement("div");


        participant.className =
            "participant-card";


        participant.dataset.participant =
            number;


        participant.innerHTML = `

            <div class="participant-heading">

                <span class="participant-number">
                    ${String(number).padStart(2, "0")}
                </span>

                <div>

                    <span class="small-label">
                        PARTICIPANT
                    </span>

                    <h3>
                        PARTICIPANT ${number}
                    </h3>

                </div>

            </div>


            <div class="participant-fields">


                <!-- NAME -->

                <div class="field-group">

                    <label>
                        NAME
                    </label>

                    <input
                        type="text"
                        class="participant-name"
                        placeholder="Enter participant name"
                        autocomplete="name"
                        required
                    >

                </div>


                <!-- YEAR -->

                <div class="field-group">

                    <label>
                        YEAR
                    </label>

                    <select
                        class="participant-year"
                        required
                    >

                        <option value="">
                            Select Year
                        </option>

                        <option value="1">
                            1st Year
                        </option>

                        <option value="2">
                            2nd Year
                        </option>

                        <option value="3">
                            3rd Year
                        </option>

                    </select>

                </div>


                <!-- REGISTRATION NUMBER -->

                <div class="field-group">

                    <label>
                        REGISTRATION NUMBER
                    </label>

                    <input
                        type="text"
                        class="participant-regno"
                        placeholder="Registration Number"
                        required
                    >

                </div>


                <!-- EMAIL -->

                <div class="field-group">

                    <label>
                        EMAIL
                    </label>

                    <input
                        type="email"
                        class="participant-email"
                        placeholder="College Email"
                        autocomplete="email"
                        required
                    >

                </div>


                <!-- DEPARTMENT -->

                <div class="field-group">

                    <label>
                        DEPARTMENT
                    </label>

                    <select
                        class="participant-department"
                        required
                    >

                        <option value="">
                            Select Department
                        </option>

                        ${DEPARTMENTS.map(
                            department => `
                                <option value="${department}">
                                    ${department}
                                </option>
                            `
                        ).join("")}

                    </select>

                </div>


                <!-- WHATSAPP -->

                <div class="field-group">

                    <label>
                        WHATSAPP NUMBER
                    </label>

                    <input
                        type="tel"
                        class="participant-phone"
                        placeholder="10-digit mobile number"
                        maxlength="10"
                        inputmode="numeric"
                        required
                    >

                </div>


                <!-- VALIDATION MESSAGE -->

                <div class="participant-validation">

                    Select year of study to continue
                    verification.

                </div>


            </div>

        `;


        /* =================================================
           PHONE VALIDATION
        ================================================= */

        const phone =
            participant.querySelector(
                ".participant-phone"
            );


        phone.addEventListener(
            "input",
            function () {

                /*
                   Allow numbers only
                */

                this.value =
                    this.value
                        .replace(/\D/g, "")
                        .slice(0, 10);

            }
        );


        /* =================================================
           REGISTRATION NUMBER NORMALIZATION
        ================================================= */

        const regNo =
            participant.querySelector(
                ".participant-regno"
            );


        regNo.addEventListener(
            "input",
            function () {

                this.value =
                    this.value
                        .toUpperCase()
                        .replace(/\s+/g, "");

            }
        );


        /* =================================================
           YEAR MESSAGE
        ================================================= */

        const year =
            participant.querySelector(
                ".participant-year"
            );


        const validationMessage =
            participant.querySelector(
                ".participant-validation"
            );


        year.addEventListener(
            "change",
            function () {

                if (!this.value) {

                    validationMessage.textContent =
                        "Select year of study to continue verification.";

                    return;

                }


                validationMessage.textContent =
                    "Enter your registration number and email for verification.";

            }
        );


        return participant;

    }


    /* =====================================================
       10. PARTICIPANT COUNT
    ===================================================== */

    function updateParticipantCount(
        container,
        countElement,
        maximum
    ) {

        if (!countElement) {

            return;

        }


        const current =
            container.querySelectorAll(
                ".participant-card"
            ).length;


        countElement.textContent =
            `${current} / ${maximum} PARTICIPANTS`;

    }


    /* =====================================================
       11. SECOND EVENT
    ===================================================== */

    const addSecondEventBtn =
        document.getElementById(
            "addSecondEventBtn"
        );


    const secondEventContainer =
        document.getElementById(
            "secondEventContainer"
        );


    if (
        addSecondEventBtn &&
        secondEventContainer
    ) {

        addSecondEventBtn.addEventListener(
            "click",
            () => {

                /*
                   Prevent adding twice
                */

                if (
                    secondEventContainer
                        .dataset.active === "true"
                ) {

                    return;

                }


                secondEventContainer
                    .dataset.active = "true";


                secondEventContainer.innerHTML = `

                    <div class="event-selection-card">

                        <div class="event-card-header">

                            <span>
                                EVENT 02
                            </span>

                        </div>


                        <div class="event-select-grid">


                            <div class="field-group">

                                <label>
                                    CATEGORY
                                </label>

                                <select
                                    id="category2"
                                    required
                                >

                                    <option value="">
                                        Select Category
                                    </option>

                                    <option value="technical">
                                        Technical
                                    </option>

                                    <option value="non-technical">
                                        Non-Technical
                                    </option>

                                </select>

                            </div>


                            <div class="field-group">

                                <label>
                                    EVENT
                                </label>

                                <select
                                    id="event2"
                                    disabled
                                    required
                                >

                                    <option value="">
                                        Select category first
                                    </option>

                                </select>

                            </div>


                        </div>


                        <button
                            type="button"
                            id="removeSecondEvent"
                            class="remove-event-btn"
                        >
                            × REMOVE SECOND EVENT
                        </button>


                    </div>

                `;


                const category2 =
                    document.getElementById(
                        "category2"
                    );


                const event2 =
                    document.getElementById(
                        "event2"
                    );


                category2.addEventListener(
                    "change",
                    () => {

                        populateEventDropdown(
                            category2,
                            event2
                        );

                    }
                );


                /*
                   Prevent same event twice
                */

                event2.addEventListener(
                    "change",
                    () => {

                        if (
                            event2.value &&
                            event2.value === event1.value
                        ) {

                            alert(
                                "You have already selected this event."
                            );


                            event2.value = "";

                        }

                    }
                );


                /* Remove Event 02 */

                document
                    .getElementById(
                        "removeSecondEvent"
                    )
                    .addEventListener(
                        "click",
                        () => {

                            secondEventContainer
                                .innerHTML = "";


                            secondEventContainer
                                .dataset.active =
                                "false";


                            addSecondEventBtn
                                .style.display =
                                "inline-flex";

                        }
                    );


                /*
                   Hide add button
                */

                addSecondEventBtn.style.display =
                    "none";

            }
        );

    }


    /* =====================================================
       12. FORM
    ===================================================== */

    const registrationForm =
        document.getElementById(
            "registrationForm"
        );


    const ruleCheckbox =
        document.getElementById(
            "ruleAgreement"
        );


    const statusMessage =
        document.getElementById(
            "registrationStatus"
        );


    if (registrationForm) {

        registrationForm.addEventListener(
            "submit",
            event => {

                event.preventDefault();


                /* =========================================
                   EVENT CHECK
                ========================================= */

                if (!category1.value) {

                    showStatus(
                        "Please select an event category.",
                        "error"
                    );

                    category1.focus();

                    return;

                }


                if (!event1.value) {

                    showStatus(
                        "Please select an event.",
                        "error"
                    );

                    event1.focus();

                    return;

                }


                /* =========================================
                   PARTICIPANT VALIDATION
                ========================================= */

                const participantCards =
                    document.querySelectorAll(
                        ".participant-card"
                    );


                for (
                    let i = 0;
                    i < participantCards.length;
                    i++
                ) {

                    const card =
                        participantCards[i];


                    const name =
                        card.querySelector(
                            ".participant-name"
                        );


                    const year =
                        card.querySelector(
                            ".participant-year"
                        );


                    const regNo =
                        card.querySelector(
                            ".participant-regno"
                        );


                    const email =
                        card.querySelector(
                            ".participant-email"
                        );


                    const department =
                        card.querySelector(
                            ".participant-department"
                        );


                    const phone =
                        card.querySelector(
                            ".participant-phone"
                        );


                    /* NAME */

                    if (
                        !name ||
                        !name.value.trim()
                    ) {

                        showStatus(
                            `Enter Participant ${i + 1} name.`,
                            "error"
                        );

                        name?.focus();

                        return;

                    }


                    /* YEAR */

                    if (
                        !year ||
                        !year.value
                    ) {

                        showStatus(
                            `Select Participant ${i + 1} year.`,
                            "error"
                        );

                        year?.focus();

                        return;

                    }


                    /* REG NO */

                    if (
                        !regNo ||
                        !regNo.value.trim()
                    ) {

                        showStatus(
                            `Enter Participant ${i + 1} registration number.`,
                            "error"
                        );

                        regNo?.focus();

                        return;

                    }


                    /* EMAIL */

                    if (
                        !email ||
                        !email.value.trim()
                    ) {

                        showStatus(
                            `Enter Participant ${i + 1} email.`,
                            "error"
                        );

                        email?.focus();

                        return;

                    }


                    if (
                        !isValidEmail(
                            email.value
                        )
                    ) {

                        showStatus(
                            `Enter a valid email for Participant ${i + 1}.`,
                            "error"
                        );

                        email.focus();

                        return;

                    }


                    /* DEPARTMENT */

                    if (
                        !department ||
                        !department.value
                    ) {

                        showStatus(
                            `Select Participant ${i + 1} department.`,
                            "error"
                        );

                        department?.focus();

                        return;

                    }


                    /* PHONE */

                    if (
                        !phone ||
                        !/^[6-9]\d{9}$/.test(
                            phone.value
                        )
                    ) {

                        showStatus(
                            `Enter a valid 10-digit WhatsApp number for Participant ${i + 1}.`,
                            "error"
                        );

                        phone?.focus();

                        return;

                    }

                }


                /* =========================================
                   RULE AGREEMENT
                ========================================= */

                if (
                    ruleCheckbox &&
                    !ruleCheckbox.checked
                ) {

                    showStatus(
                        "Please agree to the QAICYS 2026 Rule Book.",
                        "error"
                    );

                    ruleCheckbox.focus();

                    return;

                }


                /* =========================================
                   SUCCESS
                ========================================= */

                showStatus(
                    "✓ Registration details validated successfully!",
                    "success"
                );


                /*
                   Google Sheets submission will be
                   connected here later.
                */


                /* Uncheck rule checkbox */

                if (ruleCheckbox) {

                    ruleCheckbox.checked =
                        false;

                }


                /* Remove success message after 3 sec */

                setTimeout(() => {

                    if (statusMessage) {

                        statusMessage.textContent =
                            "";

                        statusMessage.className =
                            "";

                    }

                }, 3000);

            }
        );

    }


    /* =====================================================
       13. EMAIL VALIDATION
    ===================================================== */

    function isValidEmail(email) {

        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/
            .test(
                email.trim()
            );

    }


    /* =====================================================
       14. STATUS MESSAGE
    ===================================================== */

    function showStatus(
        message,
        type
    ) {

        if (!statusMessage) {

            if (type === "error") {

                alert(message);

            }

            return;

        }


        statusMessage.textContent =
            message;


        statusMessage.className =
            `registration-status ${type}`;

    }


    /* =====================================================
       15. INITIAL PAGE STATE
    ===================================================== */

    event1.disabled = true;


    event1.innerHTML = `
        <option value="">
            Select category first
        </option>
    `;

});