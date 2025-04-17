import streamlit as st
import pandas as pd
import random
import time
import re

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("blv-study-alttext-data.csv")
    return df

data = load_data()

random.seed(time.time())
data_shuffled = data.sample(frac=1).reset_index(drop=True)  # Shuffle the selected 6 images

if "current_step" not in st.session_state:
    st.session_state.current_step = 0  # Tracks whether the user is viewing the image/context or rating alt texts
if "progress" not in st.session_state:
    st.session_state.progress = 0  # Tracks the current image index
if "alt_text_index" not in st.session_state:
    st.session_state.alt_text_index = 0  # Tracks which alt text is being rated

total_images = len(data_shuffled)

if st.session_state.progress >= total_images:
    st.success("You have completed the study! Thank you for participating.")
    st.stop()

row = data_shuffled.iloc[st.session_state.progress]

if st.session_state.current_step == 0:
    # Step 1: Show image and context
    st.subheader(f"Image {st.session_state.progress + 1} of {total_images}")
    st.image(
        row["image_url"],
        caption=f"Image {st.session_state.progress + 1}",
    )
    st.write(f"**Article Title:** {re.sub('_', ' ', row['article_title'])}")
    st.write(f"**Context:** {row['context']}")
    if st.button("Next", key="next_image", help="Go to the alt-text rating step"):
        st.session_state.current_step = 1  # Move to alt-text rating
        st.session_state.alt_text_index = 0  # Reset alt text index
        st.rerun()
elif st.session_state.current_step == 1:
    # Step 2: Show alt-text options
    alt_text_variants = {
        "yes_crt_yes_cnxt": row["yes_crt_yes_cnxt"],
        "other_alttext": row["other_alttext"]
    }
    shuffled_variants = list(alt_text_variants.items())
    random.shuffle(shuffled_variants)

    if st.session_state.alt_text_index < len(shuffled_variants):
        # Show individual alt text
        alt_text_key, alt_text_value = shuffled_variants[st.session_state.alt_text_index]
        st.subheader(f"Alt Text {st.session_state.alt_text_index + 1} of {len(shuffled_variants)}")
        st.write(f"{re.sub('Alt text: ', '', alt_text_value)}")

        if st.button("Next Alt Text", key=f"next_alt_text_{st.session_state.alt_text_index}"):
            st.session_state.alt_text_index += 1
            st.rerun()
    elif st.session_state.alt_text_index == len(shuffled_variants):
        # Show both alt texts side by side
        st.subheader("Compare Alt Texts")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Alt Text 1**")
            st.write(f"{re.sub('Alt text: ', '', shuffled_variants[0][1])}")

        with col2:
            st.write("**Alt Text 2**")
            st.write(f"{re.sub('Alt text: ', '', shuffled_variants[1][1])}")

        if st.button("Next Image", key="next_image_after_comparison"):
            st.session_state.progress += 1
            st.session_state.current_step = 0  # Reset to image/context step
            st.session_state.alt_text_index = 0  # Reset alt text index
            st.rerun()
