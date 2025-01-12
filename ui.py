import gradio as gr
import requests
import os
from loguru import logger 
from collections import deque
import json

HOST="127.0.0.1"
PORT="8001"

def make_visible():
    return gr.update(visible=True)

def success_message():
    return gr.update(value="Link uploaded successfully !!")

class ChatBot:
    def __init__(self):
        self.current_query = ""

    def upload_fastapi(self, file_input, drive_link):
        print(file_input)
        if file_input is None:
            return "No file uploaded."
        #send file path to FastAPI
        with open(file_input, "rb") as file:
            response = requests.post(
                url=f"http://{HOST}:{PORT}/upload?drive_link={drive_link}", 
                files={"file": file}
            ).text.strip('''"''')
        return gr.update(value=f"File uploaded successfully! \n" )    


    def chat(self, history):
        """Main chat function that processes queries and returns responses"""
        new_history= list(history) if history else [] 

        response = requests.get(
            f"http://{HOST}:{PORT}/process", 
        )
        json_response = json.loads(response.text)
        content_list = json_response["response"]
        logger.debug(type(content_list))
        logger.debug(content_list)
        result = f"Conference: {content_list[0]}  \n Reason: {content_list[1]}"
        new_history.append(["",result])
        return new_history
    
# Define custom CSS
css = """
body {
    background-size: cover;
}
.gradio-container {
    position: relative;
    height: 100vh;
    width: 100vw;
    background : url('/Users/nisarg/Downloads/pexels-jon-champaigne-622172690-27681652.jpg') no-repeat center center fixed;

}
.thinking-box {
    min-height: 400px !important;
    font-family: monospace;
    white-space: pre-wrap;>
    background-image: linear-gradient(to right, #131c2c, #2628aa);
    color: white !important;
}
.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 1rem;
}
.logo {
    position: absolute;
    left: 0rem;
    height: 40px;
    width: 40px;
    align-items: center;
    justify-content: center;
}
.title {
    font-size: 36px;
    font-weight: bold;
    margin: 0;
    padding: 0;
    text-align: left;
}
.input-container {
    display: flex;
    align-items: flex-start;
    color: white !important;
}
.upload-file {
    display: block;
    align-items: flex-start;
}
.submit-btn {
    min-height: 45px;
    background-image: linear-gradient(to right, #192058, #2628aa);
    color: white !important;
}
.search-btn {
    min-height: 45px;
    background-image: linear-gradient(to right, #1f2481, #2628aa);
    color: white !important;
}
.team-73 {
    color: blue !important;
}
.query-box {
    background-image: linear-gradient(to right,#192058, #2628aa);
    color: white !important;
}
.status {
    background-image: linear-gradient(to right, #131c2c, #2628aa);
}
"""

def clear_textbox(msg):
    return ""

# Gradio UI
def create_interface():
    bot = ChatBot()

    # Define interface
    with gr.Blocks(css=css, title='Pathway', fill_height=True, fill_width=True, theme=gr.themes.Soft()) as interface:
        # Header with logo and title
        with gr.Row(elem_classes=["header-container"]):
            with gr.Column(elem_classes=["header-container"], scale=5):
                gr.Image(
                    show_download_button=False,
                    show_fullscreen_button=False,
                    value="./assets/pathway_new.png",
                    elem_classes=["logo"],
                    show_label=False,
                    container=False
                )
            with gr.Column(elem_classes=["header-container"], scale=6):
                gr.Markdown(value = "# Team DRUGs", elem_classes=["team-73"])

        with gr.Row(height=400):
            with gr.Column():
                with gr.Row():
                    gr.Markdown("## ConEval AI", elem_classes=["title"])

                with gr.Row():    
                    chatbot = gr.Chatbot(
                        value=[],
                        #elem_id="chatbot",
                        height=400,
                        label="Chat Interface",
                        latex_delimiters=[{ "left": "$$", "right": "$$", "display": True }],
                    )

                with gr.Row(elem_classes=["input-container"]):
                    with gr.Column(scale=1, show_progress=True):
                        with gr.Row(elem_classes=["upload-file"], min_height=100):
                            link_upload = gr.Textbox(
                                show_label=False,
                                placeholder="Enter the google drive link",
                                lines=1,
                                #elem_id="msg-textbox",
                            )

                            file_upload = gr.File(
                                file_types=['.pdf','.json'], 
                                label="Upload your google drive credentials",
                                height=200,
                                visible=False
                            ) 
                           
                            upload_status = gr.Textbox( 
                                show_label=False, 
                                interactive=False,
                                container=False 
                            )               
                
                    with gr.Column(scale=3):
                        # with gr.Row(elem_classes=["input-container"]):
                        #     msg = gr.Textbox(
                        #         #label="Type your query here...",
                        #         show_label=False,
                        #         placeholder="Enter your query and press submit",
                        #         lines=12,
                        #         #elem_id="msg-textbox",
                        #     )

                        with gr.Row(elem_classes=["input-container"]):
                            submit = gr.Button(
                                "Submit", 
                                elem_classes=["submit-btn"]
                                )  

        submit.click(
                fn=bot.chat,
                inputs=[chatbot],
                outputs=[chatbot],
            ).then(
                fn=clear_textbox,
                inputs=[link_upload],
                outputs=[link_upload]
            )
        
        file_upload.upload(
                fn=bot.upload_fastapi,
                inputs=[file_upload, link_upload],
                outputs=[upload_status]
            )
        
        link_upload.submit(fn=make_visible,
                           outputs=[file_upload])

        return interface
    
demo=create_interface()
# Run Gradio
demo.load(show_progress=True)
demo.launch(debug=True, server_name=HOST)