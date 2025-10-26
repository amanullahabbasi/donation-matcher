// =======================
// Configure your backend URL here
// =======================
const API_BASE = localStorage.getItem("API_BASE") || "https://donation-matcher.onrender.com"; 

function setApiBase(url){
  localStorage.setItem("API_BASE", url);
  alert("Backend URL saved: " + url);
}

async function postJSON(path, payload){
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return res.json();
}

async function getJSON(path){
  const res = await fetch(`${API_BASE}${path}`);
  return res.json();
}

async function del(path){
  const res = await fetch(`${API_BASE}${path}`, { method: "DELETE" });
  return res.json();
}

// Forms
const victimForm = document.getElementById("victimForm");
const donorForm = document.getElementById("donorForm");
const victimsOut = document.getElementById("victimsOut");
const donorsOut = document.getElementById("donorsOut");
const matchesOut = document.getElementById("matchesOut");

victimForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(victimForm);
  const payload = Object.fromEntries(form.entries());
  payload.income = Number(payload.income || 0);
  payload.amount_needed = Number(payload.amount_needed || 0);
  await postJSON("/api/victims", payload);
  await loadVictims();
  alert("✅ Person added successfully!");
  victimForm.reset();
});

donorForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = new FormData(donorForm);
  const payload = Object.fromEntries(form.entries());
  payload.donation_amount = Number(payload.donation_amount || 0);
  await postJSON("/api/donors", payload);
  await loadDonors();
  alert("✅ Donor added successfully!");
  donorForm.reset();
});

// Buttons
document.getElementById("btnLoadVictims").addEventListener("click", loadVictims);
document.getElementById("btnLoadDonors").addEventListener("click", loadDonors);
document.getElementById("btnCompute").addEventListener("click", computeMatches);
document.getElementById("btnReset").addEventListener("click", async () => {
  if(confirm("This will delete all demo data on the server.")){
    await del("/api/reset");
    victimsOut.textContent = "";
    donorsOut.textContent = "";
    matchesOut.textContent = "";
  }
});

// ========== DISPLAY FUNCTIONS ==========

// Show victims nicely
async function loadVictims(){
  const data = await getJSON("/api/victims");
  if (!data.length) {
    victimsOut.innerHTML = "<p>No victims yet.</p>";
    return;
  }
  let html = "";
  data.forEach(v => {
    html += `
      <div class="card-entry">
        <p>🧍‍♂️ <strong>${v.name}</strong> from <strong>${v.location}</strong> needs <strong>${v.need_type}</strong> worth ₨${v.amount_needed.toLocaleString()} (Urgency: ${v.urgency})</p>
        <p>Income: ₨${v.income.toLocaleString()} | Owns home: ${v.has_home ? "Yes" : "No"}</p>
      </div>
      <hr>
    `;
  });
  victimsOut.innerHTML = html;
}

// Show donors nicely
async function loadDonors(){
  const data = await getJSON("/api/donors");
  if (!data.length) {
    donorsOut.innerHTML = "<p>No donors yet.</p>";
    return;
  }
  let html = "";
  data.forEach(d => {
    html += `
      <div class="card-entry">
        <p>💙 <strong>${d.name}</strong> from <strong>${d.location}</strong> is donating <strong>${d.resource_type}</strong> worth ₨${d.donation_amount.toLocaleString()}</p>
      </div>
      <hr>
    `;
  });
  donorsOut.innerHTML = html;
}

// Show matches nicely
async function computeMatches() {
  const data = await getJSON("/api/matches");
  if (!data.length) {
    matchesOut.innerHTML = "<p>No matches found yet.</p>";
    return;
  }
  let html = "";
  data.forEach(match => {
    const v = match.victim;
    const d = match.donor;
    html += `
      <div class="match-card">
        <p>🤝 <strong>${d.name}</strong> from <strong>${d.location}</strong> matched with <strong>${v.name}</strong> from <strong>${v.location}</strong></p>
        <p>💙 ${d.name} donated <strong>${d.resource_type}</strong> worth ₨${d.donation_amount.toLocaleString()}</p>
        <p>🧍‍♂️ ${v.name} needed <strong>${v.need_type}</strong> worth ₨${v.amount_needed.toLocaleString()} (Urgency: ${v.urgency})</p>
      </div>
      <hr>
    `;
  });
  matchesOut.innerHTML = html;
}

// Quick tip: change backend URL from browser console if needed:
// setApiBase("https://your-backend.onrender.com");
