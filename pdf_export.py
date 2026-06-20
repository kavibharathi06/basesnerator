from PIL import Image
import numpy as np
import os


def create_pdf(images, output_path):

    pdf_images = []

    for img in images:

        if len(img.shape) == 2:

            pil = Image.fromarray(img)

            pil = pil.convert("RGB")

        else:

            pil = Image.fromarray(img)

        pdf_images.append(pil)

    if len(pdf_images) == 0:

        return None

    pdf_images[0].save(
        output_path,
        save_all=True,
        append_images=pdf_images[1:]
    )

    return output_path