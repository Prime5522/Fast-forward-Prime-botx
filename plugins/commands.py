# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import sys
import asyncio 
from database import Db, db
from config import Config, temp, AUTH_CHANNEL
from script import Script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
from pyrogram.errors import *
import psutil
import time as time
from os import environ, execle, system

START_TIME = time.time()

async def is_subscribed(bot, query, channel):
    btn = []
    for id in channel:
        chat = await bot.get_chat(int(id))
        try:
            await bot.get_chat_member(id, query.from_user.id)
        except UserNotParticipant:
            btn.append([InlineKeyboardButton(f"✇ ᴊᴏɪɴ {chat.title} ✇", url=chat.invite_link)]) #✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇
        except Exception as e:
            pass
    return btn

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

main_buttons = [[
    InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs ⚙', callback_data='settings#main')
],[
    InlineKeyboardButton('💬 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/Prime_botz_Support'),
    InlineKeyboardButton('🎬 ᴍᴏᴠɪᴇꜱ ᴄʜᴀɴɴᴇʟ', url='https://t.me/Prime_Movies4U')
],[
    InlineKeyboardButton('✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇', url='https://t.me/Prime_botz')
],[
    InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
    InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')
],[
    InlineKeyboardButton('☆ 💫 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 💫 ☆', url='https://t.me/MR_PRIME_SUPREME')
]]

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    if AUTH_CHANNEL:
        try:
            btn = await is_subscribed(client, message, AUTH_CHANNEL)
            if btn:
                username = (await client.get_me()).username
                if len(message.command) > 1:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start={message.command[1]}")])
                else:
                    btn.append([InlineKeyboardButton("♻️ Try Again ♻️", url=f"https://t.me/{username}?start=true")])

                await message.reply_photo(
                    photo="https://envs.sh/KgA.jpg",  # Replace with your image link
                    caption=(
                        "<b>👋 ʜᴇʟʟᴏ ᴅᴇᴀʀ ⚡,\n\n"
                        "ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ʏᴏᴜ ᴍᴜꜱᴛ ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ.\n\n"
                        "ᴄʟɪᴄᴋ ᴏɴ \"✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇\" ʙᴜᴛᴛᴏɴ.ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ \"ʀᴇǫᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ\" ʙᴜᴛᴛᴏɴ.\n"
                        "ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴏɴ \"ᴛʀʏ ᴀɢᴀɪɴ\" ʙᴜᴛᴛᴏɴ.</b>"
                    ),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
        except Exception as e:
            print(e)

    # এখানে পরিবর্তন করা হয়েছে: কোডটিকে অ্যাসিঙ্ক্রোনাস ফাংশনের মধ্যে রাখা হয়েছে
    user = message.from_user
    if not await db.is_user_exist(user.id):  # অ্যাসিঙ্ক্রোনাস অপারেশন
        await db.add_user(user.id, user.first_name)  # অ্যাসিঙ্ক্রোনাস অপারেশন

    reply_markup = InlineKeyboardMarkup(main_buttons)

    # ফটো পাঠানো
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://envs.sh/KgL.jpg",  # এখানে ছবির path বা URL দিন
        caption=Script.START_TXT.format(message.from_user.first_name),  # ক্যাপশন
        reply_markup=reply_markup  # বাটন যুক্ত করা
    )
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text(text="<i>Trying to restarting.....</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [[
        InlineKeyboardButton('🤔 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')
    ],[
        InlineKeyboardButton('Aʙᴏᴜᴛ ✨️', callback_data='about'),
        InlineKeyboardButton('⚙ Sᴇᴛᴛɪɴɢs', callback_data='settings#main')
    ],[
        InlineKeyboardButton('• back', callback_data='back')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(text=Script.HELP_TXT, reply_markup=reply_markup)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Script.START_TXT.format(query.from_user.first_name))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [[
         InlineKeyboardButton('• back', callback_data='help'),
         InlineKeyboardButton('Stats ✨️', callback_data='status')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    upt = await get_bot_uptime(START_TIME)
    buttons = [[
        InlineKeyboardButton('• back', callback_data='help'),
        InlineKeyboardButton('System Stats ✨️', callback_data='systm_sts'),
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024**3)  # Convert to GB
    used_space = disk_usage.used / (1024**3)    # Convert to GB
    free_space = disk_usage.free / (1024**3)
    text = f"""
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ</b>: <code>{total_space:.2f} GB</code>
║┣⪼ <b>ᴜsᴇᴅ</b>: <code>{used_space:.2f} GB</code>
║┣⪼ <b>ꜰʀᴇᴇ</b>: <code>{free_space:.2f} GB</code>
║┣⪼ <b>ᴄᴘᴜ</b>: <code>{cpu}%</code>
║┣⪼ <b>ʀᴀᴍ</b>: <code>{ram}%</code>
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

async def get_bot_uptime(start_time):
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_hours != 0:
        uptime_string += f" {uptime_hours % 24}H"
    if uptime_minutes != 0:
        uptime_string += f" {uptime_minutes % 60}M"
    uptime_string += f" {uptime_seconds % 60} Sec"
    return uptime_string   
    

