from Evie import ubot


class XPlayer(GroupCall):
    def __init__(self, chat_id: int):
        self.replay_songs = False
        self.is_active = False
        self.current_vol = 100
        self.playlist = []
        self.chat_id = chat_id
        self.chat_has_bot = False
        super().__init__(
            client=ubot, play_on_repeat=self.replay_songs, path_to_log_file=""
        )

    def start_playout(self, key: str):
        self.input_filename = keypath(key)

    def replay(self) -> bool:
        self.play_on_repeat = self.replay_songs = not self.replay_songs
        return self.replay_songs

    def get_playlist(self) -> str:
        out = "🗒  **PLAYLIST**\n\n"
        if len(self.playlist) == 0:
            out += "`[ Empty ]`"
        else:
            current = self.playlist[0]
            out += f"▶️  **Now Playing :  🎵 [{escape_markdown(current['title'])}]({(BASE_YT_URL + current['id']) if current['yt_url'] else current['msg'].link})**\n"
            if len(self.playlist) > 1:
                out += "\n".join(
                    [
                        f"• **{x}.** [{escape_markdown(y['title'])}]({(BASE_YT_URL + y['id']) if y['yt_url'] else y['msg'].link})"
                        for x, y in enumerate(self.playlist[1:], start=1)
                    ]
                )
        return out

    async def join(self):
        # Joining the same group call can crash the bot
        # if not self.is_connected: (https://t.me/tgcallschat/7563)
        if not self.is_active:
            await super().start(self.chat_id)
            self.is_active = True

    async def leave(self):
        self.input_filename = ""
        # https://nekobin.com/nonaconeba.py
        try:
            await super().stop()
            self.is_active = False
        except AttributeError:
            pass
