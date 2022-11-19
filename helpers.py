from telegram import Update


def user_id_text_from_update(update: Update):
    return update.message.from_user.id, update.message.text
