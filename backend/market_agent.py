# agents.py

from datetime import datetime

def market_agent(drug_name: str) -> dict:
    """
    Advanced Market Intelligence Agent (Real-World Style)

    This agent simulates how pharma commercial and strategy teams
    evaluate market viability for drug repurposing.
    """

    current_year = datetime.now().year

    # -------------------------------
    # 1) CURRENT MARKET LANDSCAPE
    # -------------------------------
    current_market = (
        f"The current market for {drug_name} in its primary indication "
        "is mature and highly competitive, with multiple generic entrants "
        "and strong price erosion across both developed and emerging markets."
    )

    # -------------------------------
    # 2) UNMET MEDICAL NEED
    # -------------------------------
    unmet_need = (
        "Despite therapeutic alternatives, significant unmet medical need persists "
        "in patient subpopulations such as treatment-resistant cases, "
        "multi-morbid patients, and regions with limited access to advanced therapies."
    )

    # -------------------------------
    # 3) REPURPOSING MARKET OPPORTUNITY
    # -------------------------------
    repurposing_opportunity = (
        "Repurposing into a differentiated indication presents an opportunity to "
        "access higher-value segments, particularly in chronic, rare, or progressive "
        "disease areas where existing treatment options are limited or suboptimal."
    )

    # -------------------------------
    # 4) COMPETITIVE LANDSCAPE
    # -------------------------------
    competitive_landscape = (
        "The competitive landscape for the repurposed indication is characterized by:\n"
        "- Limited number of approved therapies\n"
        "- High discontinuation rates due to safety or tolerability issues\n"
        "- Emerging biotech entrants with early-stage assets\n"
        "This environment favors fast-to-market repurposed assets with known safety profiles."
    )

    # -------------------------------
    # 5) PRICING & REIMBURSEMENT
    # -------------------------------
    pricing_reimbursement = (
        "Pricing potential is favorable if the repurposed product demonstrates "
        "clear clinical differentiation and health-economic value. "
        "Payers are more likely to reimburse premium pricing in settings "
        "with high disease burden or lack of effective alternatives."
    )

    # -------------------------------
    # 6) COMMERCIALIZATION STRATEGY
    # -------------------------------
    commercialization_strategy = (
        "An optimal commercialization strategy would focus on:\n"
        "- Targeted specialist prescriber segments\n"
        "- Clear patient stratification criteria\n"
        "- Evidence generation through real-world data and pragmatic trials\n"
        "This approach can accelerate uptake while controlling commercial risk."
    )

    # -------------------------------
    # FINAL MARKET ASSESSMENT
    # -------------------------------
    strategic_market_assessment = (
        f"From a commercial perspective, repurposing {drug_name} represents "
        "a moderate-risk, high-potential opportunity. Strategic success will depend "
        "on selecting an indication with strong unmet need, limited competition, "
        "and supportive reimbursement dynamics."
    )

    return {
        "current_market_landscape": current_market,
        "unmet_medical_need": unmet_need,
        "repurposing_market_opportunity": repurposing_opportunity,
        "competitive_landscape": competitive_landscape,
        "pricing_and_reimbursement": pricing_reimbursement,
        "commercialization_strategy": commercialization_strategy,
        "strategic_market_assessment": strategic_market_assessment,
        "analysis_year": current_year,
    }


# -------------------------------------------------
# Wrapper used by main.py to get ONE summary string
# -------------------------------------------------
def market_agent_summary(drug_name: str) -> str:
    """
    Call market_agent(drug_name) and flatten its structured output
    into a single human-readable market summary string.
    """
    data = market_agent(drug_name)

    parts = [
        data["current_market_landscape"],
        "",
        data["unmet_medical_need"],
        "",
        data["repurposing_market_opportunity"],
        "",
        data["competitive_landscape"],
        "",
        data["pricing_and_reimbursement"],
        "",
        data["commercialization_strategy"],
        "",
        data["strategic_market_assessment"],
    ]

    return "\n".join(parts)
