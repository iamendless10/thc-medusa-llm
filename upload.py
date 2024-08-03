import gradio as gr
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import PyPDF2
import streamlit as st

# API Key
GROQ_API_KEY = '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'

# Define the chain with the LangChain setup
chat = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768")
system = ("You are a helpful assistant specializing in providing medical advice and recommending doctors. "
          "You should never answer any questions other than medical related queries. "
          "Please note that this chatbot is intended for providing medical advice only. "
          "You are knowledgeable, empathetic, and adhere to medical guidelines. "
          "For any medical advice, you should also recommend visiting SIMS Hospital for a comprehensive evaluation."
          "If user asks any questions other than medical queries, say 'Sorry, I could not help you with that.'")
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

# Function for the main chatbot
def chatbot(user_input):
    response = chain.invoke({"text": user_input})
    return response.content

# Function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text

# Function to handle PDF uploads and interaction
def handle_pdf_interaction(pdf_file, user_question):
    if pdf_file:
        pdf_text = extract_pdf_text(pdf_file)
        # Display the extracted text
        pdf_pages = pdf_text.split('\n\n')
        page_content = pdf_pages[0] if pdf_pages else "No content extracted"
    else:
        page_content = "Please upload a PDF file."

    if user_question:
        response = chain.invoke({"text": user_question})
        answer = response.content
    else:
        answer = "Please enter a question related to the PDF."

    return page_content, answer

# Create the Gradio interface
with gr.Blocks() as demo:
    with gr.Tab("Chatbot"):
        gr.Interface(fn=chatbot, inputs=gr.Textbox(label='Enter your query here'), outputs="text", title="SIMS Chatbot").launch()

    with gr.Tab("PDF Interaction"):
        pdf_file_input = gr.File(label="Upload your medical literature (PDF only)", file_types=["pdf"])
        pdf_content_output = gr.Textbox(label="PDF Page Content", lines=20, interactive=False)
        pdf_question_input = gr.Textbox(label="Ask a question related to the PDF")
        pdf_answer_output = gr.Textbox(label="Assistant's Response", lines=10, interactive=False)

        gr.Interface(
            fn=handle_pdf_interaction,
            inputs=[pdf_file_input, pdf_question_input],
            outputs=[pdf_content_output, pdf_answer_output],
            live=True
        ).launch()

demo.launch()
