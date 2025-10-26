# 🌍 Donation Matcher — AI-Powered Disaster Relief Platform

**Donation Matcher** is an AI-powered web platform that connects **donors** with **people in need** during natural disasters such as floods and earthquakes.  
It uses a **predictive scoring model** to prioritize and match victims based on their **income, assets, urgency, and required resources**, ensuring fair and transparent donation distribution.

---

## 🚀 Live Demo

- **Frontend (Web UI):** [https://donation-matcher-1.onrender.com](https://donation-matcher-1.onrender.com)  
- **Backend (Flask API):** [https://donation-matcher.onrender.com](https://donation-matcher.onrender.com)

---

## 💡 Project Overview

This project demonstrates how **AI and data-based prediction** can make humanitarian aid smarter, faster, and more effective.  
Donors input their available donation amount and resource type, while victims share their needs, income, and urgency level.  
The system uses a simple but powerful algorithm to calculate a **priority score**, automatically matching donors and victims.

Example output:
> “Ushba’s donation matched Amanullah Asim’s food need.”

---

## 🧩 Features

- 🧮 Predictive matching based on income, urgency, and resource type  
- 💰 Real-time donor–victim matching  
- 🌐 Fully hosted using Render (Flask backend + static frontend)  
- 🔒 CORS-enabled secure API for communication  
- 🧾 REST endpoints with clean JSON responses  
- 🧠 Easily extendable for machine learning integration  

---

## ⚙️ Tech Stack

| Layer | Technology |
|--------|-------------|
| **Backend** | Python (Flask) |
| **Frontend** | HTML, CSS, JavaScript |
| **Hosting** | Render (Free Tier) |
| **Data** | In-memory JSON storage (extendable to database) |
| **AI Logic** | Simple rule-based scoring system |

---

## 🧠 How It Works

1. **Victims** submit info such as name, income, has_home, amount_needed, and urgency.  
2. **Donors** specify donation amount and resource type.  
3. The backend calculates a **need score** based on urgency and financial status.  
4. The app matches donors and victims, producing readable results:
   > “Ushba’s donation matched Amanullah Asim’s food need.”

---

☁️ Deployment

Backend: Flask API hosted on Render → https://donation-matcher.onrender.com

Frontend: Static HTML/CSS/JS hosted on Render → https://donation-matcher-1.onrender.com

Both communicate through secure fetch() API calls using CORS.

🌱 Future Enhancements

🤖 Integrate AI/ML regression models for smarter need prediction

💾 Add persistent database (Firebase or PostgreSQL)

🧾 Include user authentication for donors and victims

📊 Build an admin dashboard to visualize donation flow

📱 Add mobile-responsive design