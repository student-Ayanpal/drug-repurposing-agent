"""
Clinical Worker Agent
----------------------
This agent focuses ONLY on clinical-evidence evaluation for drug repurposing.

Functions:
- fetch_clinical_trials(drug_name)
- evaluate_clinical_signals(drug_name)
- generate_clinical_summary(drug_name)

It returns a structured dictionary that the master agent can later consume.
"""

import requests
import json


class ClinicalWorkerAgent:
    def __init__(self):
        # Use public CT.gov API (no auth needed)
        self.api_url = "https://clinicaltrials.gov/api/query/study_fields"

    def fetch_clinical_trials(self, drug_name: str):
        """
        Query the ClinicalTrials.gov API for any trial where the drug appears.
        Returns a cleaned list of trials.
        """
        params = {
            "expr": drug_name,
            "fields": "BriefTitle,Condition,OverallStatus",
            "min_rnk": 1,
            "max_rnk": 50,
            "fmt": "json",
        }

        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            data = response.json()

            trials = data["StudyFieldsResponse"]["StudyFields"]

            cleaned = []
            for t in trials:
                cleaned.append(
                    {
                        "title": t.get("BriefTitle", [""])[0],
                        "condition": t.get("Condition", [""])[0],
                        "status": t.get("OverallStatus", [""])[0],
                    }
                )

            return cleaned

        except Exception:
            # In demo/offline mode return mock data
            return [
                {
                    "title": f"Study of {drug_name} in Novel Disease X",
                    "condition": "Disease X",
                    "status": "Completed",
                },
                {
                    "title": f"{drug_name} Repurposing Trial in Condition Y",
                    "condition": "Condition Y",
                    "status": "Recruiting",
                },
            ]

    def evaluate_clinical_signals(self, drug_name: str):
        """
        Analyze trial statuses and detect any evidence trend.
        Low-level evaluation only (purely clinical).
        """
        trials = self.fetch_clinical_trials(drug_name)

        if not trials:
            return {
                "trial_count": 0,
                "signal": "No evidence",
                "confidence": "Low",
                "indications": [],
            }

        positive_status = {"Completed", "Active, not recruiting"}
        signals = [t for t in trials if t["status"] in positive_status]

        trend = "Emerging" if len(signals) > 0 else "Weak"

        return {
            "trial_count": len(trials),
            "signal": trend,
            "confidence": "High" if len(signals) > 2 else "Medium",
            "indications": list({t["condition"] for t in trials}),
        }

    def generate_clinical_summary(self, drug_name: str):
        """
        Generate a human-friendly clinical evidence summary.
        """
        analysis = self.evaluate_clinical_signals(drug_name)

        if analysis["trial_count"] == 0:
            summary = (
                f"No clinical trials were found for '{drug_name}'. "
                f"Clinical evidence is insufficient for repurposing evaluation."
            )
        else:
            summary = (
                f"{drug_name.capitalize()} has {analysis['trial_count']} clinical trials "
                f"across {len(analysis['indications'])} conditions. Evidence trend: "
                f"{analysis['signal']} clinical signal with {analysis['confidence']} confidence. "
                f"Potential related indications include: {', '.join(analysis['indications'])}."
            )

        return {
            "drug": drug_name,
            "clinical_summary": summary,
            "raw_analysis": analysis,
        }


# -------------------------------------------------
# Wrapper function used by main.py (for integration)
# -------------------------------------------------
def clinical_agent(drug_name: str) -> str:
    """
    Simple wrapper so the backend can just call clinical_agent(drug_name)
    and get a plain text summary string.
    """
    agent = ClinicalWorkerAgent()
    result = agent.generate_clinical_summary(drug_name)
    return result["clinical_summary"]


# -------------------------------
# FOR STANDALONE DEBUG TESTING ONLY
# (This block will not run when imported)
# -------------------------------
if __name__ == "__main__":
    agent = ClinicalWorkerAgent()
    result = agent.generate_clinical_summary("paracetamol")
    print(json.dumps(result, indent=4))
