import streamlit as st
import numpy as np
import tensorflow as tf

def load_model():
    model = tf.keras.models.load_model('./models/model.h5', compile=False)
    return model

# Load the model
model = load_model()


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Friendly welcome
st.title("Welcome to the Hypothyroid Detection App!")

# User-friendly file upload prompt
uploaded_file = st.file_uploader("Please upload your .npy file for analysis", type=['npy'], key="file_uploader")

# Variable to track if the user has uploaded a file
file_uploaded = False

# Check if the user uploaded a file
if uploaded_file:
    file_uploaded = True

    # Load .npy file
    data = np.load(uploaded_file)

    # Reshape data
    data_reshaped = np.reshape(data, (1, 28, 1))

    # Make prediction
    predictions = (model.predict(data_reshaped) > 0.5).astype("int32")

    # Determine class
    # Assuming predictions is a 2D array

    if predictions[0][0] == 0:
        # Positive outcome: User is healthy
        st.experimental_set_query_params(healthy=True, thyroid=False)
    else:
        # Negative outcome: Potential thyroid issue
        st.experimental_set_query_params(healthy=False, thyroid=True)

# Content based on URL parameters only when a file has been uploaded
if file_uploaded:
    params = st.experimental_get_query_params()
    if 'healthy' in params and params['healthy'][0] == 'True':
        # Positive outcome content
        st.header("Great news! You seem to be in good health.")
        st.success("It's always good to prioritize your well-being.")
        st.subheader("Suggestions for maintaining a healthy lifestyle:")
        st.markdown("- Maintain a balanced diet with a variety of nutrients.")
        st.markdown("- Stay physically active and incorporate exercise into your routine.")
        st.markdown("- Ensure you get sufficient sleep for overall well-being.")
        st.markdown("- Manage stress through relaxation techniques or activities you enjoy.")
    elif 'thyroid' in params and params['thyroid'][0] == 'True':
        # Negative outcome content
        st.header("There might be a concern with your thyroid.")
        st.error("It's recommended to consult with a healthcare professional for further evaluation.")
        st.subheader("Possible next steps:")
        st.markdown("- Schedule an appointment with a healthcare provider for detailed assessment.")
        st.markdown("- Consider additional medical tests if recommended by your healthcare professional.")
        st.markdown("- Follow the advice provided by your healthcare provider for proper management.")
