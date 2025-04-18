import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("alttext.csv")
    return df

data = load_data()

# Use the dataset directly without shuffling
data_ordered = data.reset_index(drop=True)  # Ensure the dataset is in its original order

if "current_step" not in st.session_state:
    st.session_state.current_step = 0  # Tracks whether the user is viewing the image/context or rating alt texts
if "progress" not in st.session_state:
    st.session_state.progress = 0  # Tracks the current image index

total_images = 6

if st.session_state.progress >= total_images:
    st.success("You have completed the study! Thank you for participating.")
    st.stop()

row = data_ordered.iloc[st.session_state.progress]

if st.session_state.current_step == 0:
    # Step 1: Show image and context
    st.subheader(f"Image {st.session_state.progress + 1} of {total_images}")
    st.image(
        row["image_url"],
        caption=f"Image {st.session_state.progress + 1}",
        use_column_width=True  # Ensures the image fits the column width
    )
    st.write(f"**Article Title:** {re.sub('_', ' ', row['article_title'])}")
    # Clean the context by removing footnotes (e.g., [19])
    cleaned_context = re.sub(r"\[\d+\]", "", row["context"])
    st.write(f"**Context:** {cleaned_context}")
    if st.button("Next", key="next_image", help="Go to the alt-text comparison step"):
        st.session_state.current_step = 1  # Move to alt-text comparison
        st.rerun()

elif st.session_state.current_step == 1:
    # Step 2: Show both alt texts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Alt Text 1**")
        st.write(f"{re.sub('Alt text: ', '', row['alttext_1'])}")

    with col2:
        st.write("**Alt Text 2**")
        st.write(f"{re.sub('Alt text: ', '',  row['alttext_2'])}")

    if st.button("Next Image", key="next_image_after_comparison"):
        st.session_state.progress += 1
        st.session_state.current_step = 0  # Reset to image/context step
        st.rerun()
