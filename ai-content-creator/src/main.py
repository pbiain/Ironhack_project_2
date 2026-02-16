"""Main application entry point."""

from content_pipeline import ContentPipeline


def main() -> None:
    pipeline = ContentPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
