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

    # Changli Genshin-Themed Advanced Start Text
    welcome_text = f"""
    ✨ ʜᴇʏ ᴛʜᴇʀᴇ, {message.from_user.first_name}! ✨  
    ˹ ɪ'ᴍ ᴄʜᴀɴɢʟɪ — ʏᴏᴜʀ ᴇʟᴇᴍᴇɴᴛᴀʟ ᴍᴜsɪᴄ ᴍᴜsᴇ 🎶 ˼  

    🔥 ᴄʜᴀɴɴᴇʟɪɴɢ ᴍʏsᴛɪᴄᴀʟ ᴘᴏᴡᴇʀs, ɪ ᴄᴀɴ ғɪʟʟ ʏᴏᴜʀ ᴡᴏʀʟᴅ ᴡɪᴛʜ  
    ᴇᴛʜᴇʀᴇᴀʟ ᴍᴜsɪᴄ, ᴠɪʙʀᴀɴᴛ ᴍᴇʟᴏᴅɪᴇs, ᴀɴᴅ ᴜɴᴘᴀʀᴀʟʟᴇʟᴇᴅ ʜᴀʀᴍᴏɴɪᴇs! 🎧  

    🌌 **ᴅɪᴠᴇ ɪɴᴛᴏ ᴀ ᴅɪᴍᴇɴsɪᴏɴ ᴡʜᴇʀᴇ ᴍᴜsɪᴄ ᴍᴇᴇᴛs ᴍᴀɢɪᴄ!**  
    💫 **ᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ᴊᴏᴜʀɴᴇʏ!**  
    """

    buttons = [
        [InlineKeyboardButton("🎵 ʙᴇɢɪɴ ᴛʜᴇ ᴍᴜsɪᴄᴀʟ ᴊᴏᴜʀɴᴇʏ", callback_data="play_music")],
        [InlineKeyboardButton("💫 ᴄᴏɴɴᴇᴄᴛ ᴡɪᴛʜ ᴄʜᴀɴɢʟɪ", url=config.SUPPORT_CHAT)],
    ]

    keyboard_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(welcome_text, reply_markup=keyboard_markup)


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

        🌌 ᴛᴀᴘ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ:
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