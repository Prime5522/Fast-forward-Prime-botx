import re
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import (
    ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, ChannelPrivate
)
from .utils import STS
from database import db
from config import temp
from script import Script


@Client.on_message(filters.private & filters.command(["forward"]))
async def run(bot, message):
    buttons = []
    btn_data = {}
    user_id = message.from_user.id

    # Get user bot
    _bot = await db.get_bot(user_id)
    if not _bot:
        _bot = await db.get_userbot(user_id)
        if not _bot:
            return await message.reply(
                "<code>You didn't add any bot. Please add a bot using /settings !</code>"
            )

    # Get user channels
    channels = await db.get_user_channels(user_id)
    if not channels:
        return await message.reply_text("Please set a channel in /settings before forwarding")

    # If multiple channels, ask user which one
    if len(channels) > 1:
        for channel in channels:
            buttons.append([KeyboardButton(f"{channel['title']}")])
            btn_data[channel['title']] = channel['chat_id']
        buttons.append([KeyboardButton("cancel")]) 

        _toid = await bot.ask(
            message.chat.id,
            Script.TO_MSG.format(_bot['name'], _bot['username']),
            reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        )
        if _toid.text.startswith(('/', 'cancel')):
            return await message.reply_text(Script.CANCEL, reply_markup=ReplyKeyboardRemove())

        to_title = _toid.text
        toid = btn_data.get(to_title)
        if not toid:
            return await message.reply_text("Wrong channel chosen!", reply_markup=ReplyKeyboardRemove())
    else:
        toid = channels[0]['chat_id']
        to_title = channels[0]['title']

    # Ask for source message
    fromid = await bot.ask(message.chat.id, Script.FROM_MSG, reply_markup=ReplyKeyboardRemove())
    if fromid.text and fromid.text.startswith('/'):
        return await message.reply(Script.CANCEL)

    # Case 1: User sent a link instead of forward
    if fromid.text and not fromid.forward_origin:
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(fromid.text.replace("?single", ""))
        if not match:
            return await message.reply('Invalid link')

        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id = int("-100" + chat_id)

    # Case 2: User forwarded a message
    elif fromid.forward_origin and fromid.forward_origin.chat and fromid.forward_origin.chat.type in [enums.ChatType.CHANNEL, 'supergroup']:
        last_msg_id = fromid.forward_origin.message_id
        chat_id = fromid.forward_origin.chat.username or fromid.forward_origin.chat.id
        if last_msg_id is None:
            return await message.reply_text(
                "**This may be a forwarded message from a group and sent by an anonymous admin. "
                "Instead of this, please send the last message link from group.**"
            )
    else:
        return await message.reply_text("**Invalid !**")

    # Get title of source chat
    try:
        title = (await bot.get_chat(chat_id)).title
    except (PrivateChat, ChannelPrivate, ChannelInvalid):
        title = "private" if fromid.text else fromid.forward_origin.chat.title
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        return await message.reply(f'Error - {e}')

    # Ask for skip number
    skipno = await bot.ask(message.chat.id, Script.SKIP_MSG)
    if skipno.text.startswith('/'):
        return await message.reply(Script.CANCEL)

    # Double check before forwarding
    forward_id = f"{user_id}-{skipno.id}"
    buttons = [[
        InlineKeyboardButton('Yes', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('No', callback_data="close_btn")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply_text(
        text=Script.DOUBLE_CHECK.format(
            botname=_bot['name'],
            botuname=_bot['username'],
            from_chat=title,
            to_chat=to_title,
            skip=skipno.text
        ),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

    # Save state
    STS(forward_id).store(chat_id, toid, int(skipno.text), int(last_msg_id))
    
