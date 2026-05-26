// ================= TYPING EFFECT =================

let text = "Data Science Student";
let i = 0;

function typing(){
  if(i < text.length){
    document.getElementById("typing").innerHTML += text.charAt(i);
    i++;
    setTimeout(typing, 100);
  }
}

typing();


// ================= DARK MODE =================

let darkBtn = document.getElementById("darkModeBtn");

darkBtn.onclick = function(){
  if(document.body.classList.contains("dark-mode")){
    document.body.classList.remove("dark-mode");
    document.body.style.background = "";
    document.body.style.color = "";
    darkBtn.textContent = "Dark Mode";
  } else {
    document.body.classList.add("dark-mode");
    document.body.style.background = "#081b29";
    document.body.style.color = "white";
    darkBtn.textContent = "Light Mode";
  }
}


// ================= CONTACT FORM API =================

document.getElementById("contactForm").addEventListener("submit", async function(e){

  e.preventDefault();

  const name    = document.getElementById("contactName").value.trim();
  const email   = document.getElementById("contactEmail").value.trim();
  const message = document.getElementById("contactMessage").value.trim();
  const responseDiv = document.getElementById("responseMessage");

  responseDiv.style.color = "blue";
  responseDiv.innerHTML = "Sending...";

  try {
    const response = await fetch(`${window.API_BASE}/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message })
    });

    const data = await response.json();

    if(response.ok){
      responseDiv.style.color = "green";
      responseDiv.innerHTML = "✓ Message sent successfully!";
      document.getElementById("contactForm").reset();
    } else {
      responseDiv.style.color = "red";
      responseDiv.innerHTML = "✗ Error: " + (data.error || "Unknown error");
    }
  } catch(error){
    responseDiv.style.color = "red";
    responseDiv.innerHTML = "✗ Connection error. Make sure the backend server is running on port 5000.";
    console.error("Contact form error:", error);
  }

});
