document.addEventListener("DOMContentLoaded", () => {
  //TOGGLE CHATBOX
  const chatboxToggle = document.querySelector(".chatbox-toggle");
  const chatboxMessage = document.querySelector(".chatbox-message-wrapper");
  chatboxToggle.addEventListener("click", function () {
    chatboxMessage.classList.toggle("show");
  });

  // FAQ Accordion
  const faqContainer = document.querySelector(".faq-content");

  faqContainer.addEventListener("click", (e) => {
    const groupHeader = e.target.closest(".faq-group-header");
    if (!groupHeader) return;

    const group = groupHeader.parentElement;
    const groupBody = group.querySelector(".faq-group-body");
    const icon = groupHeader.querySelector("i");

    //Toggle icon
    icon.classList.toggle("fa-plus");
    icon.classList.toggle("fa-minus");

    //Toggle visibility of body
    groupBody.classList.toggle("open");

    // Close Other open FAQ bodies
    const otherGroups = faqContainer.querySelectorAll(".faq-group");

    otherGroups.forEach((otherGroup) => {
      if (otherGroup !== group) {
        const otherGroupBody = otherGroup.querySelector(".faq-group-body");
        const otherIcon = otherGroup.querySelector(".faq-group-header i");

        otherGroupBody.classList.remove("open");
        otherIcon.classList.remove("fa-minus");
        otherIcon.classList.add("fa-plus");
      }
    });
  });
});

//DROPDOWN TOGGLE
const dropdownToggle = document.querySelector(
  ".chatbox-message-dropdown-toggle"
);
const dropdownMenu = document.querySelector(".chatbox-message-dropdown-menu");

dropdownToggle.addEventListener("click", function () {
  dropdownMenu.classList.toggle("show");
});

document.addEventListener("click", function (e) {
  if (
    !e.target.matches(".chatbox-message-dropdown, .chatbox-message-dropdown *")
  ) {
    dropdownMenu.classList.remove("show");
  }
});

//Message input
const textarea = document.querySelector(".chatbox-message-input");
const chatboxForm = document.querySelector(".chatbox-message-form");
textarea.addEventListener("input", function () {
  let line = textarea.value.split("\n").length;

  if (textarea.rows < 6 || line < 6) {
    textarea.rows = line;
  }
  if (textarea.rows > 1) {
    chatboxForm.style.alignItems = "flex-end";
  } else {
    chatboxForm.style.alignItems = "center";
  }
});

// CHATBOX MESSAGE
const chatboxMessageWrapper = document.querySelector(
  ".chatbox-message-content"
);
const chatboxNoMessage = document.querySelector(".chatbox-message-no-message");
chatboxForm.addEventListener("submit", function (e) {
  e.preventDefault();

  if (isValid(textarea.value)) {
    writeMessage();
  }
});

function addZero(num) {
  return num < 10 ? "0" + num : num;
}

function writeMessage() {
  const today = new Date();
  let message = `
                  <div class="chatbox-message-item sent">
                    <span class="chatbox-message-item-text">
                        ${textarea.value.trim().replace(/\n/g, "<br>\n")}
                    </span>
                    <span class="chatbox-message-item-time">${addZero(
                      today.getHours()
                    )}:${addZero(today.getMinutes())}</span>
                  </div>
                `;
  chatboxMessageWrapper.insertAdjacentHTML("beforeend", message);
  chatboxForm.style.alignItems = "center";
  textarea.rows = 1;
  textarea.focus();
  textarea.value = "";
  chatboxNoMessage.style.display = "none";
  scrollbottom();
}
// async function sendToBackend(Usertext) {
//   try {
//     const response = await fetch("http://127.0.0.1:8000/api/User_input")
//     method: "POST",
//     headers: {"Content-Type": "application/json"},
//     body: JSON.stringify({
//       input: Usertext,
//       session_id: sessionId
//     })
//   }
// }
// const data

// const Chatbotanswer = Något //

function scrollbottom() {
  chatboxMessageWrapper.scrollTo(0, chatboxMessageWrapper.scrollHeight);
}

function isValid(value) {
  let text = value.replace(/\n/g, "");
  text = text.replace(/\s/g, "");

  return text.length > 0;
}

// (() => {
//   // Nycklar som måste matcha din backend
//   const REQUEST_KEY = "input"; // din endpoint läser Body(..., embed=True) => { "input": "..." }
//   const RESPONSE_KEY_PRIMARY = "answer"; // backend bör svara { "answer": "..." }
//   const RESPONSE_KEY_FALLBACK = "Fråga"; // fallback om du råkar returnera "Fråga"

//   const form = document.getElementById("chat-form");
//   const input = document.getElementById("chatbot_input");
//   const out = document.getElementById("out");
//   // <div class="chatbox-message-bottom">
//   //               <form id="chat-form" class="chatbox-message-form">
//   //                   <textarea id ="chatbot_input" rows="1" placeholder="Type Message..." class="chatbox-message-input"></textarea>
//   //                   <button type="submit" class="chatbox-message-submit"><i class='bx bx-send' ></i></button>

//   //               </form>
//   //           </div>
//   if (!form || !input) {
//     console.error("Hittade inte #chat-form eller #chatbot_input i DOM:en.");
//     return;
//   }

//   form.addEventListener("submit", async (event) => {
//     event.preventDefault();

//     const query = (input.value || "").trim();
//     if (!query) {
//       if (out) out.textContent = "Skriv något först!";
//       return;
//     }

//     if (out) out.textContent = "Bearbetar...";

//     try {
//       const resp = await fetch("/api/ask", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ [REQUEST_KEY]: query }),
//       });

//       console.log("http-status:", resp.status);

//       if (!resp.ok) {
//         if (out) out.textContent = `Serverfel ${resp.status}`;
//         return;
//       }

//       const data = await resp.json();

//       const msg =
//         data?.[RESPONSE_KEY_PRIMARY] ??
//         data?.[RESPONSE_KEY_FALLBACK] ??
//         "(inget svar)";

//       if (out) out.textContent = msg;
//     } catch (err) {
//       if (out) out.textContent = err?.message || "Nätverksfel";
//     } finally {
//       input.value = "";
//       input.focus();
//     }
//   });

//   // Skicka på Enter (Shift+Enter = radbrytning)
//   input.addEventListener("keydown", (e) => {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault();
//       form.requestSubmit();
//     }
//   });
// })();
