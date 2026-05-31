async function translateText() {

    const text =
        document.getElementById("inputText").value;

    const targetLanguage =
        document.getElementById("targetLang").value;

    const response = await fetch("/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text,
            targetLanguage
        })
    });

    const data = await response.json();

    document.getElementById("output").innerText =
        data.translatedText;
}

function copyText() {

    const text =
        document.getElementById("output").innerText;

    navigator.clipboard.writeText(text);

    alert("Copied Successfully");
}

function speakText() {

    const text =
        document.getElementById("output").innerText;

    const speech =
        new SpeechSynthesisUtterance(text);

    speechSynthesis.speak(speech);
}