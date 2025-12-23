# Agentic Drug Repurposing Platform

An AI-powered web application that automates early-stage drug repurposing
by combining clinical evidence, patent intelligence, and market insights.

---

## 🚀 Problem Statement
Drug repurposing research is slow, fragmented, and heavily manual,
requiring experts to analyze clinical trials, patents, and market data
across multiple sources.

---

## 💡 Solution
This platform uses a multi-agent AI architecture to:
- Analyze clinical evidence
- Assess patent and IP landscape
- Evaluate market viability
- Generate structured insights and downloadable PDF reports

---

## 🧠 System Architecture
- Clinical Agent – evaluates clinical trial evidence
- Patent Agent – analyzes IP and regulatory landscape
- Market Agent – assesses commercial and market potential
- Master Agent – aggregates insights into a final report

---

## 🛠 Tech Stack
**Backend**
- Python
- FastAPI
- FPDF
- External APIs (ClinicalTrials.gov)

**Frontend**
- HTML, CSS, JavaScript

---
## 📁 Project Structure
```text
drug-repurposing-agent/
│
├── index.html              # Frontend entry point (GitHub Pages)
├── script.js               # Frontend logic (API calls to backend)
├── styles.css              # Frontend styling
│
├── backend/                # FastAPI backend (deployed on Render)
│   ├── __init__.py         # Marks backend as a Python package
│   ├── main.py             # API routes, master agent, PDF generation
│   ├── clinical_agent.py   # Clinical intelligence agent
│   ├── patent_agent.py     # Patent & IP intelligence agent
│   ├── market_agent.py     # Market intelligence agent
│   └── requirements.txt    # Backend dependencies
│
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── README.md               # Project documentation
```

## ▶️ How to Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
---
## Frontend
Open `frontend/index.html` in your browser.

---
## Features
- Drug analysis via AI agents  
- Real-time API-based insights  
- Automated PDF report generation  
- Clean web-based UI  
---
## Team
- **Ayan Pal** – Backend & Project Lead  
- **Soumyadeep Purkayastha** – Frontend & UI  
- **Rupam Mukherjee** – Content & Presentation  
- **Soumitra De** – Data & ML  
- **Pabitra** – Testing & Deployment
---
## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software with proper attribution.  
See the [LICENSE](LICENSE) file for more details.

