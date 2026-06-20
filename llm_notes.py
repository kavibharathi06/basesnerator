from transformers import pipeline
import streamlit as st


@st.cache_resource
def load_model():

    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6",
        framework="pt",
        device=-1
    )

    return summarizer


def generate_notes(text):

    text = text.strip()

    if len(text.split()) < 30:

        return {
            "notes":
            "Not enough readable text."
        }

    text = text[:1000]

    summarizer = load_model()

    result = summarizer(

        text,

        max_length=100,
        min_length=30,
        truncation=True,
        do_sample=False

    )

    return {

        "notes":
        result[0]["summary_text"]

    }