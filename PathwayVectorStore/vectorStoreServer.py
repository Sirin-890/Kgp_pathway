import pathway as pw
import threading
from pathway.xpacks.llm import parsers, splitters, embedders
from pathway.xpacks.llm.vector_store import VectorStoreServer
from loguru import logger

def make_vector_store_server(
    source, 
    port: int,
) -> None:

    parser = parsers.PypdfParser()

    embedder = embedders.OpenAIEmbedder()

    text_splitter = splitters.TokenCountSplitter(min_tokens=10000, max_tokens=1000000)

    vector_store = VectorStoreServer(
        source,
        parser=parser,
        splitter=text_splitter,
        embedder=embedder
    )

    vector_store.run_server(
        host="127.0.0.1",
        port=port,
    )

def run_vector_store(
    credential_path: str,
    object_id: str
)-> None:

    google_drive_files = pw.io.gdrive.read(
        object_id=object_id,
        service_user_credentials_file=credential_path,
        mode = "streaming",
        with_metadata = True
    )

    t = threading.Thread(
        target=make_vector_store_server,
        args=(google_drive_files, 8765)
    )

    t.start()
    
    logger.success("Vector store formed")
    
if __name__=="__main__":
    run_vector_store(
        credential_path="/Users/nisarg/Desktop/Kgp_pathway/credentials.json", 
        object_id="1XKNHwib7rnjEvFfrskQQ_WL-4PfecymN"
        )

# # 1. Set up Google Drive connector
# google_drive_files = pw.io.gdrive.read(
#     object_id="1XKNHwib7rnjEvFfrskQQ_WL-4PfecymN", # Replace with the ID of your Google Drive folder
#     service_user_credentials_file="/Users/nisarg/Desktop/Kgp_pathway/credentials.json", # Path to your Google Drive credentials
#     with_metadata=True,
#     mode="static"
# )

# print(pw.debug.table_to_pandas(google_drive_files, include_id=False))
# logger.debug("table to pandas")

# # 2. Define parser and splitter for documents
# parser = parsers.PypdfParser()
# logger.debug("parser formed")

# text_splitter = splitters.TokenCountSplitter(min_tokens=500, max_tokens=1000)
# logger.debug("splitter formed")

# # 3. Define embedder
# embedder = embedders.OpenAIEmbedder()
# logger.debug("embedder formed")


# # 4. Build Pathway DocumentStore
# vector_store = VectorStoreServer(
#     google_drive_files,
#     parser=parser,
#     splitter=text_splitter,
#     embedder=embedder
# )
# logger.debug("vector store formed")

# vector_store.run_server(
#         host="127.0.0.1",
#         port=8765,
#     )

# # 5. Run Pathway

# t = pw.debug.table_from_markdown('''
#         query | k    | metadata_filter | filepath_globpattern
#         *     | 5000 | None            | None
#         ''',
#         schema=VectorStoreServer.RetrieveQuerySchema
#     )
# logger.debug("Query table formed")
# # 6. Retrieve all documents
# all_documents = vector_store.retrieve_query(t)
# logger.debug("Retrieval done")

# logger.info(isinstance(all_documents, pw.Table))

# df = pw.debug.table_to_pandas(all_documents)
# logger.debug("table to pandas")

# print(df)
# logger.debug("printed df")