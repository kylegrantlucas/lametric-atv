import asyncio
import pyatv
from pyatv import conf
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True
PLAYING = None
LOOP = asyncio.get_event_loop()

# Enter details used to connect
NAME = 'Living Room'
ADDRESS = 'living-room.kyrica'
HSGID = '00000000-21bf-e0d5-caf8-be759ae645b6'

# Method that is dispatched by the asyncio event loop
async def print_what_is_playing(loop):
    """Connect to device and print what is playing."""
    details = conf.AppleTV(ADDRESS, NAME)
    details.add_service(conf.DmapService(HSGID))

    print('Connecting to {}'.format(details.address))
    atv = pyatv.connect_to_apple_tv(details, loop)

    try:
        global PLAYING
        PLAYING = await atv.metadata.playing()
    finally:
        # Do not forget to logout
        await atv.logout()



@app.route('/', methods=['GET'])
def home():
    LOOP.run_until_complete(print_what_is_playing(LOOP))
    if PLAYING is not None:
      return PLAYING.title
    else:
      return "Nothing is playing"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')





