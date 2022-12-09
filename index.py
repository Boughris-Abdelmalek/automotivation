from PIL import ImageDraw, Image, ImageEnhance, ImageFont
import textwrap
import requests
from requests.exceptions import HTTPError
import os
from os import path
from os.path import join, dirname, abspath
from dotenv import load_dotenv
from pyunsplash import PyUnsplash
from pathlib import Path
import uuid

def get_quote(URL):
    try:
        response = requests.get(URL)
        data = response.json()
        print(f"Response status ({URL}): {response.status_code}")
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    return (data['content'], data['author'])


def get_background_image(file_name):
    #get the .env path
    dotenv_path = join(dirname(abspath("__file__")), './.env')
    load_dotenv(dotenv_path)

    #get the unsplash access key from the .env file
    UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")

    pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)

    #setting the params to generate the image
    photos = pu.photos(type_='random', count=1, featured=True, query="nature")
    [photo] = photos.entries

    #download the image
    response = requests.get(photo.link_download, allow_redirects=True)
    
    #generate a random Id to differenciate the pictures with same name
    random_id = str(uuid.uuid4())

    #save the image into a specific file
    file_name = file_name.replace(' ', '_') + random_id + '_unsplash_img.png'

    open(f'./images/{file_name}', 'wb').write(response.content)

    #get the url path for the generated image
    image_path = join(dirname(__file__), f'images\{file_name}')

    image_path = image_path.replace('\\', '/')

    return image_path


def image_processing(img_path, font_path, caption, author):
    # Getting an image
    img = Image.open(img_path)

    # Making the image darker
    enhacer = ImageEnhance.Brightness(img)

    factor = 0.5
    img = enhacer.enhance(factor)

    # give it a instagram size
    img = img.resize((1080, 1080))

    # Writing on it a random quote
    draw = ImageDraw.Draw(img)
    fontsize = 80
    fontpath = font_path
    W, H = img.size

    img_fraction = 0.50

    # Scaling the font size to the image
    font = ImageFont.truetype(fontpath, fontsize)
    while font.getsize(caption)[0] < img_fraction*img.size[0]:
        fontsize += 1
        font = ImageFont.truetype(fontpath, fontsize)
    fontsize -= 1
    font = ImageFont.truetype(fontpath, fontsize)
    #setting the font for the author to be twice smallet then the original
    author_font = ImageFont.truetype(fontpath, int(fontsize / 2))

    wrapper = textwrap.TextWrapper(width=int(W*0.02))
    word_list = wrapper.wrap(text=caption)

    caption_new = ""

    for word in word_list:
        caption_new += word + '\n\n'

    # writing on the image in the center of it
    draw.text(((W / 2, H / 2)), caption_new, fill="white", font=font, anchor="mm")
    draw.text(((W / 2, H / 1.25)), author, fill="white", font=author_font, anchor="mm")

    img.show()



font_path = "./RobotoMono-Regular.ttf"

quote_URL = 'https://api.quotable.io/random?tags=inspirational&maxLength=120'

quote, author = get_quote(quote_URL)

img_path = get_background_image(author)

image_processing(img_path, font_path, quote, author)