from __init__ import player_posts
import base64
test = player_posts["79e940993f554e41a6689ac27b424c42"]
for post in test.find():
    hello = post['image']

with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decodebytes(hello))
