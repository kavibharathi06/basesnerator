def generate_notes(text):

    text = text.strip()

    if len(text.split()) < 20:

        return {
            "notes":
            "Not enough readable text."
        }

    try:

        from transformers import pipeline

        generator = pipeline(
            "summarization",
            model="Falconsai/text_summarization"
        )

        text = text[:1000]

        output = generator(
            text,
            max_length=80,
            min_length=20,
            do_sample=False
        )

        return {

            "notes":

            output[0][
                "summary_text"
            ]

        }

    except Exception:

        words = text.split()

        summary = " ".join(
            words[:120]
        )

        return {

            "notes":

f"""
Summary

{summary}
"""

        }