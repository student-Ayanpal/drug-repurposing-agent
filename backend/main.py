# backend/main.py

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fpdf import FPDF
from io import BytesIO
import datetime
import re

# 🔗 Import your real agent functions
from .clinical_agent import clinical_agent
from .patent_agent import patent_agent_summary
from .market_agent import market_agent_summary


app = FastAPI(title="Agentic Repurposing Engine (Prototype)")

# -----------------------
# CORS for local frontend
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Sanitize all text before FPDF
# -----------------------
def sanitize(text: str) -> str:
    if not isinstance(text, str):
        return text

    # Remove emojis / unsupported pictographs
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U0000FE00-\U0000FE0F"
        u"\U0001F900-\U0001F9FF"
        u"\U0001FA70-\U0001FAFF"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub("", text)

    # Replace unicode punctuation unsupported by Latin‑1
    replacements = {
        "—": "-",
        "–": "-",
        "…": "...",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "-",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Strip remaining non-latin1 characters (FPDF uses latin-1)
    text = text.encode("latin-1", "ignore").decode("latin-1")
    return text

# -----------------------
# Health check endpoint
# -----------------------
@app.get("/")
def root():
    return {"message": "Backend is running!"}

# -----------------------
# Master Agent (uses REAL agents)
# -----------------------
def master_agent(drug_name: str) -> dict:
    # Always sanitize input first
    drug_name = sanitize(drug_name)

    # Call your real agents (each returns a string)
    clinical = sanitize(clinical_agent(drug_name))
    patent = sanitize(patent_agent_summary(drug_name))
    market = sanitize(market_agent_summary(drug_name))

    # Static score for now – later you can compute via LLM
    score = sanitize("7.8 / 10 - High repurposing potential")

    recommendation = sanitize(
        f"{drug_name} seems suitable for repurposing into 1-2 high-value adjacent indications.\n"
        "Recommended next steps:\n"
        "1) Prioritize 1 niche indication.\n"
        "2) Design differentiation (dose / formulation / combination).\n"
        "3) Prepare targeted preclinical / clinical plan + IP filing."
    )

    return {
        "drug": drug_name,
        "score": score,
        "clinical_summary": clinical,
        "patent_summary": patent,
        "market_summary": market,
        "final_recommendation": recommendation,
    }

# -----------------------
# /analyze-drug endpoint
# -----------------------
@app.post("/analyze-drug")
def analyze_drug(drug_name: str = Query(..., description="Generic drug name to analyze")):
    """
    Returns the structured analysis JSON built from your 3 worker agents.
    """
    report = master_agent(drug_name)
    return JSONResponse(content=report)

# -----------------------
# PDF BUILDER — ALWAYS USE dest="S"
# -----------------------
def build_pdf_from_report(report: dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(
        0,
        10,
        sanitize(f"Drug Repurposing Report - {report['drug']}"),
        ln=True,
        align="C",
    )
    pdf.ln(6)

    pdf.set_font("Arial", size=11)
    pdf.cell(
        0,
        8,
        sanitize(
            f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ),
        ln=True,
    )
    pdf.ln(6)

    # fixed effective width between margins
    effective_width = pdf.w - 2 * pdf.l_margin

    def write_section(title: str, content: str):
        # heading
        pdf.set_font("Arial", 'B', 12)
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 8, sanitize(title), ln=True)

        # body
        pdf.set_font("Arial", size=11)
        safe = sanitize(content)

        # 🔒 hard cap to avoid insanely long content in one section
        max_len = 4000
        if len(safe) > max_len:
            safe = safe[:max_len] + "\n...[truncated for PDF]"

        for line in safe.split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(4)
                continue
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(effective_width, 7, line)

        pdf.ln(4)

    write_section("Repurposing Score", report["score"])
    write_section("1) Clinical Rationale & Trials", report["clinical_summary"])
    write_section("2) Patent & Regulatory Landscape", report["patent_summary"])
    write_section("3) Market Opportunity Assessment", report["market_summary"])
    write_section("4) Final Recommendation", report["final_recommendation"])

    # FPDF returns bytearray/bytes with dest="S" → ensure bytes
    raw = pdf.output(dest="S")
    pdf_bytes = bytes(raw)

    return pdf_bytes


# -----------------------
# /generate-pdf endpoint
# -----------------------
@app.post("/generate-pdf")
def generate_pdf(payload: dict = Body(...)):
    """
    POST /generate-pdf
    Body: { "drug_name": "aspirin" }

    Returns: application/pdf stream (download).
    """
    drug_name = payload.get("drug_name")
    if not drug_name:
        return JSONResponse(status_code=400, content={"error": "Missing drug_name"})

    report = master_agent(drug_name)
    pdf_bytes = build_pdf_from_report(report)

    filename = f"{report['drug']}_repurposing_report.pdf"

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
