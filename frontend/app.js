// frontend/app.js
const BASE = "http://127.0.0.1:8000";
const analyzeBtn = document.getElementById("analyze-btn");
const pdfBtn = document.getElementById("pdf-btn");
const input = document.getElementById("drug-input");
const statusDiv = document.getElementById("status");
const reportContainer = document.getElementById("report-container");
const resultPre = document.getElementById("result");

function setStatus(text, cls) {
  statusDiv.textContent = text || "";
  statusDiv.className = cls || "";
}

analyzeBtn.addEventListener("click", async () => {
  const drug = input.value.trim();
  if (!drug) {
    setStatus("⚠️ Please enter a drug name.", "error");
    return;
  }
  setStatus(`⏳ Running analysis for "${drug}"...`);
  reportContainer.style.display = "none";
  resultPre.textContent = "Working...";

  try {
    const resp = await fetch(`${BASE}/analyze-drug?drug_name=${encodeURIComponent(drug)}`, {
      method: "POST"
    });
    if (!resp.ok) throw new Error(`${resp.status}`);
    const data = await resp.json();

    // Render result
    resultPre.textContent =
`🔬 Drug: ${data.drug}

⭐ Score:
${data.score}

1) Clinical Rationale & Trials:
${data.clinical_summary}

2) Patent & Regulatory Landscape:
${data.patent_summary}

3) Market Opportunity Assessment:
${data.market_summary}

4) Final Recommendation:
${data.final_recommendation}
`;

    setStatus("✅ Analysis complete.");
    reportContainer.style.display = "block";
  } catch (err) {
    console.error(err);
    setStatus("❌ Error running analysis. Check backend.", "error");
    resultPre.textContent = "";
  }
});

pdfBtn.addEventListener("click", async () => {
  const drug = input.value.trim();
  if (!drug) {
    alert("Please run analysis first.");
    return;
  }
  setStatus("⏳ Generating PDF...");
  try {
    const resp = await fetch(`${BASE}/generate-pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ drug_name: drug })
    });
    if (!resp.ok) throw new Error(`Server returned ${resp.status}`);
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${drug}_repurposing_report.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setStatus("✅ PDF downloaded.");
  } catch (err) {
    console.error(err);
    setStatus("❌ PDF generation failed.", "error");
  }
});
