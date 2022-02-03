from .. import loader, utils
import os

class BCMod(loader.Module):
	strings = {"name": "Create_bot"}

	async def helpbotcmd(self, message):
		await message.edit(f'''

Этот модуль позволит вам создать своего простого бота для телеграм
[1] Создайте бота в @BotFather и скопируйте API
[2] Пропишите .tb ваш API (.tb 1111111111:qwewqwewqe-o-ababababababababababab)
[3] Пропишите .stxt что отправит бот при команде /start (.stxt Привет)
[4] Вы можете добавить чтобы бот отправил текст/текст с кнопками(до 4)/сигнальные слова/словосочетания
[4.1] Чтобы бот отправил обычное сообщение, пропишите .at текст (.at как дела?)
[4.2] Чтобы отправить текст с кнопками(до 4), вам следует: (ТЕКСТЫ НА КНОПКАХ ДОЛЖНЫ БЫТЬ РАЗНЫМИ)
[4.2.a] .atb1 текст к которому прикрепиться кнопка/и * слово на кнопке * что бот отправит по нажатию этой кнопки
[4.2.b] .atb2 текст к которому прикрепиться кнопка/и * слово на 1 кнопке * что бот отправит по нажатию 1 кнопки * слово на 2 кнопке * что бот отправит по нажатию 2 кнопки
[4.2.c] .atb3 текст к которому прикрепиться кнопка/и * слово на 1 кнопке * что бот отправит по нажатию 1 кнопки * слово на 2 кнопке * что бот отправит по нажатию 2 кнопки * слово на 3 кнопке * что бот отправит по нажатию 3 кнопки
[4.2.в] .atb3 текст к которому прикрепиться кнопка/и * слово на 1 кнопке * что бот отправит по нажатию 1 кнопки * слово на 2 кнопке * что бот отправит по нажатию 2 кнопки * слово на 3 кнопке * что бот отправит по нажатию 3 кнопки * слово на 4 кнопке * что бот отправит по нажатию 4 кнопки
[4.3] Чтобы добавить сигнальное слово/словосочетание пропишите : .sw если бот получит слово/словосочетание * что бот ответит на этот текст
[5] Чтобы закончить бота пропишите .endbot
[6] Чтоы посмотреть бота пропишите .mybot
[7] Если хотите создать нового бота, то вам следует удалить старого бота при помощи команды .delbot
''')

	async def mybotcmd(self, message):
		try:
			await message.client.send_file('me', "bot.py")
			await message.delete()
		except:
			await message.edit('<b>У вас нет бота!!!</b>')

	async def delbotcmd(self, message):
		try:
			os.remove('bot.py')
			await message.edit('<b>Бот удалён</b>')
		except:
			await message.edit('<b>У вас нет бота!!!</b>')



	async def tbcmd(self, message):
		token_bot = utils.get_args_raw(message)

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''import telebot

from telebot import types

bot = telebot.TeleBot('{token_bot}')

