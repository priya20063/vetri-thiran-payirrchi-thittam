async function runTask() {
    const task = document.getElementById("task").value;
    const text = document.getElementById("inputText").value.trim();
    const result = document.getElementById("result");
    const button = document.getElementById("submitBtn");

    if (!text) {
        result.textContent = "Please enter a question, topic or text.";
        return;
    }

    const endpoint = task === "learn" ? "/learn/recommendations" : "/" + task;
    button.disabled = true;
    button.textContent = "Thinking...";
    result.textContent = "EduGenie is preparing your answer...";

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text})
        });

        const data = await response.json();

        if (Array.isArray(data.result)) {
            result.innerHTML = data.result.map((q, i) =>
                `<div class="quiz"><b>${i+1}. ${escapeHtml(q.question)}</b>
                <ol type="A">${q.options.map(o => `<li>${escapeHtml(o)}</li>`).join("")}</ol>
                <b>Answer:</b> ${escapeHtml(q.answer)}</div>`
            ).join("");
        } else {
            result.textContent = data.result;
        }
    } catch (error) {
        result.textContent = "Unable to connect to the backend.";
    } finally {
        button.disabled = false;
        button.textContent = "✨ Ask EduGenie";
    }
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, c => ({
        "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
    }[c]));
}
