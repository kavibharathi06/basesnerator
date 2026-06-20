import re


def clean_line(line):

    line = line.strip()

    line = re.sub(
        r"[^\w\s]",
        " ",
        line
    )

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line



def is_valid_topic(line):

    line_lower = line.lower()

    bad_starts = [

        "what",
        "why",
        "how",
        "when",
        "where",
        "who",
        "explain"

    ]

    words = line.split()

    if len(words) < 5:
        return False

    if words[0].lower() in bad_starts:
        return False

    if re.search(r"\b\d{4}\b", line):
        return False

    return True



def generate_questions(text):

    questions = []

    lines = text.split("\n")

    topics = []

    for line in lines:

        cleaned = clean_line(
            line
        )

        if is_valid_topic(
            cleaned
        ):

            topics.append(
                cleaned
            )

    for topic in topics[:4]:

        short = " ".join(
            topic.split()[:6]
        )

        questions.extend([

            f"Explain the concept of {short}.",

            f"What problem does {short} solve?",

            f"Why is {short} important?",

            f"What are the applications of {short}?",

            f"Compare {short} with traditional approaches."

        ])

    if len(questions) == 0:

        return [

            "Explain the main topic discussed in the document.",

            "What is the objective of this concept?",

            "Why is this topic important?",

            "Give one practical example.",

            "What are the advantages?"
        ]

    return questions[:10]