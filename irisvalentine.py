from .. import loader		
from asyncio import sleep
#Модуль не мой, спизженный
class IrisBotMod(loader.Module):
	"""Я рекомендую создать вам чат ,где вы будете использовать данный модуль, чтобы вас не беспокоили лишнии уведомления и тд. Так же можно это делать в лс Iris-а."""
	strings = {"name": "IrisValentine"}
	
	def __init__(self):
		self.farm = True
		
	async def farmcmd(self, message):
		"""Включает команду "скрафтить валентинки". Чтобы остановить, используйте "стоп валентинки"."""
		while self.farm:
			await message.reply("скрафтить валентинки\n\n<b>Следующая команда будет произведена через 4 часа.\n\n</b>")
			await sleep(14500)
				
	async def linkcmd(self, message):
		"""Если у вас не работают команды,используйте данную команду, чтобы заново установить модуль."""
		await message.edit("<code>.dlmod https://raw.githubusercontent.com/Meyronn/Modules-FTG/irisvalentine.py</code>\n\n<b>")
