from typing import List
import requests

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class WikidocsLoader(BaseLoader):
    def __init__(self, book_id: int, base_url="https://wikidocs.net", **kwargs):
        super().__init__(**kwargs)
        self.book_id = book_id
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def load(self) -> List[Document]:
        toc = self._get_toc(self.book_id)
        pages = []
        for item in toc:
            page_id = item["id"]
            page_data = self._get_page(page_id)
            document = Document(
                title=page_data["subject"],
                page_content=page_data["content"],
                metadata={
                    'id': page_id,
                    'source': f"{self.base_url}/{page_id}",
                    'title': page_data["subject"]
                }
            )
            pages.append(document)

        return pages

    def _get_toc(self, book_id):
        url = f"{self.base_url}/api/v1/toc/{book_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Failed to get table of contents")

    def _get_page(self, page_id):
        url = f"{self.base_url}/api/v1/page/{page_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("Failed to get page")
