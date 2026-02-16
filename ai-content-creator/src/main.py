"""Main application entry point."""
from dotenv import load_dotenv
from content_pipeline import ContentPipeline
import config
def main() -> None:
    config.config_llm()
    pipeline = ContentPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
