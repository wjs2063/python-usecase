from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI,OpenAI
from dotenv import load_dotenv
import logging
from datetime import datetime
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
load_dotenv()

llm = OpenAI(
    model="gpt-4o-mini"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
prompt = PromptTemplate.from_template(
    template="""You are a helpful assistant.Answer the question as detailed as possible.
    Answer the answer by korea
    Question: {question}
    Answer:"""
)

class LoggingCallbackHandler(BaseCallbackHandler):
    """LLM 호출 전후로 간단한 로그를 남기는 LangChain CallbackHandler."""

    # def on_llm_start(
    #     self,
    #     serialized,            # 체인/LLM 메타 정보
    #     prompts,               # 전달된 프롬프트 리스트
    #     **kwargs,
    # ):
    #     """LLM 호출 직전에 실행."""
    #     # 여러 프롬프트가 들어올 수 있음 → 첫 번째만 미리보기로 표기
    #     preview = prompts[0][:200].replace("\n", " ") + ("..." if len(prompts[0]) > 200 else "")
    #     logging.info(f"[LLM START] {serialized['id']} | prompt preview: {preview}")

    def on_llm_end(
        self,
        response: LLMResult,   # LLM 실행 결과
        **kwargs,
    ):
        """LLM 호출이 정상 종료됐을 때 실행."""
        # 토큰 수·응답 길이 등 원하는 항목을 자유롭게 기록
        text = response.llm_output
        logging.info(f"[LLM END] tokens: {response.llm_output['token_usage']} | "
                     f"response preview: {text[:120]}{'...' if len(text) > 120 else ''}")

    def on_llm_error(self, error: BaseException, **kwargs):
        """LLM 호출 중 예외 발생 시 실행."""
        logging.exception("[LLM ERROR] Exception raised during LLM call", exc_info=error)

callback = LoggingCallbackHandler()

chain = (prompt | llm).with_config(
    run_name="korean_qa_chain",
    callbacks=[callback],  # 리스트 형태로 넘겨주면 됨
)

first_chain = (prompt | llm)
full_chain = ({"question":first_chain} | prompt | llm).with_config(
    run_name="korean_qa_chain",
    callbacks=[callback],
)


print(full_chain.invoke({"question": "what is the meaning of life?"}))


