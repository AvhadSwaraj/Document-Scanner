document.addEventListener("DOMContentLoaded", async function () {
    await fetchUserProfile(); // ✅ Fetch user credits on page load
});

// ✅ Fetch user profile
async function fetchUserProfile() {
    const response = await fetch("/profile/details");
    const data = await response.json();

    if (response.ok) {
        document.getElementById("username").innerText = data.username;
        document.getElementById("credits").innerText = data.credits;
    } else {
        window.location.href = "index.html"; // Redirect to login if not logged in
    }
}

// ✅ Upload Document
document.getElementById("upload-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const fileInput = document.getElementById("document");
    if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("document", fileInput.files[0]);

    const response = await fetch("/profile/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    if (response.ok) {
        alert("File uploaded successfully!");
        document.getElementById("credits").innerText = data.credits; // ✅ Update credits
    } else {
        alert(data.error);
    }
});

// ✅ View Uploaded Documents
document.getElementById("view-documents").addEventListener("click", async function () {
    const response = await fetch("/profile/documents");
    const data = await response.json();

    if (response.ok) {
        let docList = "Uploaded Documents:\n" + data.documents.join("\n");
        alert(docList);
    } else {
        alert("Error fetching documents.");
    }
});

// ✅ Logout
document.getElementById("logout-btn").addEventListener("click", async function () {
    await fetch("/auth/logout", { method: "POST" });
    window.location.href = "index.html";
});
