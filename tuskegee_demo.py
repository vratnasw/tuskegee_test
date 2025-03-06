import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import time
import base64

# Load environment variables
load_dotenv()

# Access the Groq API key
groq_api_key = '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'

# Initialize Groq LLM using ChatGroq
llm = ChatGroq(api_key=groq_api_key, model_name="mixtral-8x7b-32768")

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["history", "question", "context"],
    template="""
    You are an AI assistant that only uses the provided context to answer questions.
    Do not use any external knowledge or general training data.
    
    Conversation History:
    {history}

    Context:
    {context}

    Question: {question}
    Answer:
    """
)

# Create the LLM chain
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

# Set page configuration with custom icon
st.set_page_config(
    page_title="Groq-Powered Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Streamlit app
st.title("Groq-Powered Chatbot with Streaming Responses")

# Add a centered logo at the top of the app, shifted to the left
logo_path = r"C:\Users\visha\Downloads\tuskegee_logo.png"  # Corrected file path
if os.path.exists(logo_path):
    try:
        with open(logo_path, "rb") as image_file:
            logo_bytes = image_file.read()
        encoded = base64.b64encode(logo_bytes).decode()

        st.markdown("""
            <style>
            .logo-container {
                display: flex;
                flex-direction: column; /* Stack the image and text vertically */
                align-items: center; /* Center items horizontally */
                justify-content: center; /* Center items vertically */
                margin-left: -100px; /* Shift the logo 100px to the left */
                text-align: center;
            }
            .city-of-tuskegee{
                font-size: 20px;
            }
            </style>
        """, unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{encoded}" width="300">
                <p class="city-of-tuskegee">City of Tuskegee</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.warning(f"Failed to load logo from file: {logo_path}. Error: {e}")
        st.warning("Displaying the application without the logo.")
else:
    st.warning(f"Logo file not found at: {logo_path}")
    st.warning("Displaying the application without the logo.")


# Initialize session state for the image
if 'image_path' not in st.session_state:
    st.session_state.image_path = None

if 'show_conversation_history' not in st.session_state:
    st.session_state.show_conversation_history = True
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to check if the input contains "map"
def is_map_request(user_input):
    return "map" in user_input.lower()

# Create a container for the buttons
button_container = st.container()

with button_container:
    # Quick Actions section
    st.markdown("""
        <style>
        .quick-actions-title {
            text-align: left;
            color: green;
            font-size: 16px;
            margin-left: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <h5 class='quick-actions-title'>Quick Actions</h5>
    """, unsafe_allow_html=True)
    
    # Adjust the gap between columns using CSS
    st.markdown("""
        <style>
        .custom-columns {
            display: flex;
            column-gap: 50px;
        }
        .custom-button {
            width: 200px;
            height: 50px;
            text-align: center;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create two columns for the button grid
    col1, col2 = st.columns(2)

    # Wrap the columns in a div with the custom class
    st.markdown('<div class="custom-columns">', unsafe_allow_html=True)

    # First column of buttons (3 buttons)
    with col1:
        if st.button("What is AI?", key="ai_button", help="Click to learn about AI"):
            st.session_state.prefilled_input = "What is AI?"
            st.session_state.context = (
                "Artificial Intelligence (AI) refers to machines designed to perform tasks that typically require human intelligence, "
                "such as learning, reasoning, problem-solving, and decision-making. AI systems can be rule-based or learn from data using techniques like machine learning."
            )

        if st.button("Explain Machine Learning", key="ml_button", help="Click to learn about Machine Learning"):
            st.session_state.prefilled_input = "Explain Machine Learning"
            st.session_state.context = (
                "Machine learning is a subset of AI where computers learn from data without being explicitly programmed. "
                "It involves algorithms that improve over time as they are exposed to more data. Common types include supervised, unsupervised, and reinforcement learning."
            )

        if st.button("What is Groq?", key="groq_button", help="Click to learn about Groq"):
            st.session_state.prefilled_input = "What is Groq?"
            st.session_state.context = (
                "Groq is a company that specializes in high-performance computing hardware and software solutions, "
                "particularly for AI and machine learning workloads. Their technology focuses on delivering fast and efficient processing for large-scale models."
            )

    # Second column of buttons (3 buttons)
    with col2:
        if st.button("Tell me a joke", key="joke_button", help="Click to hear a joke"):
            st.session_state.prefilled_input = "Tell me a joke"
            st.session_state.context = (
                "Why don't scientists trust atoms? Because they make up everything!"
            )

        if st.button("How does blockchain work?", key="blockchain_button", help="Click to learn about blockchain"):
            st.session_state.prefilled_input = "How does blockchain work?"
            st.session_state.context = (
                "Blockchain is a decentralized digital ledger that records transactions across many computers. "
                "It uses cryptographic techniques to ensure security and immutability of data. Each block contains a list of transactions and links to the previous block, forming a chain."
            )

        if st.button("Show me an image", key="image_button", help="Click to see a local image"):
            # Path to the local image
            st.session_state.image_path = "local_image.jpg"

    # Close the custom div
    st.markdown('</div>', unsafe_allow_html=True)

# Display the local image if it exists in session state
if st.session_state.image_path:
    if os.path.exists(st.session_state.image_path):
        st.image(st.session_state.image_path, caption="Local Image", use_column_width=True)
    else:
        st.warning(f"Image file '{st.session_state.image_path}' not found. Please check the file path.")

# Create a container for the chat interface
chat_container = st.container()

with chat_container:
    # Initialize session state for pre-filled input and context if not already set
    if 'prefilled_input' not in st.session_state:
        st.session_state.prefilled_input = ""

    if 'context' not in st.session_state:
        st.session_state.context = ""

    # Placeholder for displaying the bot's response
    response_placeholder = st.empty()

    # Chat input for user question (pre-filled with session state)
    user_input = st.chat_input("Ask a question:")

    # Handle pre-filled input
    if st.session_state.prefilled_input:
        user_input = st.session_state.prefilled_input
        st.session_state.prefilled_input = ""

    # Handle user input
    if user_input:
         # Display the user's message
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Check if the input is a map request
        if is_map_request(user_input):
            # Respond with a textual description of the map
            full_response = (
                "You requested a map. Unfortunately, I cannot display images directly, but here is some guidance: "
                "To view a map, you can use an online mapping service like Google Maps or OpenStreetMap. "
                "Simply search for the location you're interested in, and you'll find detailed maps and directions."
            )
            response_placeholder.markdown(full_response)
            # Hide conversation history after showing the map-related response
            st.session_state.show_conversation_history = False
            st.session_state.context = ""
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            # Prepare the conversation history string (limit to last 5 messages)
            history_str = ""

            # Get the response from the LLM with streaming
            full_response = ""

            try:
                # Run the LLM chain with streaming, including the context
                for chunk in llm_chain.run(question=user_input, history=history_str, context=st.session_state.context, stream=True):
                    full_response += chunk
                    response_placeholder.markdown(full_response)
            except Exception as e:
                full_response = "Sorry, I encountered an issue while processing your request."
                response_placeholder.markdown(full_response)
                st.error(f"An error occurred: {e}")

            # Clear the context after the response is generated
            st.session_state.context = ""
            # Display the bot's response in the conversation history format
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    

    # Display conversation history if the flag is True
    if st.session_state.show_conversation_history:
        st.markdown("### Conversation History")
        for message in st.session_state.messages:
            st.markdown(f"- {message['role'].capitalize()}: {message['content']}")