''')
		f.close()

		await message.edit(f'<b>Токен бота : </b><code>{token_bot}</code>')

	async def stxtcmd(self, message):
		start_txt = utils.get_args_raw(message)

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''@bot.message_handler(commands=['start'])
def welcome(message):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('Начать')
	markup.add(item1)

	bot.send_message(message.chat.id,"""{start_txt}\nБот создан при поддержке интернета""", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):

	if message.chat.type == 'private':
		if message.text == 'Начать':''')

		f.close()

		await message.edit(f'<b>Текст при  /start : </b><code>{start_txt}</code>')


	async def atcmd(self, message):
		txt = utils.get_args_raw(message)

		file = open('bot.py','r')  
		lines = file.read()       
		if lines[-1] == ':':

			f = open('bot.py','a', encoding="utf-8")
			f.write(f'''
			bot.send_message(message.chat.id,'{txt}')''')
			f.close()			

			await message.edit(f'<b>Добавлен текст : </b><code>{txt}</code>')

		else:

			f = open('bot.py','a', encoding="utf-8")
			f.write(f'''
			bot.send_message(message.chat.id,'{txt}')''')
			f.close()

			await message.edit(f'<b>Добавлен текст : </b><code>{txt}</code>')


	async def atb1cmd(self, message):
		args = utils.get_args_raw(message).split(' * ')
		txt = args[0]
		txt_1 = args[1]
		com_but = args[2]

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			item1 = types.KeyboardButton('{txt_1}')''')
		f.close()
				
		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup.add(item1)
			bot.send_message(message.chat.id,'{txt}', reply_markup=markup)
		elif message.text == '{txt_1}':
			bot.send_message(message.chat.id,'{com_but}')''')
		f.close()

		await message.edit(f'<b>Кнопка прикреплена к тексту: {txt}\nТекст кнопки: {txt_1}\nПри нажатии на кнопку {txt_1}, отправиться: {com_but}<b>')

	async def atb2cmd(self, message):
		args = utils.get_args_raw(message).split(' * ')

		txt = args[0]

		txt_1 = args[1]
		com_but = args[2]

		txt_2 = args[3]
		com_but_2 = args[4]

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			item1 = types.KeyboardButton('{txt_1}')
			item2 = types.KeyboardButton('{txt_2}')''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup.add(item1, item2)
			bot.send_message(message.chat.id,'{txt}', reply_markup=markup)''')
		f.close()

		f = open('bot.py','a', encoding="utf-8") #by @sblro4eeek
		f.write(f'''
		elif message.text == '{txt_1}':
			bot.send_message(message.chat.id,'{com_but}')
		elif message.text == '{txt_2}':
			bot.send_message(message.chat.id,'{com_but_2}')''')
		f.close()

		await message.edit(f'<b>Кнопка прикреплена к тексту: {txt}\nТекст кнопки 1: {txt_1}\nТекст кнопки 2: {txt_2}\nПри нажатии на кнопку {txt_1}, отправиться: {com_but}\nПри нажатии на кнопку {txt_2}, отправиться: {com_but_2}<b>')


	async def atb3cmd(self, message):
		args = utils.get_args_raw(message).split(' * ')

		txt = args[0]

		txt_1 = args[1]
		com_but = args[2]

		txt_2 = args[3]
		com_but_2 = args[4]

		txt_3 = args[5]
		com_but_3 = args[6]

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			item1 = types.KeyboardButton('{txt_1}')
			item2 = types.KeyboardButton('{txt_2}')
			item3 = types.KeyboardButton('{txt_3}')''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup.add(item1, item2, item3)
			bot.send_message(message.chat.id,'{txt}', reply_markup=markup)''')
		f.close()


		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
		elif message.text == '{txt_1}':
			bot.send_message(message.chat.id,'{com_but}')
		elif message.text == '{txt_2}':
			bot.send_message(message.chat.id,'{com_but_2}')
		elif message.text == '{txt_3}':
			bot.send_message(message.chat.id,'{com_but_3}')''')
		f.close()

		await message.edit(f'<b>Кнопка прикреплена к тексту: {txt}\nТекст кнопки 1: {txt_1}\nТекст кнопки 2: {txt_2}\nТекст кнопки 3: {txt_3}\nПри нажатии на кнопку {txt_1}, отправиться: {com_but}\nПри нажатии на кнопку {txt_2}, отправиться: {com_but_2}\nПри нажатии на кнопку {txt_3}, отправиться: {com_but_3}<b>')



	async def atb4cmd(self, message):
		args = utils.get_args_raw(message).split(' * ')

		txt = args[0]

		txt_1 = args[1]
		com_but = args[2]

		txt_2 = args[3]
		com_but_2 = args[4]

		txt_3 = args[5]
		com_but_3 = args[6]

		txt_4 = args[7]
		com_but_4 = args[8]

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			item1 = types.KeyboardButton('{txt_1}')
			item2 = types.KeyboardButton('{txt_2}')
			item3 = types.KeyboardButton('{txt_3}')
			item4 = types.KeyboardButton('{txt_4}')''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
			markup.add(item1, item2, item3, item4)
			bot.send_message(message.chat.id,'{txt}', reply_markup=markup)''')
		f.close()

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
		elif message.text == '{txt_1}':
			bot.send_message(message.chat.id,'{com_but}')
		elif message.text == '{txt_2}':
			bot.send_message(message.chat.id,'{com_but_2}')
		elif message.text == '{txt_3}':
			bot.send_message(message.chat.id,'{com_but_3}')
		elif message.text == '{txt_4}':
			bot.send_message(message.chat.id,'{com_but_4}')''')
		f.close()

		await message.edit(f'<b>Кнопка прикреплена к тексту: {txt}\nТекст кнопки 1: {txt_1}\nТекст кнопки 2: {txt_2}\nТекст кнопки 3: {txt_3}\nТекст кнопки 4: {txt_4}\nПри нажатии на кнопку {txt_1}, отправиться: {com_but}\nПри нажатии на кнопку {txt_2}, отправиться: {com_but_2}\nПри нажатии на кнопку {txt_3}, отправиться: {com_but_3}\nПри нажатии на кнопку {txt_4}, отправиться: {com_but_4}<b>')


	async def swcmd(self, message):
		args = utils.get_args_raw(message).split(' * ')
		sig = args[0]
		ans = args[1]

		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
		elif message.text == '{sig}':
			bot.send_message(message.chat.id,'{ans}')''')
		f.close()

		await message.edit(f'<b>При отправке слова/словосочетания: {sig}, бот ответит: {ans}</b>')

	async def endbotcmd(self, message):
		f = open('bot.py','a', encoding="utf-8")
		f.write(f'''
bot.polling(none_stop=True)''')
		f.close()

		await message.edit(f'<b>Бот завершен! Чтобы проверить бота пропишите </b><code>.mybot</code>')
