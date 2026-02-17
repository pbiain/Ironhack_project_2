"""
Main application entry point.
1. Configures the selected LLM.
2. Processes markdown files.
3. Takes user input for Template selection, topic, and goals.
4. Generates content using the chosen engine.
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Project modules
from llm_integration import LLMFactory 
from knowledge_base import (
    build_brand_knowledge,
    build_product_knowledge,
    build_competitor_knowledge,
    build_industry_trends_knowledge,
    build_market_overview_knowledge,
)
import templates  # Import the whole module to access all templates

# Resolve project paths
BASE_DIR = Path(__file__).resolve().parent.parent

def main() -> None:
    """Main orchestration function."""
    load_dotenv()
    
    print("\n" + "="*45)
    print("🚀 AI CONTENT CREATOR - TEMPLATE MODE")
    print("="*45)
    
    # -------------------------------------------------
    # 1️⃣ PROVIDER SELECTION
    # -------------------------------------------------
    print("\n--- Step 1: Provider ---")
    print("[1] OpenAI (GPT-4o-mini)")
    print("[2] Anthropic (Claude 3.5 Sonnet)")
    choice = input("Select provider (1 or 2): ").strip()
    provider_key = "openai" if choice == "1" else "anthropic"
    
    try:
        llm = LLMFactory.get_provider(provider_key)
        print(f"✅ Using {provider_key.upper()}.")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # -------------------------------------------------
    # 2️⃣ TEMPLATE SELECTION
    # -------------------------------------------------
    print("\n--- Step 2: Strategy Template ---")
    print("[1] Brand Authority (Focus: Identity & Flexibility)")
    print("[2] Industry Problem-Solution (Focus: Data & Obsolescence)")
    print("[3] Hybrid Strategic (Focus: Ecosystem & Community)")
    t_choice = input("Select template (1, 2, or 3): ").strip()

    # -------------------------------------------------
    # 3️⃣ DATA PROCESSING
    # -------------------------------------------------
    print("\nProcessing knowledge base documents...")
    brand_path = BASE_DIR / "knowledge_base/primary/brand_guidelines.md"
    product_path = BASE_DIR / "knowledge_base/primary/product_specs.md"
    market_path = BASE_DIR / "knowledge_base/secondary/market_trends.md"
    competitor_path = BASE_DIR / "knowledge_base/secondary/competitor_analysis.md"

    brand_data = build_brand_knowledge(str(brand_path))
    product_data = build_product_knowledge(str(product_path))
    market_overview_data = build_market_overview_knowledge(str(market_path))
    industry_data = build_industry_trends_knowledge(str(competitor_path))
    competitor_data = build_competitor_knowledge(str(competitor_path))

    # -------------------------------------------------
    # 4️⃣ DYNAMIC USER INPUTS
    # -------------------------------------------------
    print("\n--- Step 3: Customization ---")
    topic_in = input("Enter topic (Leave blank for default): ").strip()
    topic = topic_in if topic_in else "Why Flexible Fitness Infrastructure Is Replacing Traditional Gyms"

    obj_in = input("Enter objective (Leave blank for default): ").strip()
    objective = obj_in if obj_in else "Reinforce infrastructure positioning"

    kpi_in = input("Enter KPI (Leave blank for default): ").strip()
    kpi = kpi_in if kpi_in else "Increase CTR by 15%"

    # -------------------------------------------------
    # 5️⃣ PROMPT PREPARATION (TEMPLATE MAPPING)
    # -------------------------------------------------
    if t_choice == "1":
        prompt_text = templates.blog_post_brand_authority_engine(
            brand_voice_section=brand_data.get("brand_voice", ""),
            product_specs_section=product_data.get("product_overview", ""),
            past_success_pattern_section="Berlin expansion framework", # Standard fallback
            operational_objective=objective,
            kpi_target=kpi,
            topic=topic
        )
    elif t_choice == "2":
        prompt_text = templates.blog_post_industry_problem_solution_engine(
            market_data_section=market_overview_data.get("industry_overview", ""),
            industry_trends_section=industry_data.get("macro_trends", ""),
            competitor_snapshot=competitor_data.get("competitive_overview", ""),
            brand_positioning_summary=brand_data.get("brand_voice", ""),
            operational_objective=objective,
            kpi_target=kpi,
            topic=topic
        )
    else: # Default to Hybrid (Choice 3)
        prompt_text = templates.blog_post_hybrid_strategic_engine(
            brand_voice_section=brand_data.get("brand_voice", ""),
            product_specs_section=product_data.get("product_overview", ""),
            partner_metrics_snapshot=product_data.get("customer_results", ""),
            market_data_snapshot=market_overview_data.get("industry_overview", ""),
            industry_trends_snapshot=industry_data.get("macro_trends", ""),
            competitor_snapshot=competitor_data.get("competitive_overview", ""),
            operational_objective=objective,
            kpi_target=kpi,
            topic=topic
        )

    # Append ANTI_SLOP_RULES to ensure they are always applied
    # prompt_text += "\n\n" + templates.ANTI_SLOP_RULES

    # -------------------------------------------------
    # 6️⃣ GENERATION
    # -------------------------------------------------
    print(f"\n🚀 Sending request using Template {t_choice}...")
    blog_output = llm.generate(prompt_text, temperature=0.7)

    blog_output_path = BASE_DIR / "blog_output.txt"
    with open(blog_output_path, "w", encoding="utf-8") as f:
        f.write(blog_output)

    print("\n" + "="*45)
    print(f"✅ SUCCESS: Article saved to {blog_output_path}")
    print("="*45 + "\n")

if __name__ == "__main__":
    main()