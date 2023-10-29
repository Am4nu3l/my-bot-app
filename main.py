from bs4 import BeautifulSoup
import requests as re
import sys
import os
import telebot
import re as regx
from telebot import types
import http.server
import socketserver
mezmurList = []
menuList = []
artistList = []
artists = []
men = ''
counter = 0
counter_1 = 0
query = 'https://wikimezmur.org/am'
API_KEY = '6475088355:AAEhkaUpNVt-vFVlsa-wyUZVVHnH2EsPbxQ'
port = 8004

# This creates a simple web server that serves files in the current directory
handler = http.server.SimpleHTTPRequestHandler

# Use the socketserver module to create the server
httpd = socketserver.TCPServer(("", port), handler)

print(f"Serving on port {port}")

request = re.get(
    "https://wikimezmur.org/am/Gospel_Singers").text
datas = BeautifulSoup(request, 'lxml')
data = datas.find_all('li')
for arts in data:
    if (counter <= 139):
        artistList.append(arts.text)
    else:
        counter == 0
        break
    counter += 1
for x in artistList:
    match = regx.search(r'\((.*?)\)', x)
    if (match):
        artists.append(match.group(1))
    else:
        print('not found')

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def handle_start(message):
    button_labels = []
    buttons_per_row = 4
    print(message.from_user.id)
    for char_code in range(ord('A'), ord('Z') + 1):
        capital_letter = chr(char_code)
        button_labels.append(capital_letter)
    buttons_split = [button_labels[i:i+buttons_per_row]
                     for i in range(0, len(button_labels), buttons_per_row)]
    print("bot started")
    bot.send_message(message.chat.id,
                     f'ሰላም !\t{message.chat.first_name}\nይህ ቦት የሚፈልጉትን የመዝሙር ግጥም እንዲያገኙ ይረዶታል::\n#---አጠቃቀም---# \n1. ከታች ያለውን የስም ምርጫ መዘርዘሪያ ይንኩ\n\teg. ለተከስተ ጌትነት (T) ይጫኑ\n2. የቦቱን መልስ በመከተል የሚፈልጉትን የመዝሙር ገጥም ያግኙ',
                     reply_markup=menu(button_labels, buttons_per_row))


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global query
    global counter_1
    global men
    button_labels = []
    artistVol = []
    artistSong = []
    filtered_list = [item for item in artists if item.startswith(call.data)]
    buttons_per_row = 2
    markup = types.InlineKeyboardMarkup(row_width=2)
    if (call.data == 'start_command'):
        buttons_per_row = 4
        print(call.message.from_user.id)
        for char_code in range(ord('A'), ord('Z') + 1):
            capital_letter = chr(char_code)
            button_labels.append(capital_letter)
        buttons_split = [button_labels[i:i+buttons_per_row]
                         for i in range(0, len(button_labels), buttons_per_row)]
        bot.send_message(call.message.chat.id,
                         f'ሰላም !\t{call.message.chat.first_name}\nይህ ቦት የሚፈልጉትን የመዝሙር ግጥም እንዲያገኙ ይረዶታል::\n#---አጠቃቀም---# \n1. ከታች ያለውን የስም ምርጫ መዘርዘሪያ ይንኩ\n\teg. ለተከስተ ጌትነት (T) ይጫኑ\n2. የቦቱን መልስ በመከተል የሚፈልጉትን የመዝሙር ገጥም ያግኙ',
                         reply_markup=menu(button_labels, buttons_per_row))
    elif (counter_1 == 0):
        for item in filtered_list:
            button_labels.append(item)
        buttons_split = [button_labels[i:i+buttons_per_row]
                         for i in range(0, len(button_labels), buttons_per_row)]
        if (button_labels):
            counter_1 += 1
            bot.send_message(call.message.chat.id, 'ዘማሪ ይምርጡ:',
                             reply_markup=menu(button_labels, buttons_per_row))
        else:
            query = 'https://wikimezmur.org/am'
            bot.send_message(call.message.chat.id, 'no data has been found')
            inline_keyboard = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(
                "Main Menu", callback_data='start_command')
            inline_keyboard.add(start_button)

    # Send the inline keyboard with the "/start" button
            bot.send_message(
                call.message.chat.id, "Click the button to start the command.", reply_markup=inline_keyboard)

    elif (counter_1 == 1):
        query = query+"/"+str(call.data).replace(" ", "_")
        request = re.get(query).text
        print(query+"/"+str(call.data).replace(" ", "_"))
        datas = BeautifulSoup(request, 'lxml')
        data = datas.find_all('li', class_='toclevel-1')
        data2 = datas.find_all('li', class_='toclevel-2')
        data.extend(data2)
        for api in data:
            button_labels.append(api.text)
        for title in button_labels:
            match = regx.search(r'\((.*?)\)', title)
            if (match):
                artistVol.append(match.group(1))
            else:
                print('not found')
        if (artistVol):
            counter_1 += 1
            bot.send_message(call.message.chat.id, 'አልበም ይምረጡ:',
                             reply_markup=menu(artistVol, 2))
        else:
            query = 'https://wikimezmur.org/am'
            bot.send_message(call.message.chat.id, 'no data has been found')
            inline_keyboard = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(
                "Main Menu", callback_data='start_command')
            inline_keyboard.add(start_button)

    # Send the inline keyboard with the "/start" button
            bot.send_message(
                call.message.chat.id, "Click the button to start the command.", reply_markup=inline_keyboard)

    elif (counter_1 == 2):
        query = query+"/"+str(call.data).replace(" ", "_")
        request = re.get(query).text
        print(query)
        datas = BeautifulSoup(request, 'lxml')
        data = datas.find_all('dd')
        for api in data:
            button_labels.append(api.text)
        for title in button_labels:
            match = regx.search(r'\((.*?)\)', title)
            if (match):
                artistSong.append(match.group(1))
            else:
                print('not found')
        if (artistSong):
            counter_1 += 1
            bot.send_message(call.message.chat.id, 'መዝሙር ይምረጡ',
                             reply_markup=menu(artistSong, 2))
        else:
            query = 'https://wikimezmur.org/am'
            bot.send_message(call.message.chat.id, 'no data has been found')
            inline_keyboard = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(
                "Main Menu", callback_data='start_command')
            inline_keyboard.add(start_button)

    # Send the inline keyboard with the "/start" button
            bot.send_message(
                call.message.chat.id, "Click the button to start the command.", reply_markup=inline_keyboard)

    elif (counter_1 == 3):
        query = query+"/"+str(call.data).replace(" ", "_")
        request = re.get(query).text
        print(query)
        datas = BeautifulSoup(request, 'lxml')
        data = datas.find_all('div', class_='poem')
        data2 = datas.find_all('div', class_='mw-parser-output')
        data.extend(data2)
        if (data):
            counter_1 = 0
            query = 'https://wikimezmur.org/am'
            text_content = ""  # Initialize an empty string outside the loop
            for poem in data:
                poem_text = poem.get_text(separator='\n', strip=True)
            bot.send_message(call.message.chat.id, f"{poem_text}"
                             .replace("<p>", "")
                             .replace('<div class="poem">', "")
                             .replace("<br/>", "")
                             .replace("</span>", "")
                             .replace('<span class="mw-poem-indented" style="display: inline-block; margin-left: 4em;">', "")
                             .replace('<span class="mw-poem-indented" style="display: inline-block; margin-left: 2em;">', "")
                             .replace('<span class="mw-poem-indented" style="display: inline-block; margin-left: 1em;">', "")
                             .replace("</p>", "").replace("</div>", "")
                             .replace("</u>", "").replace("</div>", "")
                             .replace("<u>", "").replace("</div>", ""))
            inline_keyboard = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(
                "Main Menu", callback_data='start_command')
            inline_keyboard.add(start_button)

    # Send the inline keyboard with the "/start" button
            bot.send_message(
                call.message.chat.id, "Click the button to start the command.", reply_markup=inline_keyboard)

        else:
            counter_1 = 0
            query = 'https://wikimezmur.org/am'
            bot.send_message(call.message.chat.id, "no data has been found")


def menu(button_labels, columnSize):
    buttons_per_row = columnSize
    buttons_split = [button_labels[i:i+buttons_per_row]
                     for i in range(0, len(button_labels), buttons_per_row)]
    keyboard = telebot.types.InlineKeyboardMarkup()

    for row in buttons_split:
        row_buttons = [telebot.types.InlineKeyboardButton(
            button, callback_data=button) for button in row]
        keyboard.row(*row_buttons)
    return keyboard


bot.polling()
httpd.serve_forever()
