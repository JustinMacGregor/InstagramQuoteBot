from PIL import Image, ImageDraw, ImageFont
from instabot import Bot
import requests

# ----------------RETRIEVE DATA----------------
r = requests.get(url='https://stoic-quotes.com/api/quote')
jsonObject = r.json()
text = jsonObject["text"]
author = jsonObject["author"]

# ----------------CREATE IMAGE----------------
# variables for image size
imageX = 612
imageY = 612

# QUOTE
quote = text + " -" + author

# FONT (stored in current directory)
fnt = ImageFont.truetype('CinzelDecorative-Black.otf', 30)

# CREATE IMAGE THEN ADJUST IMAGE COLORS
img = Image.new('RGB', (imageX, imageY), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

# FIND SIZE OF LETTERS IN QUOTE
letterCount = 0
for letter in quote:
    letterCount += draw.textsize(letter, font=fnt)[0]

avgLengthOfLetter = letterCount / len(quote)

# NUMBER OF LETTERS TO PUT ON EACH LINE
noLettersEachLine = (imageX / 1.618) / avgLengthOfLetter
incrementer = 0
freshQuote = ''

# ADD LINE BREAKS WHERE NECESSARY
for letter in quote:
    if letter == '-':
        freshQuote += '\n\n' + letter
    elif incrementer < noLettersEachLine:
        freshQuote += letter
    else:
        if letter == ' ':
            freshQuote += '\n'
            incrementer = 0
        else:
            freshQuote += letter
    incrementer += 1

# MAKE THE TEXT GO IN THE CENTER OF THE BOX
dimensions = draw.textsize(freshQuote, font=fnt)
x2 = dimensions[0]
y2 = dimensions[1]

qx = (imageX / 2 - x2 / 2)
qy = (imageY / 2 - y2 / 2)

draw.text((qx, qy), freshQuote, align="center", font=fnt, fill=(250, 250, 250))

img.save('quote.jpg')

# ----------------POST IMAGE TO INSTAGRAM----------------

bot = Bot()

bot.login(username="USERNAME",
          password="PASSWORD")

bot.upload_photo("quote.jpg", caption=quote + "\n-\n#Optimism #Mind #WiseQuotes #Discipline #Meaning #Persistence "
                                              "#StrongMind #InnerPeace #Philosophy #TakeAction #Perception "
                                              "#LifeLesson #Greatness #Enlightened #Think #Stoicism #StoicThought")
