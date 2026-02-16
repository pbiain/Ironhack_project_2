"""
Main application entry point.
This file does three things:
1. Configures the LLM and runs the content pipeline
2. Processes markdown files into structured knowledge
3. Saves everything into a single JSON knowledge base
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from typer import prompt
# Project modules
import config
from content_pipeline import ContentPipeline
from llm_integration import generate_content

BASE_DIR = Path(__file__).resolve().parent.parent



from knowledge_base import (
    build_brand_knowledge,
    build_product_knowledge,
    build_competitor_knowledge,
    build_industry_trends_knowledge,
    build_market_overview_knowledge,
)
# ✅ NEW: Template import (does not change existing logic)

from templates import blog_post_hybrid_strategic_engine
def main() -> None:
    """
    Main orchestration function.
    Runs pipeline + builds structured knowledge base.
    """
    # -------------------------------------------------
    # 1️⃣ ENVIRONMENT + PIPELINE
    # -------------------------------------------------
    print("Current working directory:", os.getcwd())
    # Load .env variables
    load_dotenv()
    # Configure LLM
    config.config_llm()
    # Run content pipeline
    print("Running content pipeline...")
    pipeline = ContentPipeline()
    pipeline.run()
    # -------------------------------------------------
    # 2️⃣ BUILD SAFE PATHS (THIS IS THE FIX)
    # -------------------------------------------------
    
    brand_path = BASE_DIR / "knowledge_base/primary/brand_guidelines.md"
    product_path = BASE_DIR / "knowledge_base/primary/product_specs.md"
    competitor_path = BASE_DIR / "knowledge_base/secondary/competitor_analysis.md"
    market_path = BASE_DIR / "knowledge_base/secondary/market_trends.md"
    print("Loading and processing knowledge base documents...")
    # -------------------------------------------------
    # 3️⃣ BUILD STRUCTURED KNOWLEDGE
    # -------------------------------------------------
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
    # -------------------------------------------------
    # 4️⃣ SAVE JSON OUTPUT
    # -------------------------------------------------
    output_path = BASE_DIR / "knowledge_base.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_knowledge_base, f, indent=4, ensure_ascii=False)
    print("✅ Knowledge base JSON created successfully.")
    print(f"Saved to: {output_path}")
    # -------------------------------------------------
    # 5️⃣ PROMPT INJECTION VERIFICATION (NEW BLOCK)
    # -------------------------------------------------
    print("\nGenerating prompt (verification only)...")
    # Extract specific condensed sections
    brand_voice_section = brand_data.get("brand_voice", "")
    product_specs_section = product_data.get("product_overview", "")
    partner_metrics_snapshot = product_data.get("customer_results", "")
    market_data_snapshot = market_overview_data.get("industry_overview", "")
    industry_trends_snapshot = industry_data.get("macro_trends", "")
    competitor_snapshot = competitor_data.get("competitive_overview", "")
    operational_objective = "Increase sign-ups and reinforce infrastructure positioning"
    kpi_target = "Increase CTR by 15% in 90 days"
    topic = "Why Flexible Fitness Infrastructure Is Replacing Traditional Gyms"
    prompt = blog_post_hybrid_strategic_engine(
        brand_voice_section=brand_voice_section,
        product_specs_section=product_specs_section,
        partner_metrics_snapshot=partner_metrics_snapshot,
        market_data_snapshot=market_data_snapshot,
        industry_trends_snapshot=industry_trends_snapshot,
        competitor_snapshot=competitor_snapshot,
        operational_objective=operational_objective,
        kpi_target=kpi_target,
        topic=topic
    )
    print("\n----- PROMPT PREVIEW (first 2000 characters) -----\n")
    print(prompt[:2000])

    # -------------------------------------------------
# 6️⃣ SAVE PROMPT TO FILE (VERIFICATION OUTPUT)
# -------------------------------------------------

    prompt_output_path = BASE_DIR / "prompt_test.txt"

    with open(prompt_output_path, "w", encoding="utf-8") as f:
        f.write(prompt)

    print("\n✅ Prompt saved successfully.")
    print(f"Saved to: {prompt_output_path}")

    # -------------------------------------------------
    # 8️⃣ CALL LLM
    # -------------------------------------------------

    print("\nSending prompt to LLM...")

    blog_output = generate_content(prompt)

    print("✅ Blog article generated successfully.")
    blog_output_path = BASE_DIR / "blog_output.txt"

    with open(blog_output_path, "w", encoding="utf-8") as f:
        f.write(blog_output)

    print(f"Blog saved to: {blog_output_path}")



# Run only when file executed directly
if __name__ == "__main__":
    main()