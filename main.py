import logging
import webbrowser
import json
import os

#from telegram.ext.messagehandler import MessageHandler
from telegram import Update
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from sqlalchemy import create_engine
from models import Base, Lector, Subject
from sqlalchemy.orm import Session
from sqlalchemy import select

engine = create_engine("sqlite+pysqlite:///C:\\Users\\nabac\\OneDrive\\Desktop\\bot-Telegram\\database.db", echo=True)

EXPECT_LECTOR_NAME, EXPECT_LECTOR_SURNAME, EXPECT_LECTOR_SECONDNAME,EXPECT_LECTOR_ZOOMCODE,EXPECT_LECTOR_ZOOMPASS,EXPECT_LECTOR_TEAMS = range(6)
EXPECT_SUBJECT_NAME, EXPECT_SUBJECT_DAY, EXPECT_SUBJECT_LESSON, EXPECT_SUBJECT_WEEKTYPE, EXPECT_SUBJECT_GROUP, EXPECT_SUBjECT_LECTOR_NAME = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"**Привет, {update.effective_user.first_name}, я бот помощник Инженерного учебно-научного института**",parse_mode='Markdown')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await context.bot.send_message("**Все мои возможности: **",parse_mode='Markdown')

async def add_lector(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,text = 'Creating Lector')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector name', reply_markup=ForceReply())
    return EXPECT_LECTOR_NAME
    
