import pathway as pw
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.xpacks.llm.servers import DocumentStoreServer
from pathway.stdlib.indexing.nearest_neighbors import BruteForceKnnFactory
from pathway.xpacks.llm import parsers
from pathway.debug import table_to_pandas
from loguru import logger

def run_vector_store(credential_path: str, object_id: str) -> None:
    table = pw.io.gdrive.read(
        object_id=object_id,
        service_user_credentials_file=credential_path,
        with_metadata = True
    )
    logger.debug("Table read from Google Drive")

    # Initialize the retriever factory (example: k-NN)
    retriever_factory = BruteForceKnnFactory(dimensions=512)
    logger.debug("Retriever factory initialized")

    parser = parsers.ParseUnstructured(
        mode='single'
    )

    # Initialize the DocumentStore
    doc_store = DocumentStore(
        docs=table,
        retriever_factory=retriever_factory,
        parser=parser,
    )

    logger.debug("DocumentStore initialized")

    # DocumentStoreServer.run(
    #     host="127.0.0.1",
    #     port=8765,
    #     doc_store=doc_store,
    # )

    query_tab = pw.Table.empty(query="str", k=int, metadata_filter=None, filepath_globpattern=None)
    print(pw.debug.compute_and_print(query_tab, include_id=False))
    logger.debug("Query table initialized")
    logger.info(isinstance(query_tab, pw.Table))

    # Fetch all input documents
    result_list = doc_store.retrieve_query(query_tab)
    logger.debug("Query executed")

    logger.info(isinstance(result_list, pw.Table))


    # Convert results to Python data
    results = pw.debug.table_to_pandas(result_list, include_id=False)
    logger.debug("Results converted to pandas")

    # Extract text data
    # documents = [doc["text"] for doc in results["result"]]
    # for i, text in enumerate(documents):
    #     print(f"Document {i+1}: {text}")
    

    print ("Server initiated")
    pw.run()
    return ""

if __name__ == "__main__":
    run_vector_store(
        credential_path="/Users/nisarg/Desktop/Google_drive/Google_credentials.json",
        object_id="1PKCELu34EgxIEp-tdZz2wpxAdIXF-e_e",
    )