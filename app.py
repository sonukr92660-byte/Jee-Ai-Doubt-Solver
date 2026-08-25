import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🤖 JEE AI DOUBT SOLVER")
st.write("Upload or scan a Physics, Chemistry, or Maths question to get an instant step-by-step solution.")

# --- स्टेप 1: एआई की सेटिंग्स ---
api_key = st.text_input("Enter your Gemini API Key (Optional):", type="password")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please enter a Google Gemini API key to activate the solver.")

# --- स्टेप 2: कैमरा और इमेज इनपुट ---
st.write("---")
st.write("### 📸 Scan Your Question")
uploaded_file = st.file_uploader("Choose an image of the question...", type=["jpg", "jpeg", "png"])
camera_file = st.camera_input("Or take a photo of the question directly")

target_image = None
if uploaded_file is not None:
    target_image = Image.open(uploaded_file)
elif camera_file is not None:
    target_image = Image.open(camera_file)

# --- स्टेप 3: एआई प्रोसेसिंग और आउटपुट ---
if target_image is not None:
    st.image(target_image, caption="Uploaded Question Screen.", use_container_width=True)
    
    if st.button("Solve with AI"):
        if not api_key:
            st.error("Cannot solve! API Key is missing. Please provide a Gemini API Key above.")
        else:
            st.write("🔄 Analyzing the question and generating solution...")
            
            try:
                # यहाँ हमने पुराना मॉडल बदलकर नया 'gemini-2.5-flash' कर दिया है
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = (
                    "You are an expert IIT-JEE professor. Analyze this image carefully. "
                    "Extract the text of the physics, chemistry, or mathematics question from it. "
                    "Provide a highly accurate, step-by-step clear solution. State the core formulas "
                    "used first, then provide the breakdown, and output the final answer clearly."
                )
                
                response = model.generate_content([prompt, target_image])
                
                st.write("---")
                st.write("### 📝 Step-by-Step Solution:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred while connecting to AI: {e}")