async def lector_name_input_by_user(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data["lector_name"] = name
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector surname', reply_markup=ForceReply())
    return EXPECT_LECTOR_SURNAME

async def lector_surname_input_by_user(update: Update, context: CallbackContext): 
    surname = update.message.text
    context.user_data["lector_surname"] = surname
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector secondname', reply_markup=ForceReply())
    return EXPECT_LECTOR_SECONDNAME

async def lector_secondname_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    context.user_data["lector_secondname"] = value
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector zoom code', reply_markup=ForceReply())
    return EXPECT_LECTOR_ZOOMCODE

async def lector_zoomcode_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    context.user_data["lector_zoomcode"] = value
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector zoom password', reply_markup=ForceReply())
    return EXPECT_LECTOR_ZOOMPASS

async def lector_zoompass_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    context.user_data["lector_zoompass"] = value
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector teams (y/n)', reply_markup=ForceReply())
    return EXPECT_LECTOR_TEAMS

async def lector_teams_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    if value != 'y' and value != 'n': 
        value = 'n'
    context.user_data["lector_teams"] = value

    name = context.user_data.get('lector_name', 'F')
    surname = context.user_data.get('lector_surname', 'F')
    secondname = context.user_data.get('lector_secondname', 'F')
    zoomcode = context.user_data.get('lector_zoomcode', 'F')
    zoompass = context.user_data.get('lector_zoompass', 'F')
    teams = context.user_data.get('lector_teams', 'F')
    tmp = Lector(
        name = name,
        surname = surname,
        secondname = secondname,
        zoomcode = zoomcode,
        zoompass = zoompass, 
        isteams = teams == 'y' if True else False
    )
    print(tmp.__repr__())
    with Session(engine) as session:
        session.add_all([tmp])
        session.commit()
    return ConversationHandler.END

async def add_subject(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,text = 'Creating Subject')
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject name', reply_markup=ForceReply())
    return EXPECT_SUBJECT_NAME

async def subject_name_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    context.user_data["subject_name"] = value
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject day', reply_markup=ForceReply())
    return EXPECT_SUBJECT_DAY

async def subject_day_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    context.user_data["subject_day"] = value
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject lesson (number)', reply_markup=ForceReply())
    return EXPECT_SUBJECT_LESSON

async def subject_lesson_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    intval = 0
    try:
        intval = int(value)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Only Number, Error')
        return ConversationHandler.END
    
    context.user_data["subject_lesson"] = intval
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject week type (1 - for numerator / 2 - for denominator / 3 - both)', reply_markup=ForceReply())
    return EXPECT_SUBJECT_WEEKTYPE

async def subject_weektype_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    intval = 0
    try:
        intval = int(value)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Only Number, Error')
        return ConversationHandler.END
    
    context.user_data["subject_weektype"] = intval
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject group (3 - for all)', reply_markup=ForceReply())
    return EXPECT_SUBJECT_GROUP

async def subject_group_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    intval = 0
    try:
        intval = int(value)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Only Number, Error')
        return ConversationHandler.END
    
    context.user_data["subject_lesson"] = intval
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject lector Name', reply_markup=ForceReply())
    return EXPECT_SUBjECT_LECTOR_NAME

async def subject_lector_name_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    lector = None
    #try:
    with Session(engine) as session:
        stmt = select(Lector).where(Lector.name.in_([value]))
        for lc in session.scalars(stmt):
            lector = lc
    #except:
        #await context.bot.send_message(chat_id=update.effective_chat.id,
                                # text='Error')
        #return ConversationHandler.END
    
    context.user_data["subject_lector_name"] = lector.id

    name = context.user_data.get('subject_name', 'F')
    day = context.user_data.get('subject_day', 'Wednesday')
    lesson = context.user_data.get('subject_lesson', 1)
    weektype = context.user_data.get('subject_weektype', 'y')
    group = context.user_data.get('subject_group', 3)

    tmp = Subject(
        name = name,
        day = day,
        lesson  = lesson,
        weektype = weektype == 'y' if True else False,
        group = group, 
        lector_id = lector.id,
        lector = lector
    )
    with Session(engine) as session:
        session.add_all([tmp])
        session.commit()
    print(tmp.__repr__())

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Name Conversation cancelled by user. Bye.')
    return ConversationHandler.END

async def get_by_day(update: Update, context: CallbackContext):
    with Session(engine) as session:
        stmt = select(Subject).where(Subject.day.in_([context.args[0]]))
        for lc in session.scalars(stmt):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{lc.__repr__()} {lc.lector.__repr__()}")

async def get_name(update: Update, context: CallbackContext):
    name = context.user_data.get(
        'lector_name', 'Not found.')
    surname = context.user_data.get('lector_surname', 'F')
    secondname = context.user_data.get('lector_secondname', 'F')
    zoomcode = context.user_data.get('lector_zoomcode', 'F')
    zoompass = context.user_data.get('lector_zoompass', 'F')
    teams = context.user_data.get('lector_teams', 'F')
    await update.message.reply_text(f"{name} {surname} {secondname} {zoomcode} {zoompass} {teams}")

if __name__ == "__main__":
    config = open("C:/Users/nabac/OneDrive/Desktop/bot-Telegram/config.json","r")
    _config = json.loads(config.read())

    updater = ApplicationBuilder().token(_config["token"]).build()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    
    app = ApplicationBuilder().token(_config["token"]).build()

    _handlers = {}

    _handlers['start_handler'] = CommandHandler(['start','hello'], start)
    _handlers['help_handler'] = CommandHandler('help', help)
    _handlers['add_lector_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('add_lector', add_lector)],
        states={
            EXPECT_LECTOR_NAME: [MessageHandler(filters.ALL, lector_name_input_by_user)],
            EXPECT_LECTOR_SURNAME: [MessageHandler(filters.ALL, lector_surname_input_by_user)],
            EXPECT_LECTOR_SECONDNAME: [MessageHandler(filters.ALL, lector_secondname_input_by_user)],
            EXPECT_LECTOR_ZOOMCODE: [MessageHandler(filters.ALL, lector_zoomcode_input_by_user)],
            EXPECT_LECTOR_ZOOMPASS: [MessageHandler(filters.ALL, lector_zoompass_input_by_user)],
            EXPECT_LECTOR_TEAMS: [MessageHandler(filters.ALL, lector_teams_input_by_user)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    _handlers['add_subject_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('add_subject', add_subject)],
        states={
            EXPECT_SUBJECT_NAME: [MessageHandler(filters.ALL, subject_name_input_by_user)],
            EXPECT_SUBJECT_DAY: [MessageHandler(filters.ALL, subject_day_input_by_user)],
            EXPECT_SUBJECT_LESSON: [MessageHandler(filters.ALL, subject_lesson_input_by_user)],
            EXPECT_SUBJECT_WEEKTYPE: [MessageHandler(filters.ALL, subject_weektype_input_by_user)],
            EXPECT_SUBJECT_GROUP: [MessageHandler(filters.ALL, subject_group_input_by_user)],
            EXPECT_SUBjECT_LECTOR_NAME: [MessageHandler(filters.ALL, subject_lector_name_input_by_user)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    _handlers['get_by_day'] = CommandHandler('get_by_day',get_by_day)
    _handlers['get_fullname'] = CommandHandler('get_fullname',get_name)

    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        updater.add_handler(_handler)

    updater.run_polling()
