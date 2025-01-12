import os, glob, PyPDF2

def extract_pdf_folder(folder_path: str) -> list:
    final_output = ""

    # Walk through all subdirectories and files
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):  # Check if the file is a PDF
                if(root.split("/")[-1] == "Non-Publishable"):
                    final_output += "Given below is an example of a NON-PUBLISHABLE research paper\n\n"
                else:
                    final_output += "Given below is an example of a PUBLISHABLE research paper\n\n"
                    final_output += (root.split("/")[-1].upper() + "\n\n")  
                file_path = os.path.join(root, file)
                pdfReader = PyPDF2.PdfReader(file_path)
                output = ""
                for i in range(len(pdfReader.pages)):
                    pageObj = pdfReader.pages[i]
                    output += pageObj.extract_text()
                final_output += (output + "-------------------------------------------------------------------------------------------\n\n")

    return final_output  

# For a single PDF
def extract_pdf_single(pdf_path: str) -> str:
    pdfFileObject = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObject)
    output = "Research Paper: "
    for i in range(len(pdfReader.pages)):
        pageObj = pdfReader.pages[i]
        output += pageObj.extract_text()
    return output

if __name__ == "__main__":
    str = extract_pdf_folder('/Users/nisarg/Desktop/Kgp_pathway/Benchmark')
    for (root,dirs,files) in os.walk('/Users/nisarg/Downloads/Papers', topdown=True):
        print (root)
        print (dirs)
        print (files)
        print ('--------------------------------')