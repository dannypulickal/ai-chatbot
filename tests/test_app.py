from unittest.mock import MagicMock, patch

from ai_chatbot.app import (
    display_chat_history,
    display_sidebar,
    handle_user_input,
    initialize_chain,
)


@patch("ai_chatbot.app.st")
@patch("ai_chatbot.app.ChatOpenAI")
@patch("ai_chatbot.app.ChatPromptTemplate")
@patch("ai_chatbot.app.StrOutputParser")
@patch("ai_chatbot.app.constants")
def test_initialize_chain(
    mock_constants, mock_parser, mock_template, mock_llm, mock_st
):
    # Mock constants
    mock_constants.MODEL = "gpt-4o"
    mock_constants.TEMPERATURE = 0.7
    mock_constants.SYSTEM_PROMPT = "You are a helpful AI assistant."
    # Mock session_state
    mock_st.session_state = MagicMock()

    # Call the function
    initialize_chain()

    # Assert that chain is set
    assert hasattr(mock_st.session_state, "chain")
    # Check that the components were called
    mock_llm.assert_called_once()
    mock_template.from_messages.assert_called_once()
    mock_parser.assert_called_once()


@patch("ai_chatbot.app.st")
def test_display_chat_history(mock_st):
    # Mock session_state with chat history
    from langchain_core.messages import AIMessage, HumanMessage

    mock_st.session_state = MagicMock()
    mock_st.session_state.chat_history = [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there"),
    ]
    mock_st.chat_message = MagicMock()
    mock_st.write = MagicMock()

    # Call the function
    display_chat_history()

    # Assert chat_message was called for user and assistant
    assert mock_st.chat_message.call_count == 2
    mock_st.chat_message.assert_any_call("user")
    mock_st.chat_message.assert_any_call("assistant")
    assert mock_st.write.call_count == 2


@patch("ai_chatbot.app.st")
def test_handle_user_input_no_input(mock_st):
    # Mock no input
    mock_st.chat_input.return_value = None
    mock_st.session_state = MagicMock()
    mock_st.session_state.chat_history = []

    # Call the function
    handle_user_input()

    # Assert no changes
    assert mock_st.session_state.chat_history == []


@patch("ai_chatbot.app.st")
def test_handle_user_input_with_input(mock_st):
    # Mock input
    mock_st.chat_input.return_value = "Test input"
    mock_st.session_state = MagicMock()
    mock_st.session_state.chat_history = []
    mock_st.chat_message = MagicMock()
    mock_st.spinner = MagicMock()
    mock_st.write = MagicMock()
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "Test response"
    mock_st.session_state.chain = mock_chain

    # Call the function
    handle_user_input()

    # Assert history updated
    assert len(mock_st.session_state.chat_history) == 2
    assert mock_st.session_state.chat_history[0].content == "Test input"
    assert mock_st.session_state.chat_history[1].content == "Test response"
    mock_chain.invoke.assert_called_once()


@patch("ai_chatbot.app.st")
def test_display_sidebar(mock_st):
    mock_st.sidebar = MagicMock()
    mock_sidebar = MagicMock()
    mock_st.sidebar.return_value.__enter__ = mock_sidebar
    mock_st.sidebar.return_value.__exit__ = MagicMock()
    mock_st.title = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    mock_st.subheader = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.rerun = MagicMock()

    # Call the function
    display_sidebar()

    # Assert sidebar elements called
    mock_st.title.assert_called_with("Options")
    mock_st.button.assert_called_with("Clear Chat")
    mock_st.subheader.assert_called_with("About")
    mock_st.markdown.assert_called_once()
