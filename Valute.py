from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import Message

from utils.misc import modules_help, prefix


class ValuteMod:

    @Client.on_message(filters.command("val", prefix) & filters.me)
    async def valcmd(self, client: Client, message: Message):
        state = message.text[len(prefix + "val "):].strip()
        if not state:
            await message.edit("<b>Аргумент не может быть пустым.</b>")
            return
        
        chat = "@exchange_rates_vsk_bot"
        try:
            response = client.listen(chat, filters=filters.user(1210425892) & filters.text)
            bot_send_message = await client.send_message(chat, state)
            bot_response = await response

            bot_response_text = bot_response.text
            replacements = {
                "#GloryToUA": "",
                "https://200rf.com/": "",
                "https://minusrus.com/ru": "",
                "https://u24.gov.ua": "",
                "======": "",
                "Donation to support Ukraine": "",
                "РВК, иди нах*й": "",
            }
            for key, value in replacements.items():
                bot_response_text = bot_response_text.replace(key, value)

            await bot_send_message.delete()
            await message.edit(f"<b>{bot_response_text.strip()}</b>")
            await bot_response.delete()

        except RPCError as e:
            if "user is blocked" in str(e).lower():
                await message.edit(f"<b>Убери из ЧС:</b> {chat}")
            else:
                await message.edit(f"<b>Произошла ошибка:</b> {str(e)}")


# Регистрация команды и помощь по модулю
modules_help["valute"] = {
    "val [amount] [currency]": "конвертировать валюту"
}