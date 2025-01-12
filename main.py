import time
import pandas as pd
import os
from src.extract import extract_pdf_single
from src.conference_selection import final_conference
from src.evaluator import evaluate
from PathwayVectorStore.vectorRetriever import VectorStoreRetriever
from loguru import logger


def result_csv(folder_path: str) -> None:
    data = {"Paper ID": [], "Publishable": [], "Conference": [], "Rationale": []}
    df = pd.DataFrame(data)
    count = 1
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                time.sleep(20)
                file_path = os.path.join(root, file)
                research_paper = extract_pdf_single(file_path)
                eval_result = evaluate(research_paper)
                if(eval_result == "Yes"):
                    result = final_conference(research_paper)
                    print(f"{count} {file.split('.pdf')[0]} -> {result[0]}")
                    df.loc[len(df)] = [file.split(".pdf")[0], 1, result[0], result[1]]
                else:
                    print(f"{count} {file.split('.pdf')[0]} -> Not suitable for publication")
                    df.loc[len(df)] = [file.split(".pdf")[0], 0, "na", "na"]
                count += 1        
    return df

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
    # research_paper = extract_pdf_single('/Users/nisarg/Desktop/Kgp_pathway/Benchmark/Publishable/TMLR/R015.pdf')
    # evaluation_result = evaluate(research_paper)
    # print(evaluation_result)    
    # if(evaluation_result == "Yes"):
    #     print(final_conference(research_paper))
    # else:
    #     print("Not suitable for publication")

