import os
print("Current working directory:", os.getcwd())

"""Main application entry point."""

# src/main.py

# Import Python's built-in JSON library
import json

# Import our knowledge builder function
from knowledge_base import build_brand_knowledge


from dotenv import load_dotenv
from content_pipeline import ContentPipeline
import config


def main() -> None:
    config.config_llm()
    pipeline = ContentPipeline()
    pipeline.run()


    # Path to the markdown file
    file_path = "C:\\Users\\pbiai\\Desktop\\Ironhack_Project_2\\ai-content-creator\\knowledge_base\\primary\\brand_guidelines.md"
    print(f"File path: {file_path}")
    print("Loading brand guidelines...")

    # Build structured knowledge dictionary
    brand_data = build_brand_knowledge(file_path)

    # Define where to save the JSON file
    output_path = "../brand_guidelines.json"

    # Open file in write mode and save JSON
    with open(output_path, "w", encoding="utf-8") as f:
        # indent=4 makes it pretty
        # ensure_ascii=False keeps special characters readable
        json.dump(brand_data, f, indent=4, ensure_ascii=False)

    print("✅ JSON created successfully.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()

