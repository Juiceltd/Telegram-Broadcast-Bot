from telebot.async_telebot import AsyncTeleBot
import json


bot = AsyncTeleBot('BOT_TOKEN')
admin = False

@bot.message_handler(commands=['setadmin'])
async def set_admin(message):
    global admin
    if not admin:
        admin = message.from_user.id
        await bot.send_message(message.from_user.id, f'Админ установлен {message.from_user.id}')
    else:
        await bot.send_message(message.from_user.id, 'Админ уже установлен')

@bot.message_handler(commands=['deladmin'])
async def del_admin(message):
    global admin
    if admin:
        admin = False
        await bot.send_message(message.from_user.id, 'Админ удален')
    else:
        await bot.send_message(message.from_user.id, 'Админ еще не был установлен')


@bot.channel_post_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
    'text', 'location', 'contact', 'sticker', 'video_note'])
async def channel_post(message):
    with open('data.json', 'r') as file:
        data = json.load(file)
    for chat in data['chats']:
        await bot.forward_message(chat['id'], message.chat.id, message.id)

@bot.my_chat_member_handler()
async def new_pool(message):
    global admin
    if message.chat.type == 'channel':
        await bot.send_message(admin, f'Добавили/удалили канал {message.chat.title} с id {message.chat.id}')
    if message.chat.type == 'supergroup':
        with open('data.json', 'r') as file:
            data = json.load(file)
            new_chat = {'name': f'{message.chat.title}', 'id': f'{message.chat.id}'}
            if 'chats' not in data:
                data['chats'] = []
            chat_found = False
            for chat in data['chats']:
                if chat['id'] == f'{message.chat.id}':
                    await bot.send_message(admin, f'Удалили из чата {message.chat.title} с id {message.chat.id}')
                    data['chats'].remove(chat)
                    chat_found = True
                    break
            if not chat_found:
                data['chats'].append(new_chat)
                await bot.send_message(admin, f'Добавили в чат {message.chat.title} с id {message.chat.id}')
        with open('data.json', 'w') as file:
            json.dump(data, file)



if __name__ == '__main__':
    import asyncio
    asyncio.run(bot.polling(non_stop=True))