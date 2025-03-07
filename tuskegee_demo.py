import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import base64
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import re  # Import the regular expression module

# Load environment variables

# Access the Groq API key
groq_api_key = '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'

try:
    with open(R"C:\Users\visha\Downloads\zoning_context.txt", "r") as f:
        zoning_context = f.read()
except FileNotFoundError:
    st.error("Error: zoning_context.txt not found. Please create the file and put the zoning information inside.")
    st.stop()  # Stop the app if the file is not found
except Exception as e:
    st.error(f"An error occurred while reading zoning_context.txt: {e}")
    st.stop()


try:
    with open(R"C:\Users\visha\Downloads\permit.txt", "r") as f:
        permits = f.read()
except FileNotFoundError:
    st.error("Error: zoning_context.txt not found. Please create the file and put the zoning information inside.")
    st.stop()  # Stop the app if the file is not found
except Exception as e:
    st.error(f"An error occurred while reading zoning_context.txt: {e}")
    st.stop()


try:
    with open(R"C:\Users\visha\Downloads\permit.txt", "r") as f:
        permits = f.read()
except FileNotFoundError:
    st.error("Error: zoning_context.txt not found. Please create the file and put the zoning information inside.")
    st.stop()  # Stop the app if the file is not found
except Exception as e:
    st.error(f"An error occurred while reading zoning_context.txt: {e}")
    st.stop()

try:
    with open(R"C:\Users\visha\Downloads\infrastructure.txt", "r") as f:
        grants = f.read()
except FileNotFoundError:
    st.error("Error: zoning_context.txt not found. Please create the file and put the zoning information inside.")
    st.stop()  # Stop the app if the file is not found
except Exception as e:
    st.error(f"An error occurred while reading zoning_context.txt: {e}")
    st.stop()


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
    #page_title="Groq-Powered Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Streamlit app
#st.title("Groq-Powered Chatbot with Streaming Responses")

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

# Initialize session state for the pdf upload
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# Function to check if the input contains an address-like pattern
def is_address_in_input(user_input):
    """
    Checks if the user input contains a pattern that looks like an address.
    (This is a basic check; more sophisticated patterns could be added).
    """
    address_pattern = r"\d+\s+\w+\s+\w+"  # e.g., "123 Main Street"
    return bool(re.search(address_pattern, user_input))

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
    
   # st.markdown("""
   #     <h5 class='quick-actions-title'>Quick Actions</h5>
   # """, unsafe_allow_html=True)
    
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
        if st.button("Check Zoning Rules", key="ai_button"):
            st.session_state.prefilled_input = "What are the zoning rules?"
            st.session_state.context = zoning_context

        if st.button("Approved Plans Program    ", key="approved plans"):
            st.session_state.prefilled_input = "What is the Approved Plans Program?"
            st.session_state.context = (
                "The Approved Plans Program is a program within the City of Tuskegee that allows applicants to submit site plans, building plans, or other related plans to be reviewed by the City. "
            )

        if st.button("Grant Finder", key="groq_button"):
            st.session_state.prefilled_input = "Give me a proposal for an open grant"
            st.session_state.context = grants

    # Second column of buttons (3 buttons)
    with col2:
        if st.button("Apply for a Permit", key="permit"):
            st.session_state.prefilled_input = "Tell me about this permit"
            st.session_state.context = permits

        if st.button("Spot Zoning/Variances", key="blockchain_button"):
            st.session_state.prefilled_input = "What are spot zoning and variances?"
            st.session_state.context = (
                "Spot zoning is the application of zoning regulations to a specific piece of property, and it is often contrary to the general zoning plan. A variance is a permitted deviation from the current zoning regulations."
            )

        if st.button("View Master Plan", key="image_button"):
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
    
    # Display conversation history if the flag is True
    if st.session_state.show_conversation_history:
        st.markdown("### Conversation History")
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
             # Determine the icon based on the role
            if role == "user":
                icon = "👤"  # User icon
            elif role == "assistant":
                icon = "🤖"  # Assistant icon
            else:
                icon = ""  # Default (no icon)

            # Display the message with the icon
            st.markdown(f"- {icon} {role.capitalize()}: {content}")

    # Initialize session state for pre-filled input and context if not already set
    if 'prefilled_input' not in st.session_state:
        st.session_state.prefilled_input = ""

    if 'context' not in st.session_state:
        st.session_state.context = ""
    

    # Placeholder for displaying the bot's response
    response_placeholder = st.empty()
    
    # Add PDF upload button
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    # Chat input for user question (pre-filled with session state)
    user_input = st.chat_input("Ask a question:")
   
    tmp_file_path = None
        # Handle PDF upload
    if uploaded_file is not None and not st.session_state.pdf_uploaded:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Read PDF
            pdf_loader = PyPDFLoader(tmp_file_path)
            docs = pdf_loader.load()
            
            st.session_state.context = ""
            for doc in docs:
                st.session_state.context += doc.page_content
            st.session_state.pdf_uploaded = True
            st.success("PDF uploaded successfully.")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
        finally:
            if tmp_file_path:
                os.remove(tmp_file_path)


    # Handle pre-filled input
    if st.session_state.prefilled_input:
        user_input = st.session_state.prefilled_input
        st.session_state.prefilled_input = ""

    # Handle user input
    if user_input:
        # Display the user's message in the conversation history format
        st.session_state.messages.append({"role": "user", "content": user_input})

        #setting the context
        if is_address_in_input(user_input) and st.session_state.prefilled_input != "Tell me about this permit":
            st.session_state.context = zoning_context.split("**R2")[0]
        
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

            # Display the bot's response in the conversation history format
        st.session_state.messages.append({"role": "assistant", "content": full_response})
