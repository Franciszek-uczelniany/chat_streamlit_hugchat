import os

import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from tools.chatpdf import chatpdf as chatpdf
from streamlit_chat import message

st.set_page_config(
    page_title="ChatPDF",
    page_icon="📄",
)

st.title('📄 ChatPDF')

# st.markdown('''Submit your PDF file and chat with it!''')

pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", type=['pdf'], accept_multiple_files=True)

if pdf_docs is not None:
    for pdf_doc in pdf_docs:
        with open(os.path.join("docs", pdf_doc.name), "wb") as f:
            f.write(pdf_doc.getbuffer())

if st.button('Process'):
    chatpdf.index_documents("docs")


if 'generated_chatpdf' not in st.session_state:
    st.session_state['generated_chatpdf'] = ["I'm HugChat, How may I help you?"]
## past stores User's questions
if 'past_chatpdf' not in st.session_state:
    st.session_state['past_chatpdf'] = ['Hi!']

# Layout of input/response containers
response_container_chatpdf = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container_chatpdf = st.container()

# User input
## Function for taking user provided prompt as input
def get_text_chatpdf():
    input_text_chatpdf = st.text_input("You: ", "", key="input_chatpdf")
    return input_text_chatpdf
## Applying the user input box
with input_container_chatpdf:
    user_input_chatpdf = get_text_chatpdf()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response_chatpdf(prompt):
    response_chatpdf = chatpdf.my_chatGPT_bot(prompt)
    return response_chatpdf

## Conditional display of AI generated responses as a function of user provided prompts
with response_container_chatpdf:
    if user_input_chatpdf:
        response_chatpdf = generate_response_chatpdf(user_input_chatpdf)
        st.session_state.past_chatpdf.append(user_input_chatpdf)
        st.session_state.generated_chatpdf.append(response_chatpdf)
        
    if st.session_state['generated_chatpdf']:
        for i in range(len(st.session_state['generated_chatpdf'])):
            message(st.session_state['past_chatpdf'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated_chatpdf"][i], key=str(i))