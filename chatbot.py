import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"
USER_NAME = "staple_ai_client"
LIST_OF_FEATURES=["Semantic Seach","Contextual Summarization"]
PREFERRED_TEXT_LENGTH=["Short","Medium","Long"]

st.title("Staple AI - LLM-powered Contextual Search and Summarization")


def show_loading_overlay(message="Uploading..."):
    loading_css = """
    <style>
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
    }
    </style>
    """
    st.markdown(loading_css, unsafe_allow_html=True)
    st.markdown(f"<div class='overlay'>{message}</div>", unsafe_allow_html=True)

def hide_loading_overlay():
    st.markdown("<style>.overlay { display: none; }</style>", unsafe_allow_html=True)

# Fetch documents list once
def fetch_documents():
    response = requests.get(f"{API_URL}/get_uploaded_documents")
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        st.error("Failed to fetch uploaded documents.")
        return []

# Store documents list in session state
if "documents" not in st.session_state:
    st.session_state.documents = fetch_documents()

left_col, right_col = st.columns([1, 2])

with left_col:
    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Store the selected document in session state
    if "selected_doc" not in st.session_state:
        st.session_state.selected_doc = None

    if "messages_shown" not in st.session_state:
        st.session_state.messages_shown = []
    
    if "messages_shown" not in st.session_state:
        st.session_state.messages_stored = []

    if "documents" not in st.session_state:
        st.session_state.documents = fetch_documents()

    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = False  # Track upload status

    # Display document selector from session state
    if st.session_state.documents:
        previous_doc = st.session_state.get("selected_doc", None)  # Store previous document

        st.session_state.selected_doc = st.selectbox("Select a document:", st.session_state.documents, key="document_selector")
        st.session_state.messages_shown = []
        
        # Reset messages ONLY when the selected document changes
        if previous_doc != st.session_state.selected_doc:
            st.session_state.messages_stored = []
        
        st.write(f"You selected: {st.session_state.selected_doc}")
    else:
        st.write("No documents uploaded yet.")

    if not uploaded_file: 
        st.session_state.file_uploaded = False

    if uploaded_file and not st.session_state.file_uploaded:  # Only upload if not already uploaded
        show_loading_overlay("Uploading document and triggering indexing...")
        try:
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{API_URL}/upload_document_and_trigger_indexing", files=files)
            hide_loading_overlay()  # Hide loading overlay after request

            if response.status_code == 200:
                st.success("Document uploaded successfully.")
                st.toast("Document upload and indexing completed!")

                # Refresh document list only after a successful upload
                st.session_state.documents = fetch_documents()
                st.session_state.file_uploaded = True  # Mark file as uploaded

                # Force rerun to update dropdown
                st.rerun()
            else:
                st.error(f"Failed to upload document: {response.text}")
        except Exception as e:
            hide_loading_overlay()
            st.error(f"An error occurred: {str(e)}")


with right_col:
    st.subheader("💬 Chat")
    
    selected_feature=st.selectbox("Choose feature: Search or Summarize ? ",LIST_OF_FEATURES,index=0)
    
    st.session_state.selected_feature=selected_feature
    
    if st.session_state.selected_feature == LIST_OF_FEATURES[1]:
        selected_length=st.selectbox("What's your preferred length of summary ? ",PREFERRED_TEXT_LENGTH,index=1)
        st.session_state.selected_length=selected_length
        
    # Ensure DOC_NAME is assigned properly
    DOC_NAME = st.session_state.selected_doc if st.session_state.selected_doc else ""

    if "messages_shown" not in st.session_state:
        st.session_state.messages_shown = []

    chat_css = """
    <style>
        .chat-container {
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .chat-message {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }
        .chat-user {
            background-color: #2B2B2B;
            padding: 12px;
            border-radius: 10px;
            color: white;
            flex: 1;
        }
        .chat-assistant {
            background-color: #3A3A3A;
            padding: 12px;
            border-radius: 10px;
            color: #FFD700;
            flex: 1;
        }
        .chat-icon {
            font-size: 24px;
            margin-right: 10px;
        }
    </style>
    """
    st.markdown(chat_css, unsafe_allow_html=True)

    for message in st.session_state.messages_shown:
        role_class = "chat-user" if message["role"] == "user" else "chat-assistant"
        icon = "👤" if message["role"] == "user" else "🤖"  # User and Assistant icons

        with st.container():
            st.markdown(f"""
                <div class='chat-message'>
                    <span class='chat-icon'>{icon}</span>
                    <div class='{role_class}'>{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)

    if prompt := st.chat_input("Ask a question..."):
        if not DOC_NAME:
            st.error("You must select the document first")
        else: 
            st.session_state.messages_shown.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            })
            
            st.session_state.messages_stored.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            })

            # Display user message immediately
            with st.container():
                st.markdown(f"""
                    <div class='chat-message'>
                        <span class='chat-icon'>👤</span>
                        <div class='chat-user'>{prompt}</div>
                    </div>
                """, unsafe_allow_html=True)

            with st.spinner("Thinking..."):
                if st.session_state.selected_feature == LIST_OF_FEATURES[0]:
                    print("messages_stored: ",st.session_state.messages_stored)
                    response = requests.post(f"{API_URL}/semantic_search/{DOC_NAME}", json={"list_of_messages": st.session_state.messages_stored})
                else:
                    print("messages_stored: ",st.session_state.messages_stored)
                    response = requests.post(f"{API_URL}/generate_summarization/{DOC_NAME}", json={
                        "list_of_messages": st.session_state.messages_stored,
                        "preferred_response_length":st.session_state.selected_length})

            assistant_response = "Error: Unable to get response from backend" if response.status_code != 200 else response.json().get('response', 'No response')

            # Display assistant response
            with st.container():
                st.markdown(f"""
                    <div class='chat-message'>
                        <span class='chat-icon'>🤖</span>
                        <div class='chat-assistant'>{assistant_response}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.session_state.messages_shown.append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            })
            
            st.session_state.messages_stored.append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            })
