from PathwayVectorStore.vectorStoreClient import VectorStoreClientModified
from loguru import logger
from typing import List, Dict

class VectorStoreRetriever(object):
    def __init__(
        self,
        host: str,
        port: int = 8765
    ) -> None:
        self.host = host
        self.port = port

        self.client = VectorStoreClientModified(
            host=self.host,
            port=self.port
        )

    def get_context(self, query: str, topk: int = 50) -> List[str]:
        docs = self.client(
            query=query,
            k=topk
        )

        docs_list = []
        for doc in docs:
            docs_list.append(
                doc["text"]
            )

        return docs_list

    def get_top_k(self, query: str, topk: int = 5) -> List[Dict[str, str]]:
        docs = self.client(
            query=query,
            k=topk
        )
        return docs
    
    def get_all_chunks(self, query: str) -> List[Dict[str, str]]:
        return self.client.query_all_chunks(query)

    def get_num_input_files(self):
        res = self.client.get_input_files()
        return len(res)
    
    def get_doc_text(self, query: str) -> str:
        res = self.get_context(
            query=query,
            topk=100000
        )
        return "".join(res)


if __name__ == "__main__":
    retriever = VectorStoreRetriever("127.0.0.1", port=8765)
    res = retriever.get_doc_text("What is the abstract of the document?")
    logger.debug(f"Result: {res}")
    logger.debug(f"type - {type(res)}")
    logger.debug(f"len - {len(res)}")
