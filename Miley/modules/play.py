from . import start, stop, put, get, transcode
from ..events import Mbot
from .. import vc



@Mbot(pattern="^/play ?(.*)")
async def play_new(e):
 
