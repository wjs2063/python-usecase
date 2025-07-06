from langchain_community.retrievers import WikipediaRetriever
from langchain.retrievers import EnsembleRetriever

class WikipediaRetrieverFixed(WikipediaRetriever):
    def _search(self, query: str):
        # 매 호출마다 언어를 강제로 설정
        self.wiki_client.set_lang(self.lang)
        return super()._search(query)
print(WikipediaRetriever.__mro__)
# 1) 언어별 인스턴스
retriever_ko = WikipediaRetriever(lang="ko", top_k_results=1)  # ← 한글 위키
retriever_en = WikipediaRetriever(lang="en", top_k_results=1)

# 2) 개별 호출
docs_en = retriever_en.invoke("Large language model")
docs_ko = retriever_ko.invoke("대규모 언어 모델")
print(docs_en)
print(docs_ko)

combo = EnsembleRetriever(retrievers=[retriever_en],   # 순서는 가중치에 따라
                          weights=[0.5])
docs = combo.invoke("손흥민")   # 한글·영문 위키 컨텍스트를 한 번에

print(docs)

# 여기서 뭔가 전역 API_URL이 덮어씌워지는 현상이 발생함