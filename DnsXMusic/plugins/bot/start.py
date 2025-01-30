import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import _boot_
from BrandrdXMusic.plugins.sudo.sudoers import sudoers_list
from BrandrdXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BrandrdXMusic.utils.decorators.language import LanguageStart
from BrandrdXMusic.utils.formatters import get_readable_time
from BrandrdXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # Simple, stylish start text with cool small caps font (ʜɪ style)
    welcome_text = f"""
      ˹ ʜɪ ᴛʜᴇʀᴇ, {message.from_user.first_name}! 💥 ˼
    
   ⊚ ɪ'ᴍ ʏᴏᴜʀ ᴘᴇʀsᴏɴᴀʟ ᴍᴜsɪᴄ ᴀssɪsᴛᴀɴᴛ, ʀᴇᴀᴅʏ ᴛᴏ ʙʀɪɴɢ 
   ⊚  ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ᴛʀᴀᴄᴋs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ! 

    ➤ ᴘʟᴀʏ ᴍᴜsɪᴄ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ
    ➤ ᴘᴀᴜsᴇ, ʀᴇsᴜᴍᴇ, ᴀɴᴅ sᴋɪᴘ sᴏɴɢs
    ➤ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴘʟᴀʏʙᴀᴄᴋ

    ‣ ʟᴇᴛ ᴍᴇ ʜᴇʟᴘ ʏᴏᴜ ɢᴇᴛ ᴛʜᴇ ʙᴇsᴛ ᴍᴜsɪᴄ ᴠɪʙᴇ!
    ‣ ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ
    """

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_text(welcome_text, reply_markup=keyboard)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} just started the bot to check <b>sudolist</b>.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Searching...")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} just started the bot to check <b>track information</b>.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        await message.reply_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} just started the bot.\n\n<b>User ID :</b> <code>{message.from_user.id}</code>\n<b>Username :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_text(
        f"""
        ʜɪ, {message.from_user.first_name}! ɪ'ᴍ **{app.mention}** 🎶
        
        ɪ'ᴍ ᴀᴄᴛɪᴠᴇ ғᴏʀ **{get_readable_time(uptime)}**.
        ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴘʟᴀʏ ᴍᴜsɪᴄ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ!

        ᴄᴏᴍᴍᴀɴᴅs ʏᴏᴜ ᴄᴀɴ ᴜsᴇ:
        ➤ **/play [sᴏɴɢ ɴᴀᴍᴇ]**
        ➤ **/pause**
        ➤ **/skip**
        ➤ **/stop**
        
        ᴛᴏ ɢᴇᴛ ᴍᴏʀᴇ ʜᴇʟᴘ, ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ:
        """,
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_text(
                    _["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)