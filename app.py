import os
import json
from pathlib import Path
from typing import Type, List, cast

from dotenv import load_dotenv

load_dotenv()

from pydantic import BaseModel, Field

from src.logger import get_logger
from src.llm import BedrockLLM
from src.crawler import ClaudeCrawler


MODEL_ID = os.environ.get("MODEL_ID", "us.anthropic.claude-3-5-haiku-20241022-v1:0")
AWS_PROFILE_NAME = os.environ.get("AWS_PROFILE_NAME", None)
AWS_REGION = os.environ.get("AWS_REGION", None)

logger = get_logger("app")


class Article(BaseModel):
    """
    LOL(League of Legends) champion tatic article schema.
    Contains details about how to play and win with a specific LOL champion.
    """

    title: str = Field(..., description="The title of the article.")
    url: str = Field(..., description="The URL link to the article.")
    season: int = Field(..., description="The season of the article.")
    published_at: str = Field(..., description="The published date of the article in RFC 3339 format.")


class OutputSchema(BaseModel):
    """
    Schema to extract articles for the LOL tatic from the page.
    """

    articles: List[Article] = Field(
        [], description="A list of LOL champion tactic article objects extracted from the page."
    )


def main(url: str, instruction: str, output_schema: Type[BaseModel]):
    """
    Main function to crawl and extract LOL champion tactic articles from a webpage.

    Args:
        url (str): The URL of the webpage to crawl
        instruction (str): Instructions for the crawler on what to extract
        output_schema (Type[BaseModel]): Pydantic model defining the expected output structure

    Returns:
        OutputSchema: Extracted articles in the defined schema format
    """
    llm = BedrockLLM(
        model=MODEL_ID,
        aws_profile_name=AWS_PROFILE_NAME,
        aws_region=AWS_REGION,
    )
    crawler = ClaudeCrawler(llm.model, output_schema)
    return crawler.crawl(url, instruction)


if __name__ == "__main__":
    url = "https://lol.inven.co.kr/dataninfo/champion/manualTool.php?confirm=2&season=14"

    output_path = Path(__file__).resolve().parent / "output"
    _ = output_path.exists() or output_path.mkdir(exist_ok=True, parents=True)

    instruction = (
        "Please extract the LOL champion tactic articles from the page."
        "The articles are listed at the <table> tag in the page."
    )
    resp = main(url, instruction, OutputSchema)
    logger.info(f"Output: {resp}")

    with open(output_path / "output.jsonl", "w") as fp:
        output = cast(OutputSchema, resp)
        for article in output.articles:
            fp.write(json.dumps(article.__dict__) + "\n")
