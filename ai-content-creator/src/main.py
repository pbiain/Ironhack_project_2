"""
Main application entry point.
1. Configures the selected LLM (OpenAI or Anthropic)
2. Processes markdown files into structured knowledge
3. Saves everything into a single JSON knowledge base
4. Generates content using the selected provider
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Project modules
from content_pipeline import ContentPipeline
# NEW: Import the Factory instead of the single function
from llm_integration import LLMFactory 

from knowledge_base import (
    build_brand_knowledge,
    build_product_knowledge,
    build_competitor_knowledge,
    build_industry_trends_knowledge,
    build_market_overview_knowledge,
)
from templates import blog_post_hybrid_strategic_engine

BASE_DIR = Path(__file__).resolve().parent.parent

def main() -> None:
    """Main orchestration function."""
    
    # -------------------------------------------------
    # 1️⃣ PROVIDER SELECTION & ENVIRONMENT
    # -------------------------------------------------
    load_dotenv()
    
    print("\n--- LLM Provider Selection ---")
    print("[1] OpenAI (GPT-4o-mini)")
    print("[2] Anthropic (Claude 3.5 Sonnet)")
    choice = input("Select provider (1 or 2): ").strip()
    
    provider_key = "openai" if choice == "1" else "anthropic"
    
    try:
        # Initialize the chosen provider via Factory
        llm = LLMFactory.get_provider(provider_key)
        print(f"✅ Using {provider_key.upper()} provider.")
    except Exception as e:
        print(f"❌ Error initializing provider: {e}")
        return

    # -------------------------------------------------
    # 2️⃣ RUN CONTENT PIPELINE
    # -------------------------------------------------
    print("\nRunning content pipeline...")
    pipeline = ContentPipeline()
    pipeline.run()

    # -------------------------------------------------
    # 3️⃣ BUILD KNOWLEDGE BASE PATHS
    # -------------------------------------------------
    brand_path = BASE_DIR / "knowledge_base/primary/brand_guidelines.md"
    product_path = BASE_DIR / "knowledge_base/primary/product_specs.md"
    competitor_path = BASE_DIR / "knowledge_base/secondary/competitor_analysis.md"
    market_path = BASE_DIR / "knowledge_base/secondary/market_trends.md"

    print("Processing knowledge base documents...")
    
    brand_data = build_brand_knowledge(str(brand_path))
    product_data = build_product_knowledge(str(product_path))
    competitor_data = build_competitor_knowledge(str(competitor_path))
    industry_data = build_industry_trends_knowledge(str(competitor_path))
    market_overview_data = build_market_overview_knowledge(str(market_path))

    full_knowledge_base = {
        "brand": brand_data,
        "product": product_data,
        "competitor_analysis": competitor_data,
        "industry_trends": industry_data,
        "market_overview": market_overview_data,
    }

    # Save JSON
    output_path = BASE_DIR / "knowledge_base.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_knowledge_base, f, indent=4, ensure_ascii=False)
    print(f"✅ Knowledge base saved to: {output_path}")

    # -------------------------------------------------
    # 4️⃣ PROMPT PREPARATION
    # -------------------------------------------------
    topic = "Why Flexible Fitness Infrastructure Is Replacing Traditional Gyms"
    
    # Injecting data into template
    prompt_text = blog_post_hybrid_strategic_engine(
        brand_voice_section=brand_data.get("brand_voice", ""),
        product_specs_section=product_data.get("product_overview", ""),
        partner_metrics_snapshot=product_data.get("customer_results", ""),
        market_data_snapshot=market_overview_data.get("industry_overview", ""),
        industry_trends_snapshot=industry_data.get("macro_trends", ""),
        competitor_snapshot=competitor_data.get("competitive_overview", ""),
        operational_objective="Increase sign-ups and reinforce infrastructure positioning",
        kpi_target="Increase CTR by 15% in 90 days",
        topic=topic
    )

    # Save Prompt for verification
    prompt_output_path = BASE_DIR / "prompt_test.txt"
    with open(prompt_output_path, "w", encoding="utf-8") as f:
        f.write(prompt_text)

    # -------------------------------------------------
    # 5️⃣ CALL SELECTED LLM & GENERATE
    # -------------------------------------------------
    print(f"\nSending prompt to {provider_key.upper()}...")
    
    # Instead of generate_content(prompt_text), we use our factory object
    blog_output = llm.generate(prompt_text, temperature=0.5)

    print("✅ Blog article generated successfully.")
    
    blog_output_path = BASE_DIR / "blog_output.txt"
    with open(blog_output_path, "w", encoding="utf-8") as f:
        f.write(blog_output)

    print(f"Blog saved to: {blog_output_path}")

if __name__ == "__main__":
    main()