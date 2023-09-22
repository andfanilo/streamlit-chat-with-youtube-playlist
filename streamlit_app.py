"""
Chat with transcripts stored by Llamaindex in Weaviate Cloud
"""
import openai
import streamlit as st
import weaviate
from llama_index import ServiceContext
from llama_index import VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.vector_stores import WeaviateVectorStore

st.set_page_config(
    page_title="Chat with my Youtube Channel",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

openai.api_key = st.secrets["OPENAI_API_KEY"]

weaviate_index = "LlamaIndex"


def init_session_state():
    if "messages" not in st.session_state.keys():
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Ask me a question"}
        ]


@st.cache_resource(show_spinner=False)
def load_weaviate_client():
    client = weaviate.Client(
        url=st.secrets["WEAVIATE_URL"],
        auth_client_secret=weaviate.AuthApiKey(api_key=st.secrets["WEAVIATE_API_KEY"]),
        additional_headers={"X-OpenAI-Api-Key": st.secrets["OPENAI_API_KEY"]},
    )
    return client


@st.cache_resource(show_spinner=False)
def load_weaviate_llamaindex(index_name: str):
    weaviate_client = load_weaviate_client()

    if not weaviate_client.schema.exists(index_name):
        st.error(
            f"Index / Weaviate class {index_name} does not exist. Please build it beforehand"
        )
        st.stop()

    vector_store = WeaviateVectorStore(
        weaviate_client=weaviate_client, index_name=index_name
    )
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2,
            system_prompt="You are an expert on the Streamlit Python library. Your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts. Do not hallucinate features.",
        )
    )
    loaded_index = VectorStoreIndex.from_vector_store(
        vector_store, service_context=service_context
    )
    return loaded_index


def display_chat_history():
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])


st.header("Chat with my Youtube Channel")

init_session_state()

index = load_weaviate_llamaindex(weaviate_index)
chat_engine = index.as_chat_engine(
    chat_mode="condense_question", verbose=True
)

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
)

# Display the prior chat messages
display_chat_history()

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {
                "role": "assistant", 
                "content": response.response
            }
            st.session_state.messages.append(message)  # Add response to message history
