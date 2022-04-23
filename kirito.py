# █ █ ▀ █▄▀ ▄▀█ █▀█ ▀    ▄▀█ ▀█▀ ▄▀█ █▀▄▀█ ▄▀█
# █▀█ █ █ █ █▀█ █▀▄ █ ▄  █▀█  █  █▀█ █ ▀ █ █▀█
#
#              © Copyright 2022
#
#          https://t.me/hikariatama
#
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikariatama

from .. import loader, utils
import logging
import requests
import re
import asyncio
from .._types import LoadError

logger = logging.getLogger(__name__)


@loader.tds
class KiritoMod(loader.Module):
    """Publishes buttons"""

    strings = {"name": "Kirito"}

    async def client_ready(self, client, db) -> None:
        self._db = db
        self._client = client

        self._bot = "@hikka_userbot"

        if not self.get("token"):
            async with client.conversation(self._bot) as conv:
                m = await conv.send_message("/token")
                r = await conv.get_response()
                token = r.raw_text
                await m.delete()
                await r.delete()

                if not token.startswith("kirito_"):
                    raise LoadError("Token level is too low")

                self.set("token", token)

    async def add_dl_buttonscmd(self, message) -> None:
        """<channel> - Adds download buttons to all posts of channel"""
        await message.edit("🌘 <b>Adding buttons...</b>")
        async for msg in self._client.iter_messages(
            utils.get_args_raw(message),
            reverse=True,
        ):
            if not getattr(msg, "reply_markup", False) and re.search(
                r".dlmod (https?://.*?\.py)",
                getattr(msg, "raw_text", False) or "",
            ):
                answ = (
                    await utils.run_sync(
                        requests.post,
                        "https://hikka.hikariatama.ru/add_buttons",
                        headers={"Authorization": f"Bearer {self.get('token')}"},
                        data={
                            "channel": utils.get_args_raw(message),
                            "message_id": msg.id,
                        },
                    )
                ).json()

                if "wow" not in answ or not answ["wow"]:
                    logger.error(answ)

        await message.edit("🌘 <b>Buttons added!</b>")
