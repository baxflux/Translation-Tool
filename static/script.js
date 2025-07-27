async function translate() {
    const input = document.getElementById('inputText').value;
    if (!input.trim()) {
        document.getElementById('outputText').innerText = 'Error: Please enter text';
        return;
    }
    const response = await fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texts: [input] })
    });
    const result = await response.json();
    document.getElementById('outputText').innerText = 
        result.error ? `Error: ${result.error}` : `Result: ${result.translated[0]}`;
}