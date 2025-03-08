async function fetchDetails() {
    const flatNumber = document.getElementById("flatInput").value.trim();

    if (!flatNumber) {
        alert("Please enter your flat number!");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/get_user/${flatNumber}`);
        if (!response.ok) {
            throw new Error("Flat number not found!");
        }

        const data = await response.json();

        document.getElementById("name").innerText = `Name: ${data.name}`;
        document.getElementById("totalMembers").innerText = data.totalMembers;
        document.getElementById("remainingMembers").innerText = data.remainingMembers;
        document.getElementById("qrCode").src = data.qrCode;

        document.getElementById("details").classList.remove("hidden");
    } catch (error) {
        alert(error.message);
    }
}