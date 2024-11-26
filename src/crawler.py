from typing import Type

from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel


from .scraper import Scraper
from .logger import get_logger
from .prompt import SYSTEM_PROMPT, USER_PROMPT

logger = get_logger("crawler")


class ClaudeCrawler:
    def __init__(self, scraper: Scraper, model: BaseChatModel, output_schema: Type[BaseModel]):
        self.scraper = scraper
        self.model = model.with_structured_output(output_schema)
        self.system_prompt = SYSTEM_PROMPT
        self.user_prompt = USER_PROMPT

    def extract(self, instruction: str, html_content: str):
        logger.info("extract outputs...")
        prompt_value = ChatPromptTemplate(
            [
                ("system", SYSTEM_PROMPT),
                ("human", USER_PROMPT),
            ]
        ).invoke({"html_content": html_content, "instruction": instruction})
        return self.model.invoke(prompt_value)

    def crawl(self, url: str, instruction: str):
        logger.info(f"crawl url: {url}...")

        html_content = self.scraper.scrape(url)
        return self.extract(instruction, html_content)
