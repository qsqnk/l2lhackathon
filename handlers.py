import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

import user_repository
import user_queue
from bot_states import *
from helpers import user_id_text_from_update


# from start state
async def suggest_fill_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user_repository.create_user(user_id, update.message.from_user.username)
    await update.message.reply_text(
        "Welcome to Migrate2gether chat-roulette ✈️!\n\n" +
        "Here you can talk to people that had to leave their home just like you. " +
        "Specify information about you and our system will find the best match 🔥.",
        reply_markup=ReplyKeyboardMarkup([["Start filling the information"]], one_time_keyboard=True),
    )
    return START_FILL_INFO


# from start fill info state
async def suggest_choose_country_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Let's fill info about you. Which country are you migrating from?",
    )
    return WAITING_FOR_COUNTRY_FROM


# from waiting for country from state
async def save_choose_country_from(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user_repository.update_country_from(user_id, text)
    await update.message.reply_text(
        "Which country are you migrating to?",
    )
    return WAITING_FOR_COUNTRY_TO


async def save_choose_country_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user_repository.update_country_to(user_id, text)
    await update.message.reply_text(
        "What is your field of activity?",
        reply_markup=ReplyKeyboardMarkup([["IT 💻", "Business 📊", "Another..."]], one_time_keyboard=True),
    )
    return WAITING_FOR_WORK_FIELD


async def save_work_field(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user_repository.update_job(user_id, text)
    await update.message.reply_poll(
        question="Choose problems",
        options=["Documents 📄", "Housing 🏠", "Job 🚀"],
        is_anonymous=False,
        allows_multiple_answers=True,
        reply_markup=ReplyKeyboardRemove(),
    )
    return WAITING_FOR_PROBLEMS


async def save_problems(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.poll_answer.user.id

    answers = update.poll_answer.option_ids
    user_repository.update_problems(user_id, answers)

    await context.bot.send_message(
        user_id,
        f"Thank you! Information filled. Now you can find an interlocutor with similar data",
        reply_markup=ReplyKeyboardMarkup([["Find interlocutor"]], one_time_keyboard=True),
    )
    return CHATTING


async def add_to_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user_queue.add_user(user_id)

    await update.message.reply_text(
        "You have been added to queue! Please wait for your interlocutor 🕔",
    )

    return CHATTING


async def chatting_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)

    user = user_repository.get_user(user_id)
    if not user.interlocutor:
        await update.message.reply_text(
            "The interlocutor has not been found yet. Please wait 🕔",
        )
        return CHATTING

    await context.bot.send_message(
        user.interlocutor,
        text,
    )

    return CHATTING


async def stop_chatting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user = user_repository.get_user(user_id)
    interlocutor = user.interlocutor
    for id in (user_id, interlocutor):
        user_repository.update_interlocutor(id, None)
        await context.bot.send_message(
            id,
            "Chat terminated" if id == user_id else "Your interlocutor terminated chat",
            reply_markup=ReplyKeyboardMarkup([["Find interlocutor"]],
                                             one_time_keyboard=True),
        )

    return CHATTING


async def next_interlocutor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user = user_repository.get_user(user_id)
    interlocutor = user.interlocutor
    user_repository.update_interlocutor(user_id, None)
    user_repository.update_interlocutor(interlocutor, None)
    await context.bot.send_message(
        interlocutor,
        "Your interlocutor terminated chat",
        reply_markup=ReplyKeyboardMarkup([["Find interlocutor"]], one_time_keyboard=True),
    )
    await update.message.reply_text(
        "Looking for next interlocutor... 🕔",
    )
    user_queue.add_user(user_id)
    return CHATTING


async def exchange_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user = user_repository.get_user(user_id)
    interlocutor = user.interlocutor

    await update.message.reply_text(
        "Contact exchanging request has been sent",
    )

    await context.bot.send_message(
        interlocutor,
        "Your interlocutor want to exchange contacts",
        reply_markup=ReplyKeyboardMarkup([["Agree exchange", "Disagre exchange"]], one_time_keyboard=True),
    )

    return CHATTING


async def agree_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user = user_repository.get_user(user_id)
    interlocutor = user.interlocutor

    for id in (user_id, interlocutor):
        await context.bot.send_message(
            id,
            f"First interlocutor: @{user_repository.get_user(user_id).username}\n" +
            f"Second interlocutor: @{user_repository.get_user(interlocutor).username}\n",
            reply_markup=ReplyKeyboardMarkup([["Stop chatting", "Next interlocutor", "Exchange contacts"]],
                                             one_time_keyboard=True),
        )

    return CHATTING


async def disagree_exchange(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, text = user_id_text_from_update(update)
    user = user_repository.get_user(user_id)
    interlocutor = user.interlocutor

    await context.bot.send_message(
        interlocutor,
        "Your interlocutor disagreed contact exchange",
        reply_markup=ReplyKeyboardMarkup([["Stop chatting", "Next interlocutor", "Exchange contacts"]],
                                         one_time_keyboard=True),
    )
    return CHATTING
