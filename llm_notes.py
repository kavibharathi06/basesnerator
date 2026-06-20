from transformers import pipeline
import streamlit as st


@st.cache_resource
def load_model():

    return pipeline(

        "summarization",

        model="sshleifer/distilbart-cnn-12-6"

    )


def generate_notes(text):

    text = text.strip()

    if len(text.split()) < 30:

        return {

            "notes":
            "Not enough readable text."
        }

    text = text[:1200]

    summarizer = load_model()

    result = summarizer(

        text,

        max_length=150,

        min_length=60,

        do_sample=False

    )

    return {

        "notes":

        result[0][
            "summary_text"
        ]

    }