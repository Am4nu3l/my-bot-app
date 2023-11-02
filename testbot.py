import mysql.connector
import telebot
from telebot import types
mezmurList = []
menuList = []
artist_id_name = {}
artists = []
men=''
counter = 0
counter_1 = 0
host = "bjlkoynqli1nvi24lvbu-mysql.services.clever-cloud.com"
user = "uokebst08hzhbrnu"
password = "rPjR6o7BweOLqMA8X41d"
database = "bjlkoynqli1nvi24lvbu"
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=3306,

)
API_KEY = '6475088355:AAEhkaUpNVt-vFVlsa-wyUZVVHnH2EsPbxQ'
bot = telebot.TeleBot(API_KEY)

if connection.is_connected():
    cursor=connection.cursor()
    query = 'select * from singers'
    reset=cursor.execute(query)
    x=cursor.fetchall()
    connection.commit()
    for i in x:
        artists.append(i[1])
        artist_id_name[i[0]] = i[1]
else:
    print("not connected")

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
    buttons_per_row = 2
    markup = types.InlineKeyboardMarkup(row_width=2)
    filtered_list = [item for item in artists if item.startswith(call.data)]
    if(counter_1==0):
        for item in filtered_list:
            button_labels.append(item)
            buttons_split = [button_labels[i:i+buttons_per_row]
                            for i in range(0, len(button_labels), buttons_per_row)]
        if (button_labels):
            bot.send_message(call.message.chat.id, 'ዘማሪ ይምርጡ:',
                            reply_markup=menu(button_labels, buttons_per_row))
        counter_1+=1
    elif(counter_1==1):
        for key,value in artist_id_name.items():
            if(str(value)==str(call.data)):
                singerId=key
                query = f'select son_name from songs where sin_id={key}'
                cursor.execute(query)
                filtered_list=cursor.fetchall()
                connection.commit()
                for item in filtered_list:
                    button_labels.append(item[0])
                    buttons_split = [button_labels[i:i+buttons_per_row]
                                    for i in range(0, len(button_labels), buttons_per_row)]
                if (button_labels):
                    bot.send_message(call.message.chat.id, 'choose songs',
                                    reply_markup=menu(button_labels, buttons_per_row))
                break
            else:
                continue
        counter_1 += 1
    elif (counter_1 == 2):
        query = f"select *from songs where son_name='{call.data}'"
        cursor.execute(query)
        filtered_list = cursor.fetchall()
        connection.commit()
        data = [row[3] for row in filtered_list]
        # print(filtered_list)
        if (filtered_list):
            try:
                bot.send_message(call.message.chat.id, f'{data[0]}')
            except Exception as e:
                # Handle the exception
                error_message = f"An error occurred: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
                
                with open(f"{call.data}.txt", "w") as file:
                    file.write(str(data[0]))
                    bot.send_document(call.message.chat.id, file)
                    print(error_message)
                    counter_1 = 0
        else:
            bot.send_message(call.message.chat.id, 'no song found',)
        counter_1=0
        
        


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
