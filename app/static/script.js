async function checkHealth() {
    const status = document.getElementById("status");

    try {
        const response = await fetch("/health");
        const data = await response.json();

        if (response.ok) {
            status.textContent = `${data.service}: ${data.status}`;
        } else {
            status.textContent = "Service unavailable";
        }
    } catch (error) {
        status.textContent = "Unable to reach service";
    }
}

checkHealth();