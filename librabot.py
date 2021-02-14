import random, requests, json, os, magic, pathlib
from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler
from matrix_client.client import MatrixClient

# Load credentials from JSON file
cred = json.load(open("credentials.json"))
client = MatrixClient(cred["server"])
token = client.login(username=cred["username"], password=cred["password"])

# Save PNG from URL, upload it to the server and send the image MCX URL to the room
def send_image_from_url(room, url):
    image = requests.get(url).content
    with open("temp.png", "wb") as png:
        png.write(image)
    mime_type = magic.from_file("temp.png", mime=True)
    mxc = client.upload(image, mime_type)
    room.send_image(mxc,"image")
    os.remove("temp.png")

# Send a random cat picture
def cat_callback(room, event):
    room.send_text("Serving a cat, please wait...")
    send_image_from_url(room, json.loads(requests.get('http://aws.random.cat/meow').content)["file"])

# Send a random dog picture
def dog_callback(room, event):
    room.send_text("Serving a dog, please wait...")
    send_image_from_url(room, json.loads(requests.get('https://random.dog/woof.json').content)["url"])

# Send a random fox picture
def fox_callback(room, event):
    room.send_text("Serving a fox, please wait...")
    send_image_from_url(room, json.loads(requests.get('https://randomfox.ca/floof/').content)["image"])

# Send a random gif
def gif_callback(room, event):
    room.send_text("Serving a gif, please wait...")
    args = event['content']['body']
    arg = args[5:]
    if(arg == ""):
        room.send_text("You need to provide an argument! Example: !gif happy")
        return
    send_image_from_url(room, json.loads(requests.get("https://g.tenor.com/v1/search?key="
    + cred["tenorAPI"] + "&limit=1&q=" + arg).content)["results"][0]["media"][0]["gif"]["url"])

def main():

    bot = MatrixBotAPI(cred["username"], cred["password"], cred["server"])

    # Set command handlers
    bot.add_handler(MCommandHandler("cat", cat_callback))
    bot.add_handler(MCommandHandler("dog", dog_callback))
    bot.add_handler(MCommandHandler("fox", fox_callback))
    bot.add_handler(MCommandHandler("gif", gif_callback))
    
    bot.start_polling()
    while True:
        input()

if __name__ == "__main__":
    main()