""" URL = "https://api.unsplash.com/photos?page=1"

HEADERS = {"Authorization": "Client-ID tKq2uU7VT5a5p6aYX0FPn-uTMjglwoOmV2TsKtYlAus"}

r = requests.get(url=URL, headers=HEADERS)

data = r.json()

image_links = list(map(lambda x: x["user"]["profile_image"]["large"], data))

pprint.pprint(image_links) """

from PIL import ImageDraw, Image, ImageEnhance, ImageFont

# The steps are :

# Getting an image
img = Image.open('C:/Users/User/Desktop/auto_motivation/nature.jpg')

""" d1 = ImageDraw.Draw(img)
d1.text((28, 36), "Hello, Malik!", fill=(255, 0, 0)) """

# Making the image darker
enhacer = ImageEnhance.Brightness(img)

factor = 0.5
img = enhacer.enhance(factor)

# give it a instagram size
img = img.resize((1080, 1080))

# Writing on it a random quote
draw = ImageDraw.Draw(img)
text = "let's try this if it works"
fontsize = 1
fontpath = "C:/Users/User/AppData/Local/Microsoft/Windows/Fonts/RobotoMono-Regular.ttf"
W, H = img.size

img_fraction = 0.50

font = ImageFont.truetype(fontpath, fontsize)
while font.getsize(text)[0] < img_fraction * img.size[0]:
    fontsize += 1
    font = ImageFont.truetype(fontpath, fontsize)
fontsize -= 1
font = ImageFont.truetype(fontpath)

draw.text(((W)/2, (H)/2), text, fill="white")

img.show()