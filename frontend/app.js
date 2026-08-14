const API_URL = "http://127.0.0.1:8000";

let currentLanguage = "English";


/* -------------------------
   GENERAL
------------------------- */

function scrollToSection(id) {

    document.getElementById(id).scrollIntoView({
        behavior: "smooth"
    });

}


/* -------------------------
   LANGUAGE
------------------------- */

function setLanguage(language) {

    currentLanguage = language;

    document.getElementById("languageStatus").innerText =
        "Current language: " + language;

}


/* -------------------------
   CHAT
------------------------- */

function handleEnter(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

}


function quickQuestion(question) {

    document.getElementById("userInput").value = question;

    scrollToSection("assistant");

    sendMessage();

}


function addMessage(text, type) {

    const messages =
        document.getElementById("chatMessages");

    const message =
        document.createElement("div");

    message.className =
        "message " + type;


    if (type === "bot") {

        message.innerHTML = `
            <div class="avatar">🤖</div>
            <div>${text}</div>
        `;

    } else {

        message.innerHTML = `
            <div>${text}</div>
        `;

    }


    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;

}


async function sendMessage() {

    const input =
        document.getElementById("userInput");

    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    addMessage(question, "user");

    input.value = "";


    addMessage(
        "Sahayak is thinking...",
        "bot"
    );


    try {

        const response =
            await fetch(
                `${API_URL}/api/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: question,
                        language: currentLanguage
                    })
                }
            );


        const data =
            await response.json();


        const messages =
            document.getElementById(
                "chatMessages"
            );


        messages.lastElementChild.remove();


        addMessage(
            data.response,
            "bot"
        );


    } catch (error) {

        const messages =
            document.getElementById(
                "chatMessages"
            );

        messages.lastElementChild.remove();


        addMessage(
            "Backend is not running. Please start the FastAPI server.",
            "bot"
        );

    }

}


/* -------------------------
   SCAM SCANNER
------------------------- */

async function scanScam() {

    const input =
        document.getElementById(
            "scamInput"
        ).value.trim();


    const result =
        document.getElementById(
            "scanResult"
        );


    if (!input) {

        result.innerHTML = `
            <div class="service-card">
                Please enter a message or URL.
            </div>
        `;

        return;
    }


    result.innerHTML = `
        <div class="service-card">
            🔍 Analysing...
        </div>
    `;


    try {

        const response =
            await fetch(
                `${API_URL}/api/scan`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        content: input
                    })
                }
            );


        const data =
            await response.json();


        let riskClass = "";


        result.innerHTML = `

            <div class="service-card">

                <h3>
                    ${data.risk_level}
                </h3>

                <p>
                    Risk Score:
                    <strong>
                        ${data.risk_score}/100
                    </strong>
                </p>

                <p>
                    ${data.message}
                </p>

                <h4>Detected indicators:</h4>

                <ul>
                    ${
                        data.indicators
                        .map(
                            item =>
                            `<li>${item}</li>`
                        )
                        .join("")
                    }
                </ul>

            </div>
        `;


    } catch (error) {

        result.innerHTML = `
            <div class="service-card">
                Unable to connect to security engine.
            </div>
        `;

    }

}


/* -------------------------
   VOICE ASSISTANT
------------------------- */

function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Voice recognition is not supported in this browser."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    if (currentLanguage === "ಕನ್ನಡ") {

        recognition.lang = "kn-IN";

    } else if (currentLanguage === "हिन्दी") {

        recognition.lang = "hi-IN";

    } else {

        recognition.lang = "en-IN";

    }


    recognition.start();


    recognition.onresult = function(event) {

        const text =
            event.results[0][0].transcript;


        document.getElementById(
            "userInput"
        ).value = text;


        sendMessage();

    };


    recognition.onerror = function() {

        alert(
            "Voice recognition failed. Please try again."
        );

    };

}


/* -------------------------
   SENIOR CITIZEN MODE
------------------------- */

document
    .getElementById("seniorModeBtn")
    .addEventListener(
        "click",
        function() {

            document.body.classList.toggle(
                "senior-mode"
            );

        }
    );