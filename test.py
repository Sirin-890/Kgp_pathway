import pathway as pw
from pathway.xpacks.llm import parsers, splitters, embedders
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.stdlib.indexing.vector_document_index import default_vector_document_index

# 1. Set up Google Drive connector
google_drive_files = pw.io.gdrive.read(
    object_id="1mS7UIpHTCCczn4EI7SEurkO9I9JUEzQ0", # Replace with the ID of your Google Drive folder
    service_user_credentials_file="/Users/nisarg/Desktop/Google_drive/credentials.json", # Path to your Google Drive credentials
    with_metadata=True,
    mode="static",
)


# 2. Define parser and splitter for documents
parser = parsers.PypdfParser()
text_splitter = splitters.TokenCountSplitter(min_tokens=500, max_tokens=5000) # Adjust chunk size and overlap as needed


# 3. Define embedder. Note that OpenAI embedder requires `OPENAI_API_KEY` environment variable.
embedder = embedders.OpenAIEmbedder(
    cache_strategy=pw.udfs.DefaultCache()
)


# 4. Build Pathway DocumentStore
document_store = DocumentStore(
    docs=google_drive_files,
    parser=parser,
    splitter=text_splitter,
    retriever_factory=pw.stdlib.indexing.UsearchKnnFactory(
        dimensions=embedder.get_embedding_dimension(),
        embedder=embedder,
    ),
)


# 5. (Optional) Set up a REST API endpoint
# from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
# from pathway.xpacks.llm.servers import QASummaryRestServer
# chat = llms.OpenAIChat() # create an OpenAI chat model
# rag_app = BaseRAGQuestionAnswerer(chat, document_store) # create a RAG app
# app = QASummaryRestServer("127.0.0.1", 8000, rag_app) # create a REST server object

# Then you can query the server
# rag_app.run_server()

# 6. Run Pathway
pw.run()

# Now you can use document_store.chunked_docs to access the extracted text
# and document_store.index to query the index