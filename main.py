import pandas as pd
from src.conference_selection import final_conference
from src.evaluator import evaluate
from PathwayVectorStore.vectorRetriever import VectorStoreRetriever
from loguru import logger

def pipeline() -> str:
    retriever = VectorStoreRetriever("127.0.0.1", port=8765)
    pdf = retriever.get_doc_text("What is document about?")
    evaluation_result = evaluate(pdf)
    if(evaluation_result == "Yes"):
        logger.debug("Research paper is suitable for publication")
        response = final_conference(pdf)
        print(response)
        return response
    else:
        logger.debug("Research paper is not suitable for publication")
        return ["N/A","Not suitable for publication"]
    
if __name__ == "__main__":
    pipeline()


