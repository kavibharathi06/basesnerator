from transformers import pipeline


generator = pipeline(
    "summarization",
    model="Falconsai/text_summarization"
)


def generate_notes(text):

    if len(text.split()) < 20:

        return {
            "notes":
            "Not enough readable text."
        }

    text = text[:1000]

    output = generator(

        text,

        max_length=80,

        min_length=20,

        do_sample=False

    )

    return {

        "notes":
        output[0]["summary_text"]

    }