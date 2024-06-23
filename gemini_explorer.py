import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = 'bubbly-access-427200-f3'
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature = 0.4
)

# Loading the model with the configuration
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

chat = model.start_chat()

# Helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })
    st.session_state.messages.append({
        "role": "model",
        "content": output
    })

st.title("Gemini Explorer")

# Initializing the Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# To display and load the Chat History
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message['role'],
        parts = [Part.from_text(message['content'])]
    )

    chat.history.append(content)

# For initial message startup
if len(st.session_state.messages) == 0:
    initial_prompt = f"Introduce yourself as ReX, an AI assistant powered by Geminin Pro. You use emojis to be interactive."
    llm_function(chat, initial_prompt)

# To capture the user's input
query = st.chat_input("Message ReX")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(chat, query)
