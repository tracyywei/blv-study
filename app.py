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

st.title("Alt-Text BLV Study")

random.seed(time.time())
data_shuffled = data.sample(frac=1, random_state=42).reset_index(drop=True)

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
        st.experimental_rerun()
elif st.session_state.current_step == 1:
    # Step 2: Rate alt-text options
    alt_text_variants = {
        "yes_crt_yes_cnxt": row["yes_crt_yes_cnxt"],
        "other_alttext": row["other_alttext"]
    }
    shuffled_variants = list(alt_text_variants.items())
    random.shuffle(shuffled_variants)

    if st.session_state.alt_text_index < len(shuffled_variants):
        alt_text_key, alt_text_value = shuffled_variants[st.session_state.alt_text_index]
        st.subheader(f"Alt Text {st.session_state.alt_text_index + 1} of {len(shuffled_variants)}")
        st.write(f"{re.sub('Alt text: ', '', alt_text_value)}")

        # Rating scales using dropdowns
        quality = st.selectbox(
            "Rate the quality of this description (1-Low, 5-High):",
            options=[1, 2, 3, 4, 5],
            key=f"quality_{st.session_state.alt_text_index}"
        )
        imaginability = st.selectbox(
            "Rate how easy it is to imagine the image from this description (1-Low, 5-High):",
            options=[1, 2, 3, 4, 5],
            key=f"imaginability_{st.session_state.alt_text_index}"
        )
        relevance = st.selectbox(
            "Rate the relevance of this description to the image (1-Low, 5-High):",
            options=[1, 2, 3, 4, 5],
            key=f"relevance_{st.session_state.alt_text_index}"
        )
        plausibility = st.selectbox(
            "Rate the plausibility of this description (1-Low, 5-High):",
            options=[1, 2, 3, 4, 5],
            key=f"plausibility_{st.session_state.alt_text_index}"
        )

        if st.button("Next Alt Text", key=f"next_alt_text_{st.session_state.alt_text_index}"):
            # Save the ratings (replace with your actual saving logic)
            # Example:
            # sheet.append_row([
            #     st.session_state.progress + 1,
            #     row["image_name"],
            #     alt_text_key,
            #     quality,
            #     imaginability,
            #     relevance,
            #     plausibility,
            #     time.time()
            # ])
            st.session_state.alt_text_index += 1
            st.experimental_rerun()
    else:
        # All alt texts rated, move to the next image
        if st.button("Next Image", key="next_image_after_ratings"):
            st.session_state.progress += 1
            st.session_state.current_step = 0  # Reset to image/context step
            st.experimental_rerun()