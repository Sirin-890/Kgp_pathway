import pathway as pw
import pandas as pd
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.stdlib.indexing.nearest_neighbors import BruteForceKnnFactory
from pathway.xpacks.llm import parsers
from loguru import logger
from sentence_transformers import SentenceTransformer
from typing import Optional

class RetrieveQuerySchema(pw.Schema):
    query: str
    k: int
    metadata_filter: Optional[str]
    filepath_globpattern: Optional[str]

def run_vector_store(credential_path: str, object_id: str) -> None:
    try:
        # Initialize the embedding model
        logger.info("Initializing embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Read table from Google Drive
        logger.info("Reading table from Google Drive...")
        table = pw.io.gdrive.read(
            object_id=object_id,
            service_user_credentials_file=credential_path,
            with_metadata=True
        )
        logger.debug("Table read successfully from Google Drive")

        # Initialize components
        logger.info("Initializing retriever factory...")
        retriever_factory = BruteForceKnnFactory(dimensions=384)
        
        logger.info("Initializing parser...")
        parser = parsers.ParseUnstructured(
            mode='single',
            embedder=model
        )

        # Initialize DocumentStore
        logger.info("Initializing DocumentStore...")
        doc_store = DocumentStore(
            docs=table,
            retriever_factory=retriever_factory,
            parser=parser,
        )
        logger.debug("DocumentStore initialized successfully")

        # Create query data
        query_data = pd.DataFrame([{
            'query': "Retrieve all documents",
            'k': 5,
            'metadata_filter': None,
            'filepath_globpattern': None
        }])
        
        # Convert to pathway table with explicit schema
        query_tab = pw.debug.table_from_pandas(
            query_data,
            schema=RetrieveQuerySchema
        )
        logger.debug("Query table created with correct schema")

        # Execute query
        logger.info("Executing query...")
        result_list = doc_store.retrieve_query(query_tab)
        logger.debug("Query executed successfully")

        # Process results
        logger.info("Processing results...")
        results = pw.debug.table_to_pandas(result_list, include_id=False)
        
        if results.empty:
            logger.warning("No results found")
            return
            
        if 'result' not in results.columns:
            logger.warning("Results do not contain expected 'result' column")
            return

        # Print results
        logger.info("Query Results:")
        if len(results['result']) > 0:
            for idx, doc in enumerate(results['result'].iloc[0], 1):
                print(f"\nDocument {idx}:")
                print(f"Text: {doc['text']}")
                print(f"Score: {doc['dist']}")
                print(f"Metadata: {doc['metadata']}")

        logger.info("Starting Pathway runtime...")
        pw.run()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        run_vector_store(
            credential_path="/Users/nisarg/Desktop/Google_drive/Google_credentials.json",
            object_id="1PKCELu34EgxIEp-tdZz2wpxAdIXF-e_e",
        )
        logger.info("Vector store query completed successfully")
    except Exception as e:
        logger.error(f"Failed to run vector store: {str(e)}")
        raise