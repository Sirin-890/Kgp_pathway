import os, glob, PyPDF2

# For all the PDFs in a folder
def extract_pdf_folder(folder_path: str) -> list:
    read_files = glob.glob(os.path.join(folder_path,'*.pdf'))
    final_output = []
    for files in read_files:
        pdfReader = PyPDF2.PdfReader(files)
        output = ""
        for i in range(len(pdfReader.pages)):
            pageObj = pdfReader.pages[i]
            output += pageObj.extract_text()
        final_output.append(output)
    return final_output    

# For a single PDF
def extract_pdf_single(pdf_path: str) -> str:
    pdfFileObject = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObject)
    output = ""
    for i in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[i]
        output += pageObj.extract_text()
    return output

if __name__ == "__main__":
    print(extract_pdf_folder('.')[0])