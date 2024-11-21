from typing import Type

import requests
from bs4 import BeautifulSoup as Soup
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_aws.chat_models import ChatBedrockConverse

from .logger import get_logger
from .prompt import SYSTEM_PROMPT, USER_PROMPT

logger = get_logger("crawler")


class ClaudeCrawler:
    def __init__(self, model: ChatBedrockConverse, output_schema: Type[BaseModel]):
        self.model = model.with_structured_output(output_schema)
        self.system_prompt = SYSTEM_PROMPT
        self.user_prompt = USER_PROMPT

        self.tags_to_remove = [
            "head",
            "script",
            "style",
            "noscript",
            "svg",
            "meta",
            "iframe" "link",
            "video",
            "audio",
        ]

    def should_remove_tag(self, tag):
        """
        태그가 제거되어야 하는 조건
        1. 내용이 비어있거나 공백뿐인 경우
        2. 자식 노드가 하나뿐이고 같은 태그인 경우
        """
        if not tag.contents:
            return True

        if len(tag.contents) == 1:
            child = tag.contents[0]
            if isinstance(child, type(tag)) and child.name == tag.name:
                return True

        text_content = tag.get_text(strip=True)
        if not text_content and len(tag.find_all()) == 0:
            return True

        return False

    def _clean_tag(self, tag):
        """재귀적으로 모든 자식 태그들을 정리한다."""
        for child in tag.find_all(recursive=False):
            self._clean_tag(child)

        if self.should_remove_tag(tag):
            tag.unwrap()

    def flatten_html(self, soup: Soup) -> Soup:
        """모든 불필요한 공백을 제거하고 중첩된 의미없는  래핑 태그들을 제거해준다."""
        for element in soup(text=lambda text: isinstance(text, str)):
            if element.strip() == "":
                element.extract()

        self._clean_tag(soup)

        return soup

    def clean_html(self, soup: Soup) -> Soup:
        for tag in self.tags_to_remove:
            for element in soup.find_all(tag):
                element.decompose()
        return soup

    def extract(self, instruction: str, soup: Soup):
        logger.info("extract outputs...")
        prompt_value = ChatPromptTemplate(
            [
                ("system", SYSTEM_PROMPT),
                ("human", USER_PROMPT),
            ]
        ).invoke({"html_content": str(soup), "instruction": instruction})
        return self.model.invoke(prompt_value)

    def fetch(self, url: str) -> str:
        logger.info(f"fetch url: {url}")
        return requests.get(url, timeout=5).content.decode("utf-8")

    def crawl(self, url: str, instruction: str):
        logger.info(f"scrape url: {url}...")

        raw_html = self.fetch(url)
        raw_soup = Soup(raw_html, "html.parser")
        cleaned_soup = self.clean_html(raw_soup)
        flat_soup = self.flatten_html(cleaned_soup)
        return self.extract(instruction, flat_soup)
