from pyrogram.types import InlineKeyboardButton

def get_pagination(current_page, total_pages, callback_prefix):
    buttons = []
    if total_pages > 1:
        row = []
        if current_page > 1:
            row.append(InlineKeyboardButton("⬅️ ᴘʀᴇᴠ", callback_data=f"{callback_prefix}_{current_page-1}"))
        row.append(InlineKeyboardButton(f"📄 {current_page}/{total_pages}", callback_data="none"))
        if current_page < total_pages:
            row.append(InlineKeyboardButton("ɴᴇxᴛ ➡️", callback_data=f"{callback_prefix}_{current_page+1}"))
        buttons.append(row)
    return buttons
