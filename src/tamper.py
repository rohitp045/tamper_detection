

from ultralytics import YOLO
import cv2
import os
import streamlit as st

save_folder = "upload_files"
os.makedirs(save_folder,exist_ok=True)
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# colors for annot
class_colors = {
    0: (0, 0, 255),   # Red for 'Whitener'
    1: (0, 255, 0),   # Green for 'Overwriting'
    # 2: (255, 0, 0),   # Blue for 'Re-writing'
    2 :(0, 0, 255), 
    3: (0, 255, 255)  # Yellow for 'Erase'
}

class tamper_detection:

    def save_uploaded_file(uploaded_file):
        # os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path

    def annotate_and_save_image(input_image_path, output_image_name):
        # Initialize the progress bar in Streamlit

        st.write ("Tamper Cheaking in progress...")
        progress_bar = st.progress(0)
        
        model = YOLO("tamper_model.pt")
        results = model.predict(input_image_path)

        if results[0].boxes is not None:
            tampering_classes = [0, 1, 2, 3]
            annotated_img = results[0].orig_img.copy()

            total_boxes = len(results[0].boxes)  
            progress_increment = 1 / total_boxes if total_boxes > 0 else 1

            for idx, box in enumerate(results[0].boxes):
                cls = int(box.cls.item())
                if cls in tampering_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    label = results[0].names[cls]
                    color = class_colors.get(cls, (255, 255, 255))
                    cv2.rectangle(annotated_img, (x1, y1), (x2, y2), color, 6)
                    cv2.putText(annotated_img, f'{label}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.5, color, 6)
                
                # Update the progress bar after each box is processed
                progress_bar.progress(min((idx + 1) * progress_increment, 1.0))
            
            # os.makedirs("output", exist_ok=True)
            output_image_path = os.path.join(output_folder, output_image_name)
            cv2.imwrite(output_image_path, annotated_img)
            
            # Indicate completion of progress bar
            progress_bar.progress(1.0)
            
            return annotated_img, output_image_path
        else:
            progress_bar.progress(1.0)  # If no boxes were found, just complete the progress bar
            return None, None