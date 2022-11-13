import json
import random
import textwrap
import shutil

import requests
from google_images_download import google_images_download
from PIL import Image, ImageDraw, ImageFont


def image_editer(image, quote_values):
    im = Image.open(str(image))
    # Open an Image
    resized_im = im.resize((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))

    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(resized_im)

    quote_font = ImageFont.truetype("./font.ttf", size=25)
    author_font = ImageFont.truetype("./font.ttf", size=22)

    # Add Text to an image
    I1.text(
        (300, 200),
        '"' + str(quote_values[0]) + '"',
        font=quote_font,
        anchor="mm",
        fill=(255, 255, 250),
    )
    I1.text(
        (380, 400), "- " + str(quote_values[1]), font=author_font, fill=(255, 255, 250)
    )
    #     # Display edited image
    resized_im.show()

    # Save the edited image
    resized_im.save(str(image))


def retrieve_images(query):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": str(query),
        "format": "jpg",
        "limit": 1,
        "print_urls": True,
        "size": "large",
        "aspect_ratio": "square",
    }
    paths = response.download(arguments)

    shutil.copy(paths[0][query][0], "outputs")
    return str(paths[0][query][0])


def get_quotes():
    returned_values = []
    response = requests.get("https://programming-quotes-api.herokuapp.com/quotes")
    data = response.json()
    quote = random.choice(data)
    wrapper = textwrap.TextWrapper(width=35)
    word_list = wrapper.wrap(text=str(quote["en"]))
    caption_new = ""
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + "\n"
    caption_new += word_list[-1]
    returned_values.append(caption_new)
    returned_values.append(quote["author"])
    return returned_values


def main():
    f = open("queries.json")
    data = json.load(f)
    input_query = random.choice(data["query"])
    image_editer(retrieve_images(str(input_query)), get_quotes())
    f.close()

if __name__ == "__main__":
    main()
