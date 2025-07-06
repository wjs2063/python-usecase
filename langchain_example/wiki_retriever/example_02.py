# wikiapi_retriever.py
from typing import List
import wikipediaapi
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
import requests
class WikiApiRetriever(BaseRetriever):
    def __init__(self, lang: str = "en", top_k: int = 3, chars_max: int = 6_000):
        self.wiki = wikipediaapi.Wikipedia(language=lang, extract_format=wikipediaapi.ExtractFormat.WIKI)
        self.top_k = top_k
        self.chars_max = chars_max
        self.lang = lang

    def _get_relevant_documents(self, query: str) -> List[Document]:
        # 1) search
        search_url = (
            f"https://{self.lang}.wikipedia.org/w/api.php?"
            f"action=query&list=search&srlimit={self.top_k}&format=json&srsearch={query}"
        )
        data = requests.get(search_url, timeout=10).json()["query"]["search"]

        docs = []
        for item in data:
            page = self.wiki.page(item["title"])
            if not page.exists():           # rare but possible
                continue
            content = page.text[: self.chars_max]
            docs.append(
                Document(
                    page_content=content,
                    metadata={
                        "title": page.title,
                        "source": page.fullurl,
                        "summary": item["snippet"],
                    },
                )
            )
        return docs

    # langchain 1.x 스타일 invoke 호환
    def invoke(self, query: str, **kw):
        return self._get_relevant_documents(query)



wiki_en = wikipediaapi.Wikipedia(
    user_agent='MyProject/1.0 (your_@email.com)',
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

wiki_ko = wikipediaapi.Wikipedia(
    user_agent='MyProject/1.0 (your_@email.com)',
    language='ko',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

print(1)

docs_ko = wiki_ko.page("lee-jae yong")
print(docs_ko.text)
print("="*100)
print(docs_ko.sections)
print("="*100)
print(docs_ko.links)
print("="*100)
print(docs_ko.categories)
print("="*100)
print(docs_ko.summary)
docs_en = wiki_en.page("")
"""
    ATTRIBUTES_MAPPING = {
        "language": [],
        "variant": [],
        "pageid": ["info", "extracts", "langlinks"],
        "ns": ["info", "extracts", "langlinks"],
        "title": ["info", "extracts", "langlinks"],
        "contentmodel": ["info"],
        "pagelanguage": ["info"],
        "pagelanguagehtmlcode": ["info"],
        "pagelanguagedir": ["info"],
        "touched": ["info"],
        "lastrevid": ["info"],
        "length": ["info"],
        "protection": ["info"],
        "restrictiontypes": ["info"],
        "watchers": ["info"],
        "visitingwatchers": ["info"],
        "notificationtimestamp": ["info"],
        "talkid": ["info"],
        "fullurl": ["info"],
        "editurl": ["info"],
        "canonicalurl": ["info"],
        "readable": ["info"],
        "preload": ["info"],
        "displaytitle": ["info"],
        "varianttitles": ["info"],
    }
"""

def page_to_document(wiki_page,doc_content_chars_max:int) -> List[Document]:
    if not wiki_page.exists():
        return list()
    try:
        main_meta = {
            "title": wiki_page.title,
            "summary": wiki_page.summary,
            "source": wiki_page.fullurl,
        }
        add_meta = (
            {
                "categories": wiki_page.categories,
                "page_url": wiki_page.fullurl,
                "related_titles": wiki_page.links,
                "sections": wiki_page.sections,
            })

        doc = Document(
            page_content=wiki_page.text[: doc_content_chars_max],
            metadata={
                **main_meta,
                **add_meta,
            },
        )
    except Exception as e:
        import logging
        logging.warning(f"Error converting page to document: {e}")
    else:
        return doc

print(page_to_document(docs_ko,100))
# Section 1
# Text of section 1
# Section 1.1
# Text of section 1.1
# ...


# wiki_html = wikipediaapi.Wikipedia(
#     user_agent='wikipedia (https://github.com/goldsmith/Wikipedia/)',
#     language='en',
#     extract_format=wikipediaapi.ExtractFormat.HTML
# )
# p_html = wiki_html.page("lee-jae yong")
# print(p_html.text)