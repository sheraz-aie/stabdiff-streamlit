
import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Initialize session state for the prompt if it doesn't exist
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""

# Set page title
st.set_page_config(page_title="AIE Image Creator")

# Main title
st.markdown("<h1 style='font-size:40px;'>AI Image Creator</h1>", unsafe_allow_html=True)

# Function to clear prompt
def clear_prompt():
    st.session_state.prompt = ""

# Button to clear previous prompt

    
# Main area - Prompts using session state
prompt = st.text_area("Enter Image Description (Prompt)", value=st.session_state.prompt, key="prompt_input")

# Update session state when text area changes
st.session_state.prompt = prompt

negative_prompt = st.text_area("Enter Negative Prompt (optional)", "ugly, deformed, low quality")
if st.button("Clear Prompt"):
    clear_prompt()
# Sidebar configuration
st.sidebar.markdown("<h1 style='font-size:80px;'>AIE</h1>", unsafe_allow_html=True)

# Move controls to sidebar
inference_steps = st.sidebar.number_input("Number of Inference Steps", min_value=1, max_value=50, value=20)
guidance_scale = st.sidebar.slider("Guidance Scale", min_value=1.0, max_value=10.0, value=7.5, step=0.1)

# Generate button in sidebar
if st.sidebar.button("Generate Image"):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "num_inference_steps": inference_steps,
        "guidance_scale": guidance_scale
    }
    
    try:
        response = requests.post("http://52.224.63.177:9002/generate", json=payload)
        
        if response.status_code == 200:
            
            # Create an image from the binary response content
            image = Image.open(BytesIO(response.content))
            
            # Display image in main area
            st.image(image, caption="Generated Image", use_container_width=True)
            
        else:
            st.error(f"Server returned error status: {response.status_code}")
            st.write(f"Response content: {response.text[:500]}")
    except Exception as e:
        st.error(f"Error: {e}")
