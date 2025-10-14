const API_URL = "http://127.0.0.1:5050/api/v1";

/* =======================
   CHARGER LES ÉLIGIBLES
======================= */
async function loadEligible() {
  const res = await fetch(`${API_URL}/eligible`);
  const data = await res.json();
  const tbody = document.querySelector("#eligibleTable tbody");
  tbody.innerHTML = "";

  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);

  // On garde seulement les habitants arrivés il y a ≥ 1 an
  const filtered = data.filter(item => {
    const arrival = new Date(item.resident.date_arrivee);
    return arrival <= oneYearAgo;
  });

  filtered.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${item.resident.prenom}</td>
      <td>${item.resident.age}</td>
      <td>${item.resident.date_arrivee}</td>
      <td>${item.cadeau_associe.map(c => c.nom).join(", ")}</td>
    `;
    tbody.appendChild(tr);
  });

  if (filtered.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="4">Aucun habitant éligible pour le moment 🎂</td>`;
    tbody.appendChild(tr);
  }

  document.querySelector("#eligibleSection").classList.remove("hidden");
}

/* =======================
   AFFICHER / MASQUER LES ÉLIGIBLES
======================= */
const eligibleBtn = document.querySelector("#loadEligible");
const eligibleSection = document.querySelector("#eligibleSection");

let eligibleLoaded = false; // savoir si les données ont déjà été chargées

eligibleBtn.addEventListener("click", async () => {
  const isHidden = eligibleSection.classList.contains("hidden");

  if (isHidden) {
    // Si la section est masquée → on charge (une seule fois)
    if (!eligibleLoaded) {
      await loadEligible();
      eligibleLoaded = true;
    }
    eligibleSection.classList.remove("hidden");
    eligibleBtn.textContent = "🫥 Masquer les habitants éligibles";
  } else {
    // Si la section est visible → on la masque
    eligibleSection.classList.add("hidden");
    eligibleBtn.textContent = "👀 Voir les habitants éligibles";
  }
});



/* =======================
   AJOUTER UN HABITANT
======================= */
document.querySelector("#addResidentForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const newResident = {
    id: parseInt(document.querySelector("#id").value),
    prenom: document.querySelector("#prenom").value,
    age: parseInt(document.querySelector("#age").value),
    date_arrivee: document.querySelector("#date_arrivee").value
  };

  try {
    const res = await fetch(`${API_URL}/residents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newResident)
    });

    if (!res.ok) throw new Error("Erreur d’ajout du résident");

    showToast(`${newResident.prenom} ajouté !`, "success");
    e.target.reset();

// 🔹 On recharge seulement si la section est visible
if (!eligibleSection.classList.contains("hidden")) {
  await loadEligible();
}

  } catch (err) {
    showToast("Impossible d’ajouter le résident", "error");
    console.error(err);
  }
});

/* =======================
   LANCER LES ATTRIBUTIONS
======================= */
document.querySelector("#doAttribution").addEventListener("click", async () => {
  try {
    const res = await fetch(`${API_URL}/attributions`, { method: "POST" });
    const data = await res.json();
    const emailsDiv = document.querySelector("#emails");

    // On vide le placeholder s’il existe
    emailsDiv.querySelector(".placeholder")?.remove();

    if (emailsDiv.innerHTML.trim() === "") {
      data.forEach(a => {
        const mail = document.createElement("div");
        mail.classList.add("email");
        mail.innerHTML = `
          <strong>📩 À : ${a.resident.prenom}@ville.fr</strong><br>
          Bonjour ${a.resident.prenom},<br>
          🎁 Félicitations ! Vous venez de recevoir le cadeau suivant :
          <strong>${a.cadeau_associe.nom}</strong>.<br>
          Date d’attribution : ${a.date_attribution}
        `;
        emailsDiv.appendChild(mail);
      });

      if (data.length > 0) {
        const summary = document.createElement("div");
        summary.classList.add("email");
        summary.innerHTML = `
          <strong>📧 Service cadeaux - Récapitulatif</strong><br>
          ${data.length} cadeaux attribués aujourd’hui :
          <ul>${data.map(a => `<li>${a.resident.prenom} → ${a.cadeau_associe.nom}</li>`).join("")}</ul>
        `;
        emailsDiv.appendChild(summary);
      } else {
        // Aucun mail créé → on remet le placeholder
        emailsDiv.innerHTML = `<p class="placeholder">Aucun mail n’a encore été envoyé aujourd’hui.</p>`;
      }

      showToast(`${data.length} attributions réalisées et mails simulés !`, "success");
    } else {
      showToast("Les attributions ont déjà été faites aujourd’hui", "info");
    }


    if (!eligibleSection.classList.contains("hidden")) {
      await loadEligible();
    }

  } catch (err) {
    showToast("Erreur lors de l’attribution", "error");
    console.error(err);
  }
});

/* =======================
   RÉINITIALISER LES ATTRIBUTIONS
======================= */
const resetButton = document.querySelector("#resetAttributions");
if (resetButton) {
  resetButton.addEventListener("click", async () => {
    try {
      await fetch(`${API_URL}/reset`, { method: "POST" });

      const emailsDiv = document.querySelector("#emails");
      emailsDiv.innerHTML = `
        <p class="placeholder">Aucun mail n’a encore été envoyé aujourd’hui.</p>
      `;

      showToast("Attributions réinitialisées !", "info");
    } catch (err) {
      showToast("Erreur de réinitialisation", "error");
    }
  });
}


/* =======================
   DATE AUTOMATIQUE DANS LE HEADER
======================= */
const dateSpan = document.querySelector(".date");
if (dateSpan) {
  const today = new Date();
  const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
  dateSpan.textContent = today.toLocaleDateString("fr-FR", options);
}

/* === NOTIFICATIONS STYLÉES === */
function showToast(message, type = "success") {
  const container =
    document.querySelector(".toast-container") ||
    Object.assign(document.body.appendChild(document.createElement("div")), {
      className: "toast-container"
    });

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${
      type === "success"
        ? "✅"
        : type === "error"
        ? "❌"
        : "ℹ️"
    }</span>
    <span class="toast-msg">${message}</span>
  `;

  container.appendChild(toast);

  // Animation d’apparition
  setTimeout(() => toast.classList.add("show"), 50);

  // Disparition automatique
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 500);
  }, 3500);
}

/* === Particules d'arrière-plan (style mairie amélioré) === */
window.addEventListener("load", () => {
  const canvas = document.getElementById("backgroundCanvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let particles = [];
  const num = 60; // plus de particules

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener("resize", resize);
  resize();

  // couleurs plus visibles et tailles plus variées
  const colors = [
    "rgba(255,255,255,0.9)",
    "rgba(31,60,136,0.7)",
    "rgba(46,75,139,0.6)",
    "rgba(31,60,136,0.4)"
  ];

  for (let i = 0; i < num; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 3 + 1.5,
      dx: (Math.random() - 0.5) * 0.8,
      dy: (Math.random() - 0.5) * 0.8,
      color: colors[Math.floor(Math.random() * colors.length)]
    });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // légère couche sombre pour donner de la profondeur
    ctx.fillStyle = "rgba(0, 0, 30, 0.03)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 10;
      ctx.fill();

      // déplacement
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
    });

    ctx.shadowBlur = 0;
    requestAnimationFrame(draw);
  }

  draw();
});

