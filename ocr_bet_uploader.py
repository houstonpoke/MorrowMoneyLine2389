import streamlit as st
from PIL import Image
import pytesseract

def upload_and_parse_bet():
    st.header("🧾 Upload Bet Screenshot")
    uploaded_file = st.file_uploader("Upload an image of your bet slip", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Extracting text with OCR..."):
            try:
                text = pytesseract.image_to_string(image)
                st.success("✅ OCR Text Extracted:")
                st.text_area("Bet Details:", value=text, height=200)
            except Exception as e:
                st.error(f"OCR failed: {e}")

def show_cover_status():
    st.subheader("📊 Real-Time Cover Status (Simulated)")
    st.info("This feature will show Red / Yellow / Green status based on live score feeds soon.")

