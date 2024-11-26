from abc import ABC, abstractmethod

from playwright.sync_api import Route
from bs4 import BeautifulSoup as Soup
from playwright.sync_api import sync_playwright


from .logger import get_logger

logger = get_logger("scraper")


class Scraper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> str: ...


class PlayWrightScraper(Scraper):
    """Playwright를 사용하여 웹 페이지를 스크래핑 하는 클래스"""

    def __init__(self):
        super().__init__()

        # 차단할 리소스 타입 정의
        self.block_resource_types = [
            "beacon",
            "csp_report",
            "font",
            "image",
            "imageset",
            "media",
            "object",
            "texttrack",
        ]

        # 차단할 트래커 및 광고 도메인 정의
        self.block_resource_names = [
            "adzerk",
            "analytics",
            "cdn.api.twitter",
            "doubleclick",
            "exelator",
            "facebook",
            "fontawesome",
            "google",
            "google-analytics",
            "googletagmanager",
            "adform",
        ]

        # 제거할 태그 목록
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

    def _intercept_route(self, route: Route):
        """요청을 가로채서 차단된 리소스는 중단"""
        if route.request.resource_type in self.block_resource_types:
            logger.debug(f"리소스 차단: {route.request.url} (타입: {route.request.resource_type})")
            return route.abort()

        if any(tracker in route.request.url for tracker in self.block_resource_names):
            logger.debug(f"트래커 차단: {route.request.url}")
            return route.abort()

        return route.continue_()

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
        """HTML에서 불필요한 태그를 제거한다."""
        for tag in self.tags_to_remove:
            for element in soup.find_all(tag):
                element.decompose()
        return soup

    def fetch(self, url: str) -> str:
        """페이지의 HTML을 가져온다."""
        logger.info(f"fetch url: {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.route("**/*", self._intercept_route)
            page.goto(url)
            content = page.content()
            browser.close()
            return content

    def scrape(self, url: str) -> str:
        """웹 페이지를 스크래핑한다."""
        logger.info(f"scrape url: {url}...")

        raw_html = self.fetch(url)
        raw_soup = Soup(raw_html, "html.parser")
        cleaned_soup = self.clean_html(raw_soup)
        flat_soup = self.flatten_html(cleaned_soup)
        return str(flat_soup)
