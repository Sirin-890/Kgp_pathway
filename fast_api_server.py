import uvicorn
from fastapi import FastAPI, UploadFile
import os
from loguru import logger
from PathwayVectorStore.vectorStoreServer import run_vector_store
from main import pipeline

app = FastAPI()

# Ensure the directory for uploaded files exists
os.makedirs("./uploaded_files", exist_ok=True)

# FastAPI endpoint to upload file
@app.post("/upload")
async def save_file(file: UploadFile, drive_link: str):
    global collection_name_global
    collection_name_global = ""
    logger.success(f"Drive Link received: {drive_link}")
    temp_file_path = os.path.join("./uploaded_files", file.filename)

    object_id = drive_link.split("/")[-1]

    logger.success(f"Object ID: {object_id}")
    logger.success(f"File Path: {temp_file_path}")

    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    run_vector_store(
        credential_path=temp_file_path,
        object_id=object_id
    )
    return ""

# FastAPI endpoint to process text
@app.get("/process")
async def process_text():
    final_response = pipeline()
    return {"response":final_response}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)