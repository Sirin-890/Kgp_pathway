import pathway as pw
from pathway.xpacks.llm import parsers, splitters, embedders
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.stdlib.indexing.vector_document_index import default_vector_document_index

# 1. Set up Google Drive connector
google_drive_files = pw.io.gdrive.read(
    object_id="1XKNHwib7rnjEvFfrskQQ_WL-4PfecymN", # Replace with the ID of your Google Drive folder
    service_user_credentials_file="credentials.json", # Path to your Google Drive credentials
    with_metadata=True,
    mode="static"
)

print(pw.debug.table_to_pandas(google_drive_files, include_id=False))

# 2. Define parser and splitter for documents
parser = parsers.ParseUnstructured(mode='single')
text_splitter = splitters.TokenCountSplitter(min_tokens=500, max_tokens=1000)

# 3. Define embedder
embedder = embedders.OpenAIEmbedder()


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

# 5. Run Pathway
pw.run()


# 6. Retrieve all documents
#all_documents = document_store.inputs_query(pw.Table.empty())

# Access the documents and their metadata
# for doc in all_documents.result:
#     print(f"Path: {doc['path']}")
#     print(f"Text: {doc['text'][:50]}...")  # Print the first 50 characters of the text


# Alternative method for getting the indexed documents from the retriever:
all_documents_from_index = document_store.index.data_table

# Now you can use `all_documents.result` or `all_documents_from_index` to access the retrieved documents.
print(type(all_documents_from_index))

print(all_documents_from_index)

print(all_documents_from_index.select(all_documents_from_index.text))


# If you want a simpler, more direct way to access just the text:
# for row in all_documents_from_index: # Or iterate directly if you only need the text
#     print(type(row))
#     chunk_text = row.text 
#     print(f"Chunk text (first 50 characters or less): {chunk_text[:50]}") # Access text using the "text" key
#     print("-" * 20)