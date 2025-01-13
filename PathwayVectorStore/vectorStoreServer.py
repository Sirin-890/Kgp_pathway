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

    text_splitter = splitters.TokenCountSplitter(min_tokens=1000, max_tokens=1000000)

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
