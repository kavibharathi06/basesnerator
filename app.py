import streamlit as st
import numpy as np
import cv2
import os

from scanner import scan_document
from pdf_export import create_pdf
from ocr import extract_text
from llm_notes import generate_notes
from text_cleaner import clean_text


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Snerator",
    page_icon="🧠",
    layout="wide"
)


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("🧠 Snerator")

    st.caption(
        "Scan → OCR → AI Notes"
    )

    st.divider()

    st.write(
        "Supported Formats"
    )

    st.write(
        "jpg, jpeg, png"
    )

    st.divider()

    st.write(
        "Features"
    )

    features = [

        "Document Scanner",
        "OCR",
        "AI Notes",
        "PDF Export"

    ]

    for f in features:

        st.checkbox(
            f,
            value=True,
            disabled=True
        )


# -----------------------------------
# HEADER
# -----------------------------------

st.title(
    "🧠 Snerator"
)

st.subheader(
    "Smart Notes Generator"
)

st.write(
"""
Upload images and convert them
into readable study notes.
"""
)

st.divider()


# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_files = st.file_uploader(

    "Upload Images",

    type=[
        "jpg",
        "jpeg",
        "png"
    ],

    accept_multiple_files=True

)

scanned_pages = []


# -----------------------------------
# DOCUMENT SCAN
# -----------------------------------

if uploaded_files:

    progress = st.progress(0)

    for i, uploaded in enumerate(
        uploaded_files
    ):

        progress.progress(
            (i + 1)
            /
            len(uploaded_files)
        )

        file = np.asarray(

            bytearray(
                uploaded.read()
            ),

            dtype=np.uint8

        )

        image = cv2.imdecode(

            file,

            cv2.IMREAD_COLOR

        )

        scanned = scan_document(
            image
        )

        st.subheader(
            f"Page {i+1}"
        )

        left, right = st.columns(2)

        with left:

            st.write(
                "Original"
            )

            st.image(

                cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                ),

                use_container_width=True

            )

        with right:

            st.write(
                "Scanned"
            )

            if scanned is not None:

                st.image(
                    scanned,
                    use_container_width=True
                )

                scanned_pages.append({

                    "scan":
                    scanned,

                    "original":
                    image

                })

            else:

                st.warning(
                    "Document not detected"
                )

    progress.empty()


# -----------------------------------
# STATUS
# -----------------------------------

if scanned_pages:

    st.divider()

    c1, c2 = st.columns(2)

    c1.metric(
        "Pages",
        len(
            scanned_pages
        )
    )

    c2.metric(
        "Status",
        "Ready"
    )


# -----------------------------------
# PDF EXPORT
# -----------------------------------

if scanned_pages:

    st.divider()

    if st.button(
        "📄 Export Scanned PDF"
    ):

        os.makedirs(
            "output",
            exist_ok=True
        )

        path = (
            "output/scanned_document.pdf"
        )

        create_pdf(

            [

                p["scan"]

                for p in scanned_pages

            ],

            path

        )

        with open(
            path,
            "rb"
        ) as f:

            st.download_button(

                "⬇ Download PDF",

                f,

                file_name="scanned_document.pdf",

                mime="application/pdf"

            )


# -----------------------------------
# GENERATE NOTES
# -----------------------------------

if scanned_pages:

    st.divider()

    st.subheader(
        "🧠 Generate Notes"
    )

    st.write(
        """
Generate clean study notes
from scanned pages.
"""
    )

    if st.button(
        "Generate Smart Notes"
    ):

        with st.spinner(
            "Scanning → OCR → Generating..."
        ):

            extracted = []
            
            # Keep track of words and total pages processed
            total_words = 0
            pages_used = 0

            # Loop through each page individually
            for i, page in enumerate(scanned_pages):

                text_scan = extract_text(
                    page["scan"]
                )

                text_original = extract_text(
                    page["original"]
                )

                # Pick whichever extraction gave us more text
                text = (
                    text_scan
                    if len(text_scan) > len(text_original)
                    else text_original
                )

                # Clean it up if it's long enough
                if len(text) > 100:
                    text = clean_text(text)

                # Skip pages that don't have enough readable words
                if len(text.split()) < 10:
                    continue

                # Add to our global list for the raw OCR viewer at the end
                extracted.append(f"--- Page {i+1} ---\n{text}")
                
                # Update stats counters
                total_words += len(text.split())
                pages_used += 1

                # -----------------------------------
                # GENERATE AND SHOW NOTES FOR THIS PAGE
                # -----------------------------------
                st.subheader(
                    f"📝 Generated Notes — Page {i+1}"
                )

                if len(text.split()) < 20:
                    st.warning(
                        f"Not enough readable text on Page {i+1} to generate a summary."
                    )
                else:
                    # Run the AI on ONLY this page's text
                    notes = generate_notes(text)
                    
                    st.markdown(
f"""
**Summary:**

{notes["notes"]}
"""
                    )
                
                st.divider()


            # -----------------------------------
            # GLOBAL STATS & RAW OCR DATA
            # -----------------------------------
            full_text = "\n\n".join(extracted)

            st.subheader(
                "📌 Document Stats"
            )

            c1, c2 = st.columns(2)

            c1.metric(
                "Total Words",
                total_words
            )

            c2.metric(
                "Pages Processed",
                pages_used
            )

            with st.expander(
                "🔍 View Raw OCR Text (All Pages)"
            ):

                st.text_area(
                    "Extracted Text",
                    full_text,
                    height=300
                )