import math
from pyrogram.types import InlineKeyboardButton
from BADMUSIC.utils.formatters import time_to_seconds


# Static progress bar for Timer 1
def get_progress_bar(percentage):
    umm = math.floor(percentage)
    if 0 < umm <= 10:
        return "▰▱▱▱▱▱▱▱▱"
    elif 10 < umm <= 20:
        return "▰▰▱▱▱▱▱▱▱"
    elif 20 < umm <= 30:
        return "▰▰▰▱▱▱▱▱▱"
    elif 30 < umm <= 40:
        return "▰▰▰▰▱▱▱▱▱"
    elif 40 < umm <= 50:
        return "▰▰▰▰▰▱▱▱▱"
    elif 50 < umm <= 60:
        return "▰▰▰▰▰▰▱▱▱"
    elif 60 < umm <= 70:
        return "▰▰▰▰▰▰▰▱▱"
    elif 70 < umm <= 80:
        return "▰▰▰▰▰▰▰▰▱"
    elif 80 < umm <= 90:
        return "▰▰▰▰▰▰▰▰▰"
    elif 90 < umm <= 100:
        return "▰▰▰▰▰▰▰▰▰▰"
    else:
        return "▱▱▱▱▱▱▱▱▱"


# Dynamic progress bar for Timer 2
def get_dynamic_progress_bar(percentage):
    selections = [
        "▁▄▂▇▄▅▄▅▃",
        "▁▃▇▂▅▇▄▅▃",
        "▃▁▇▂▅▃▄▃▅",
        "▃▄▂▄▇▅▃▅▁",
        "▁▃▄▂▇▃▄▅▃",
        "▃▁▄▂▅▃▇▃▅",
        "▁▇▄▂▅▄▅▃▄",
        "▁▃▅▇▂▅▄▃▇",
        "▃▅▂▅▇▁▄▃▁",
        "▇▅▂▅▃▄▃▁▃",
        "▃▇▂▅▁▅▄▃▁",
        "▅▄▇▂▅▂▄▇▁",
        "▃▅▂▅▃▇▄▅▃",
    ]
    index = math.floor((percentage / 100) * len(selections))
    return selections[index % len(selections)]


# Stream Markup with Two Timers
def stream_markup(_, videoid, chat_id, played1, dur1, played2, dur2):
    # Timer 1
    played_sec1 = time_to_seconds(played1)
    duration_sec1 = time_to_seconds(dur1)
    percentage1 = (played_sec1 / duration_sec1) * 100
    bar1 = get_progress_bar(percentage1)

    # Timer 2
    played_sec2 = time_to_seconds(played2)
    duration_sec2 = time_to_seconds(dur2)
    percentage2 = (played_sec2 / duration_sec2) * 100
    bar2 = get_dynamic_progress_bar(percentage2)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"Timer 1: {played1} {bar1} {dur1}",
                callback_data="GetTimer1",
            )
        ],
        [
            InlineKeyboardButton(
                text=_["P_B_7"], callback_data=f"add_playlist {videoid}"
            ),
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup {videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"Timer 2: {played2} {bar2} {dur2}",
                callback_data="GetTimer2",
            )
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


# Telegram Markup with Two Timers
def telegram_markup(_, chat_id, played1, dur1, played2, dur2):
    # Timer 1
    played_sec1 = time_to_seconds(played1)
    duration_sec1 = time_to_seconds(dur1)
    percentage1 = (played_sec1 / duration_sec1) * 100
    bar1 = get_progress_bar(percentage1)

    # Timer 2
    played_sec2 = time_to_seconds(played2)
    duration_sec2 = time_to_seconds(dur2)
    percentage2 = (played_sec2 / duration_sec2) * 100
    bar2 = get_dynamic_progress_bar(percentage2)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"Timer 1: {played1} {bar1} {dur1}",
                callback_data="GetTimer1",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"Timer 2: {played2} {bar2} {dur2}",
                callback_data="GetTimer2",
            )
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["PL_B_3"],
                callback_data=f"PanelMarkup None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
     #   [  InlineKeyboardButton( text="ꜱᴘᴏᴛɪꜰʏ", web_app=WebAppInfo(url="https://open.spotify.com/"),)
     #   ],
        [
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


## Search Query Inline


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"
            )
        ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"BADPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"BADPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}"
            ),
        ],
    ]
    return buttons


## Live Stream Markup


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSEMENU_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


## Slider Query Markup


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"forceclose {query}|{user_id}"
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="• ᴘᴀᴜꜱᴇ •", callback_data=f"ADMIN Pause|{chat_id}"
            ),
            InlineKeyboardButton(
                text="• ʀᴇꜱᴜᴍᴇ •",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(text="• ꜱᴋɪᴘ •", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="• ꜱᴛᴏᴘ •", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="• ʀᴇᴘʟᴀʏ •", callback_data=f"ADMIN Replay|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"Pages Back|0|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 ʙᴀᴄᴋ",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"Pages Forw|0|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="🔇 ᴍᴜᴛᴇ", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton(
                text="🔊 ᴜɴᴍᴜᴛᴇ",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="• ꜱʜᴜꜰꜰʟᴇ •",
                callback_data=f"ADMIN Shuffle|{chat_id}",
            ),
            InlineKeyboardButton(text="• ʟᴏᴏᴘ •", callback_data=f"ADMIN Loop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"Pages Back|1|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 ʙᴀᴄᴋ",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"Pages Forw|1|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="❮ 10 ꜱᴇᴄᴏɴᴅꜱ",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❯ 10 ꜱᴇᴄᴏɴᴅꜱ",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮ 30 ꜱᴇᴄᴏɴᴅꜱ",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❯ 30 ꜱᴇᴄᴏɴᴅꜱ",
                callback_data=f"ADMIN 4|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"Pages Back|2|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔙 ʙᴀᴄᴋ",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"Pages Forw|2|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons
