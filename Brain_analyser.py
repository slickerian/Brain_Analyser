import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import os
from account import create_user_folder

model_file_path1 = "C:/Users/slick/OneDrive/Desktop/Brain_analyser/models/alzheimer_cnn_model.h5"
model_file_path2 = "C:/Users/slick/OneDrive/Desktop/Brain_analyser/models/BrainTumor10EpochsCategorical.h5"

def app():
    
    #Prediction for Alzheimer's
    def predict_label(img_path):
        test_image = Image.open(img_path).convert("L")
        test_image = test_image.resize((128, 128))
        test_image = np.array(test_image) / 255.0
        test_image = test_image.reshape(-1, 128, 128, 1)

        verbose_name = {
            0: "You don't have Alzheimer's Disease.",
            1: "You have Very Mildy Demented Alzheimer's Disease.",
            2: "You have Mildy Demented Alzheimer's Disease.",
            3: "You have Moderately Demented Alzheimer's Disease.",
        }
    
        if os.path.exists(model_file_path1):
            model1 = load_model(model_file_path1)
        else:
            st.write("Model file not found:", model_file_path1)
            st.stop()

        predict_x = model1.predict(test_image)
        classes_x = np.argmax(predict_x, axis=1)

        return verbose_name[classes_x[0]]



    #Prediction for Tumor
    if os.path.exists(model_file_path1):
            model2 = load_model(model_file_path2) 
    else:
        st.write("Model file not found:", model_file_path2)
        st.stop()

    def get_prediction(model2, image):  
        image = image.convert('RGB')
        image = image.resize((64, 64))
        image = np.array(image)
        input_img = np.expand_dims(image, axis=0)
        result = model2.predict(input_img)
        class_index = np.argmax(result)
        return class_index

    def get_className(classNo):
        if classNo == 0:
            return "No Brain Tumor Detected"
        elif classNo == 1:
            return "Brain Tumor Detected"




    def main():
        st.title("Brain Disease Prediction")
        st.write("Upload an MRI scan image for prediction")
        
        uploaded_file = st.file_uploader("Choose an MRI scan image...", type=["jpg", "png"])
        
        if uploaded_file is not None:
            # Get the username from the session state
            username = st.session_state.username

            # Create a folder for the user if it doesn't exist
            folder_name = create_user_folder(username)

            # Check if the folder was created successfully
            if folder_name:
                # Save the uploaded image to the user's folder
                image_path = os.path.join(folder_name, uploaded_file.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                st.success("Image saved successfully!")

                # Display the uploaded image
                st.image(uploaded_file, caption='Uploaded MRI scan.', use_column_width=True)
                st.write("")
                prediction1 = predict_label(image_path)
                st.write("##### Prediction 1: ",prediction1)

                image = Image.open(uploaded_file)
                prediction2 = get_prediction(model2, image)
                class_name = get_className(prediction2)   
                st.write(f"##### Prediction 2: {class_name}")

                if prediction1 in ["You have Very Mildy Demented Alzheimer's Disease.", "You have Mildy Demented Alzheimer's Disease.", "You have Moderately Demented Alzheimer's Disease."]:
                    # Draw a line under the predicted label
                    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
                    st.markdown("## Alzheimer's Disease")
                    st.write("**📌 Common Name:** Alzheimer's Disease")
                    st.write("**🌐 General Overview:** Alzheimer's Disease is a progressive neurodegenerative disorder that primarily affects memory and cognitive function.")
            
                if class_name == "Brain Tumor Detected":
                    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
                    st.markdown("## Brain Tumor")
                    st.write("**📌 Common Name:** Brain Tumor")
                    st.write("**🌐 General Overview:** A brain tumor is an abnormal growth of cells within the brain.")

            else:
                st.image(uploaded_file, caption='Uploaded MRI scan.', use_column_width=True)
                st.write("")
                prediction1 = predict_label(uploaded_file)
                st.write("##### Prediction 1: ",prediction1)

                image = Image.open(uploaded_file)
                prediction2 = get_prediction(model2, image)
                class_name = get_className(prediction2)   
                st.write(f"##### Prediction 2: {class_name}")

                if prediction1 in ["You have Very Mildy Demented Alzheimer's Disease.", "You have Mildy Demented Alzheimer's Disease.", "You have Moderately Demented Alzheimer's Disease."]:
                    # Draw a line under the predicted label
                    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
                    st.markdown("## Alzheimer's Disease")
                    st.write("**📌 Common Name:** Alzheimer's Disease")
                    st.write("**🌐 General Overview:** Alzheimer's Disease is a progressive neurodegenerative disorder that primarily affects memory and cognitive function.")
            
                if class_name == "Brain Tumor Detected":
                    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
                    st.markdown("## Brain Tumor")
                    st.write("**📌 Common Name:** Brain Tumor")
                    st.write("**🌐 General Overview:** A brain tumor is an abnormal growth of cells within the brain.")
                





    main()