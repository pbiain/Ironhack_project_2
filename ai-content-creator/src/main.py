"""
Main application entry point.
1. Configures the selected LLM (OpenAI or Anthropic).
2. Processes markdown files into structured knowledge.
3. Takes dynamic user input for topic, objectives, and KPIs.
4. Generates content in a single high-quality pass.
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
from templates import blog_post_hybrid_strategic_engine

# Resolve project paths
BASE_DIR = Path(__file__).resolve().parent.parent

def main() -> None:
    """Main orchestration function."""
    load_dotenv()
    
    print("\n" + "="*45)
    print("🚀 AI CONTENT CREATOR - DYNAMIC MODE")
    print("="*45)
    
    # -------------------------------------------------
    # 1️⃣ PROVIDER SELECTION
    # -------------------------------------------------
    print("\n[1] OpenAI (GPT-4o-mini)")
    print("[2] Anthropic (Claude 3.5 Sonnet)")
    choice = input("Select provider (1 or 2): ").strip()
    
    provider_key = "openai" if choice == "1" else "anthropic"
    
    try:
        llm = LLMFactory.get_provider(provider_key)
        print(f"✅ Using {provider_key.upper()} provider.")
    except Exception as e:
        print(f"❌ Error initializing provider: {e}")
        return

    # -------------------------------------------------
    # 2️⃣ DATA PROCESSING
    # -------------------------------------------------
    print("\nProcessing knowledge base documents...")
    brand_path = BASE_DIR / "knowledge_base/primary/brand_guidelines.md"
    product_path = BASE_DIR / "knowledge_base/primary/product_specs.md"
    market_path = BASE_DIR / "knowledge_base/secondary/market_trends.md"
    competitor_path = BASE_DIR / "knowledge_base/secondary/competitor_analysis.md"

    # Loading data from your document processors
    brand_data = build_brand_knowledge(str(brand_path))
    product_data = build_product_knowledge(str(product_path))
    market_overview_data = build_market_overview_knowledge(str(market_path))
    industry_data = build_industry_trends_knowledge(str(competitor_path))
    competitor_data = build_competitor_knowledge(str(competitor_path))

    # -------------------------------------------------
    # 3️⃣ DYNAMIC USER INPUTS
    # -------------------------------------------------
    print("\n" + "-"*30)
    print("📝 CUSTOMIZE YOUR POST")
    print("-"*30)

    # Topic Input
    topic_in = input("Enter the blog topic\n(Default: Flexible Fitness vs Traditional Gyms): ").strip()
    topic = topic_in if topic_in else "Why Flexible Fitness Infrastructure Is Replacing Traditional Gyms"

    # Objective Input
    obj_in = input("\nWhat is the main goal?\n(Default: Increase sign-ups/positioning): ").strip()
    objective = obj_in if obj_in else "Increase sign-ups and reinforce infrastructure positioning"

    # KPI Input
    kpi_in = input("\nWhat is the KPI target?\n(Default: Increase CTR by 15%): ").strip()
    kpi = kpi_in if kpi_in else "Increase CTR by 15% in 90 days"

    # -------------------------------------------------
    # 4️⃣ PROMPT PREPARATION
    # -------------------------------------------------
    prompt_text = blog_post_hybrid_strategic_engine(
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

    # -------------------------------------------------
    # 5️⃣ GENERATION & SAVING
    # -------------------------------------------------
    print(f"\n🚀 Sending request to {provider_key.upper()}...")
    
    # Direct generation (no loop)
    blog_output = llm.generate(prompt_text, temperature=0.7)

    # Save Final Result
    blog_output_path = BASE_DIR / "blog_output.txt"
    with open(blog_output_path, "w", encoding="utf-8") as f:
        f.write(blog_output)

    print("\n" + "="*45)
    print(f"✅ SUCCESS: Article saved to {blog_output_path}")
    print("="*45 + "\n")

if __name__ == "__main__":
    main()