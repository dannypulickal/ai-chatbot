import os

import constants
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv()


def initialize_chain():
    """Initialize the LangChain conversation chain if not already present in 
    session state.

    Creates a ChatOpenAI LLM instance, a ChatPromptTemplate with system message,
    chat history placeholder, and human input, and combines them into a chain
    with a string output parser. Stores the chain in Streamlit session state.
    """
    if "chain" not in st.session_state:
        llm = ChatOpenAI(
            model=constants.MODEL,
            temperature=constants.TEMPERATURE,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", constants.SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        st.session_state.chain = prompt | llm | StrOutputParser()


def display_chat_history():
    """Display the chat history in the Streamlit app.

    Iterates through the messages in session state's chat_history and displays
    each HumanMessage as a user chat message and each AIMessage as an assistant
    chat message using Streamlit's chat_message and write components.
    """
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)


def handle_user_input():
    """Handle user input for the chatbot.

    Retrieves user input from Streamlit's chat_input. If input is provided,
    appends it to chat history, displays it, generates an AI response using
    the chain, displays the response, and appends it to chat history.
    """
    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chain.invoke(
                    {
                        "input": user_input,
                        "chat_history": st.session_state.chat_history,
                    }
                )
                st.write(response)

        st.session_state.chat_history.append(AIMessage(content=response))


def display_sidebar():
    """Display the sidebar with options and information.

    Creates a sidebar with a title, a 'Clear Chat' button that resets chat history
    and reruns the app, and an 'About' section with markdown text describing the app.
    """
    with st.sidebar:
        st.title("Options")

        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

        st.subheader("About")
        st.markdown("""
        AI Chatbot Application

        This module implements a simple AI chatbot using Streamlit for the UI,
        LangChain for conversation management, and OpenAI's GPT-4o model for responses.
        The app maintains chat history in session state and provides a sidebar for 
        options.
        """)


def __main__():
    """Main function to run the Streamlit AI chatbot app.

    Sets up the page configuration, initializes session state for chat history,
    and calls the functions to initialize the chain, display history, handle input,
    and display the sidebar.
    """
    st.set_page_config(page_title="AI Chatbot", layout="centered")
    st.subheader("Welcome to the AI Chatbot! Ask me anything.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    initialize_chain()
    display_chat_history()
    handle_user_input()
    display_sidebar()


if __name__ == "__main__":
    __main__()
