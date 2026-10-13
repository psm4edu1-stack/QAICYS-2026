/* =========================================================
   QAICYS 2026 — SHARED REGISTRATION ANNOUNCEMENT MODAL
========================================================= */

(function () {
    "use strict";

    function initRegistrationModal() {
        if (document.getElementById("qaicysRegistrationModal")) return;

        /* Inject Modal Styles */
        const style = document.createElement("style");
        style.id = "qaicysRegistrationModalStyles";
        style.textContent = `
            .qaicys-modal-backdrop {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(3, 6, 23, 0.88);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                z-index: 99999;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease, visibility 0.3s ease;
            }

            .qaicys-modal-backdrop.active {
                opacity: 1;
                visibility: visible;
            }

            .qaicys-modal-card {
                position: relative;
                width: 100%;
                max-width: 480px;
                background: linear-gradient(135deg, rgba(14, 22, 58, 0.96), rgba(3, 6, 23, 0.98));
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 20px;
                padding: 45px 32px 40px;
                text-align: center;
                box-shadow: 0 0 40px rgba(0, 229, 255, 0.2), 0 0 80px rgba(157, 78, 221, 0.15);
                transform: translateY(20px) scale(0.95);
                transition: transform 0.3s ease;
                overflow: hidden;
            }

            .qaicys-modal-backdrop.active .qaicys-modal-card {
                transform: translateY(0) scale(1);
            }

            .qaicys-modal-card::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: linear-gradient(90deg, #00E5FF, #9D4EDD, #00E5FF);
                background-size: 200% 100%;
                animation: qaicysModalGradient 3s linear infinite;
            }

            @keyframes qaicysModalGradient {
                0% { background-position: 0% 0%; }
                100% { background-position: 200% 0%; }
            }

            .qaicys-modal-close {
                position: absolute;
                top: 16px;
                right: 18px;
                width: 36px;
                height: 36px;
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 50%;
                background: rgba(0, 229, 255, 0.05);
                color: #ffffff;
                font-size: 24px;
                line-height: 1;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.25s ease;
            }

            .qaicys-modal-close:hover,
            .qaicys-modal-close:focus {
                background: rgba(0, 229, 255, 0.2);
                color: #00E5FF;
                border-color: #00E5FF;
                outline: none;
                box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
            }

            .qaicys-modal-eyebrow {
                color: #00E5FF;
                font-size: 15px;
                font-weight: 800;
                letter-spacing: 5px;
                text-transform: uppercase;
                margin-bottom: 16px;
                text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
            }

            .qaicys-modal-title {
                color: #ffffff;
                font-size: clamp(24px, 5vw, 32px);
                font-weight: 900;
                letter-spacing: 3px;
                line-height: 1.2;
                margin-bottom: 18px;
                text-transform: uppercase;
            }

            .qaicys-modal-date {
                color: #9D4EDD;
                font-size: clamp(20px, 4.5vw, 26px);
                font-weight: 800;
                letter-spacing: 2.5px;
                margin-top: 10px;
                text-shadow: 0 0 12px rgba(157, 78, 221, 0.6);
                text-transform: uppercase;
            }
        `;
        document.head.appendChild(style);

        /* Inject Modal HTML */
        const modalDiv = document.createElement("div");
        modalDiv.id = "qaicysRegistrationModal";
        modalDiv.className = "qaicys-modal-backdrop";
        modalDiv.setAttribute("role", "dialog");
        modalDiv.setAttribute("aria-modal", "true");
        modalDiv.setAttribute("aria-labelledby", "qaicysModalTitle");

        modalDiv.innerHTML = `
            <div class="qaicys-modal-card">
                <button type="button" class="qaicys-modal-close" id="qaicysModalClose" aria-label="Close Modal">&times;</button>
                <p class="qaicys-modal-eyebrow">BE READY</p>
                <h2 id="qaicysModalTitle" class="qaicys-modal-title">REGISTRATION OPENS</h2>
                <p class="qaicys-modal-date">10 AUGUST 2026</p>
            </div>
        `;
        document.body.appendChild(modalDiv);

        let scrollPosition = 0;
        let lastFocusedElement = null;

        function openModal(e) {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            lastFocusedElement = document.activeElement;
            scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
            modalDiv.classList.add("active");
            document.body.style.overflow = "hidden";
            const closeBtn = document.getElementById("qaicysModalClose");
            if (closeBtn) closeBtn.focus();
        }

        function closeModal() {
            modalDiv.classList.remove("active");
            document.body.style.overflow = "";
            window.scrollTo(0, scrollPosition);
            if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
                lastFocusedElement.focus();
            }
        }

        /* Expose global functions */
        window.openRegistrationAnnouncement = openModal;
        window.closeRegistrationAnnouncement = closeModal;

        const closeBtn = document.getElementById("qaicysModalClose");
        if (closeBtn) {
            closeBtn.addEventListener("click", closeModal);
        }

        modalDiv.addEventListener("click", function (e) {
            if (e.target === modalDiv) {
                closeModal();
            }
        });

        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && modalDiv.classList.contains("active")) {
                closeModal();
            }
        });

        /* Global click delegation for all registration buttons/links */
        document.addEventListener("click", function (e) {
            const target = e.target.closest("#registerNow, .register-link, .register-btn, [data-register], a[href*='docs.google.com'], a[href*='forms']");
            if (target) {
                openModal(e);
                return;
            }
            const btnTarget = e.target.closest("a, button");
            if (btnTarget && btnTarget.textContent && btnTarget.textContent.trim().toUpperCase().includes("REGISTER NOW")) {
                openModal(e);
            }
        }, true);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initRegistrationModal);
    } else {
        initRegistrationModal();
    }
})();
