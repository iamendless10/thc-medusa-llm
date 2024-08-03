import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import PyPDF2 
import keys

chat = ChatGroq(temperature=0, groq_api_key=keys.GROQ_API_KEY, model_name="mixtral-8x7b-32768")
system = ("You are a helpful assistant specializing in providing medical advice and recommending doctors. "
          "You should never answer any questions other than medical related queries. "
          "Please note that this chatbot is intended for providing medical advice only. "
          "You are knowledgeable, empathetic, and adhere to medical guidelines. "
          "For any medical advice, you should also recommend only one hospital from the following list after successfully answering the query: ['G Kuppuswami Naidu Memorial Hospital', 'PSG Hospital', 'Sri Ramkrishna Hospital', 'Kovai Medical Centre and Hospital'] "
          "If user asks any questions other than medical queries, say 'Sorry, I could not help you 1with that.'")
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'response' not in st.session_state:
    st.session_state.response = ""
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

def generate_youtube_search_url(query):
    base_url = "https://www.youtube.com/results"
    return f"{base_url}?search_query={query.replace(' ', '+')}"

def extract_pdf_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

st.set_page_config(page_title="Medical Assistant Chatbot", page_icon=":microscope:")

st.sidebar.image("medical_logo.png", use_column_width=True)
st.sidebar.header("Additional Information")
st.sidebar.markdown(
    """
    **Disclaimer:** This chatbot provides general medical advice and recommendations. 
    It is not a substitute for professional medical advice, diagnosis, or treatment. 
    Always consult a healthcare provider for personalized medical advice.
    """
)

st.title("THC - MEDUSA")

user_input = st.text_input("You: ")

if st.button("Send"):
    if user_input:
        st.session_state.user_input = user_input
        response = chain.invoke({"text": user_input})
        st.session_state.response = response.content  
        st.session_state.user_query = user_input 

if st.session_state.response:
    st.markdown("### Response:")
    st.text_area("Assistant:", st.session_state.response, height=200)

    st.markdown("### Recommended YouTube Videos:")
    youtube_url = generate_youtube_search_url(st.session_state.user_query)
    st.markdown(f"[Search YouTube for '{st.session_state.user_query}']({youtube_url})")

# if st.button("Go to PDF Upload"):
#     st.query_params["page"] = "upload"
#     st.rerun()


# query_params = st.query_params
# if query_params.get("page") == "upload":
#     st.query_params["page"] = None  

#     # st.title("Upload Medical Literature")
#     uploaded_file = st.file_uploader("Upload your medical literature (PDF only)", type=["pdf"])

#     if uploaded_file is not None:
#         pdf_text = extract_pdf_text(uploaded_file)

#         pdf_pages = pdf_text.split('\n\n')
#         selected_page = st.selectbox("Select PDF Page", options=range(len(pdf_pages)))
#         st.text_area("PDF Page Content", value=pdf_pages[selected_page], height=400)

#         user_question = st.text_input("Ask a question related to the PDF")
#         if st.button("Get Answer"):
#             response = chain.invoke({"text": user_question})
#             st.text_area("Assistant's Response", response.content, height=200)