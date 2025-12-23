# patent_agent.py

from datetime import datetime

def patent_agent(drug_name: str) -> dict:
    """
    Advanced Patent & IP Intelligence Agent (Real-World Style)

    This agent simulates how pharma IP teams analyze
    patent landscape for drug repurposing.
    """

    current_year = datetime.now().year

    # -------------------------------
    # 1) CORE COMPOSITION PATENTS
    # -------------------------------
    composition_status = (
        f"Primary composition-of-matter patents for {drug_name} "
        "are largely expired or approaching expiry in major markets "
        "(US/EU), reducing barriers for generic manufacturing."
    )

    # -------------------------------
    # 2) SECONDARY / LAYERED PATENTS
    # -------------------------------
    secondary_patents = (
        "Secondary patents may still exist around:\n"
        "- Specific crystal polymorphs or salt forms\n"
        "- Modified-release or targeted delivery formulations\n"
        "- Improved manufacturing or purification processes\n"
        "However, these are typically narrower in scope and "
        "can often be designed around."
    )

    # -------------------------------
    # 3) FREEDOM-TO-OPERATE (FTO)
    # -------------------------------
    fto_analysis = (
        "Freedom-to-operate appears favorable for a new medical use, "
        "provided the repurposed indication does not rely on "
        "protected formulations or active combination products. "
        "A focused FTO search would still be required before commercialization."
    )

    # -------------------------------
    # 4) REPURPOSING IP OPPORTUNITIES
    # -------------------------------
    repurposing_opportunities = (
        "Strong IP opportunities exist via:\n"
        "- New therapeutic indication patents (method-of-use)\n"
        "- Patient subpopulation claims (biomarker-driven therapy)\n"
        "- Novel dose or dosing-regimen patents\n"
        "- Combination therapy patents with complementary agents\n"
        "These routes are commonly used in successful repurposing programs."
    )

    # -------------------------------
    # 5) REGULATORY EXCLUSIVITY
    # -------------------------------
    regulatory_exclusivity = (
        "Beyond patents, regulatory exclusivity pathways such as "
        "Orphan Drug Designation (7 years US / 10 years EU), "
        "data exclusivity, or pediatric extensions may provide "
        "meaningful market protection even in the absence of "
        "strong composition patents."
    )

    # -------------------------------
    # FINAL STRATEGIC ASSESSMENT
    # -------------------------------
    strategic_assessment = (
        f"From a patent strategy perspective, {drug_name} represents a "
        "low-to-moderate IP risk candidate with strong repurposing potential. "
        "Success will depend on selecting an indication with high unmet need "
        "and executing a focused IP and regulatory exclusivity strategy early."
    )

    return {
        "composition_patent_status": composition_status,
        "secondary_patent_landscape": secondary_patents,
        "freedom_to_operate": fto_analysis,
        "repurposing_ip_opportunities": repurposing_opportunities,
        "regulatory_exclusivity_options": regulatory_exclusivity,
        "strategic_patent_assessment": strategic_assessment,
        "analysis_year": current_year,
    }


# -------------------------------------------------
# Wrapper used by main.py to get ONE summary string
# -------------------------------------------------
def patent_agent_summary(drug_name: str) -> str:
    """
    Call patent_agent(drug_name) and flatten its structured output
    into a single human-readable patent/IP summary string.
    """
    data = patent_agent(drug_name)

    parts = [
        data["composition_patent_status"],
        "",
        data["secondary_patent_landscape"],
        "",
        data["freedom_to_operate"],
        "",
        data["repurposing_ip_opportunities"],
        "",
        data["regulatory_exclusivity_options"],
        "",
        data["strategic_patent_assessment"],
    ]

    return "\n".join(parts)
