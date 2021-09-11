from youtubesearchpython import VideosSearch as vs

from ..utils import Cbq


@Cbq(pattern="^/play (audio|video)?(.*)")
async def _play(e):
    r = await e.get_reply_message()
    if r and r.video or r.audio:
        await e.client.download_media(r)
    if not r:
        try:
            q = e.text.split(" ", 1)[1]
        except IndexError:
            return await e.reply("Qoery was not found.")
        q = q.replace(("audio", "video"), "")
        if q.startswith("http"):
            pass
        else:
            try:
                v = vs(q, limit=1).result()["result"][0]
            except (IndexError, KeyError, TypeError):
                return await e.reply("No song/video result found for your query!")
        print("soon")
