#streamlit UI in browser

import streamlit as st
from PIL import Image
from src.tamper import tamper_detection


def main():
    st.title("Image Tampering Detection")
    
    uploaded_file = st.file_uploader("Upload Image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        input_image_name = uploaded_file.name
        saved_file_path = tamper_detection.save_uploaded_file(uploaded_file)

        if st.button("Annotate Image"):
            annotated_img, output_path = tamper_detection.annotate_and_save_image(saved_file_path, input_image_name)
            if annotated_img is not None:
                st.success("Process complete")
                st.image(annotated_img, caption='Annotated Image', use_column_width=True)

                st.success(f"Annotated image saved to {output_path}")
            else:
                st.warning("No tampering detected in the image.")

if __name__ == "__main__":
    main()
