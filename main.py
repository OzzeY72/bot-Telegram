import logging
import webbrowser
import json
import os
import shutil

import datetime
from datetime import timedelta, timezone 

#from telegram.ext.messagehandler import MessageHandler
from telegram import Update
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from sqlalchemy import create_engine
from models import Base, Lector, Subject, BindAlarm, Moderator
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_

SRC_PATH = "/app/db/"

engine = create_engine(f"sqlite+pysqlite:///{SRC_PATH}database.db", echo=True)

EXPECT_LECTOR_NAME, EXPECT_LECTOR_SURNAME, EXPECT_LECTOR_SECONDNAME,EXPECT_LECTOR_ZOOMCODE,EXPECT_LECTOR_ZOOMPASS,EXPECT_LECTOR_TEAMS = range(6)
EXPECT_SUBJECT_NAME, EXPECT_SUBJECT_DAY, EXPECT_SUBJECT_LESSON, EXPECT_SUBJECT_WEEKTYPE, EXPECT_SUBJECT_GROUP, EXPECT_SUBjECT_LECTOR_NAME = range(6)

WEEK_TYPE = 1 if datetime.date.today().isocalendar().week % 2 == 0 else 2 
DAY_NUMBER = datetime.date.today().weekday() + 1
CURRENT_LESSON = 0

print (WEEK_TYPE)

def day_convert(num):
    if num == 1:
        return ['Monday','Понеділок','Понедельник']
    elif num == 2:
        return ['Tuesday','Вівторок','Вторник']
    elif num == 3:
        return ['Wednesday','Середа','Среда']
    elif num == 4:
        return ['Thursday','Четверг','Четвер']
    elif num == 5:
        return ['Friday',"П'ятниця","Пятница"]
    elif num == 6:
        return ['Saturday','Суббота','Субота']
    else:
        return ['Sunday','Неділя','Воскресенье']

def intday_convert(str):
    if str in ['Monday','Понеділок','Понедельник']:
        return 1
    elif str in ['Tuesday','Вівторок','Вторник']:
        return 2
    elif str in ['Wednesday','Середа','Среда']:
        return 3
    elif str in ['Thursday','Четверг','Четвер']:
        return 4
    elif str in ['Friday',"П'ятниця","Пятница"]:
        return 5
    elif str in ['Saturday','Суббота','Субота']:
        return 6
    else:
        return 7

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"<b>Привіт, {update.effective_user.first_name}, я бот ІННІ</b>",parse_mode='html')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await context.bot.send_message(chat_id=update.effective_chat.id,text="<b>Всі мої можливості: </b>",parse_mode='html')

async def add_lector(update: Update, context: CallbackContext):
    tmpflag = False
    with Session(engine) as session:
        for moderator in session.query(Moderator).all():
            if int(moderator.telid) == update.effective_chat.id:
                tmpflag = True
    if tmpflag:
        await context.bot.send_message(chat_id=update.effective_chat.id,text = 'Creating Lector')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send lector name', reply_markup=ForceReply())
        return EXPECT_LECTOR_NAME
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text = 'You dont have permission')
        return ConversationHandler.END
    
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
        isteams = True if teams == 'y' else False
    )
    print(tmp.__repr__())
    with Session(engine) as session:
        session.add_all([tmp])
        session.commit()
    return ConversationHandler.END

async def add_subject(update: Update, context: CallbackContext):
    flag = False
    with Session(engine) as session:
        for moderator in session.query(Moderator).all():
            if int(moderator.telid) == update.effective_chat.id:
                flag = True
    if flag:
        await context.bot.send_message(chat_id=update.effective_chat.id,text = 'Creating Subject')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject name', reply_markup=ForceReply())
        return EXPECT_SUBJECT_NAME
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text = 'You dont have permission')
        return ConversationHandler.END

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
    
    context.user_data["subject_group"] = intval
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Send subject lector Surname', reply_markup=ForceReply())
    return EXPECT_SUBjECT_LECTOR_NAME

async def subject_lector_name_input_by_user(update: Update, context: CallbackContext):
    value = update.message.text
    lector = None
    #try:
    with Session(engine) as session:
        lector = session.query(Lector).where(Lector.surname.in_([value])).first()
    #except:
        #await context.bot.send_message(chat_id=update.effective_chat.id,
                                # text='Error')
        #return ConversationHandler.END
    
    #context.user_data["subject_lector_name"] = lector.id

    name = context.user_data.get('subject_name', 'F')
    day = context.user_data.get('subject_day', 'Wednesday')
    lesson = context.user_data.get('subject_lesson', 1)
    weektype = context.user_data.get('subject_weektype', 3)
    group = context.user_data.get('subject_group', 3)
    if lector is not None:
        tmp = Subject(
            name = name,
            day = day,
            lesson  = lesson,
            weektype = weektype,
            group = group, 
            lector_id = lector.id,
            lector = lector
        )
        with Session(engine) as session:
            session.add_all([tmp])
            session.commit()
        print(tmp.__repr__())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Invalid lector surname')
        
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Name Conversation cancelled by user. Bye.')
    return ConversationHandler.END

async def get_by_day(update: Update, context: CallbackContext):
    check_week = WEEK_TYPE
    сheck_day = context.args[0] if len(context.args) > 0 else day_convert(DAY_NUMBER)[1]
    if intday_convert(сheck_day) < DAY_NUMBER:
        if check_week == 1:
            check_week = 2
        else:
            check_week = 1
    with Session(engine) as session:
        cond = and_(Subject.day.in_([сheck_day]), or_(Subject.weektype == check_week, Subject.weektype == 3))
        stmt = select(Subject,Lector).join(Subject.lector).where(cond)
        for lc in session.scalars(stmt):
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{lc.__repr__()}",parse_mode='html')

async def week_type(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{'Чисельник' if WEEK_TYPE == 1 else 'Знаменник'}",parse_mode='html')

async def poll_handle(context: CallbackContext):
    WEEK_TYPE = 1 if datetime.date.today().isocalendar().week % 2 == 0 else 2 
    DAY_NUMBER = datetime.date.today().weekday() + 1

    hour = datetime.datetime.now(timezone.utc).hour+2
    minut = hour * 60 + datetime.datetime.now().minute

    print(minut)
    print('Чисельник' if WEEK_TYPE == 1 else 'Знаменник')
    print(DAY_NUMBER)   

    if minut < 9*60+35:
        CURRENT_LESSON = 1
    elif minut >= 9*60+35 and minut < 11*60+25:
        CURRENT_LESSON = 2
    elif minut >= 11*60+25 and minut < 12*60+55:
        CURRENT_LESSON = 3
    elif minut >= 12*60+55 and minut < 14*60+30:
        CURRENT_LESSON = 4
    elif minut >= 14*60+30 and minut < 16*60:
        CURRENT_LESSON = 5
    else:
        CURRENT_LESSON = 6
    
    print(CURRENT_LESSON)
    if minut == 7*60+50 or minut == 9*60+25 or minut == 11*60+15 or minut == 12*60+45 or minut == 14*60+20 or minut == 15*60+50:
        try:
            with Session(engine) as session:
                for ba in session.query(BindAlarm).all():
                    if ba.alarm:
                        await next(int(ba.telid),context, True,True)
        except:
            print("Error quering db in poll_handle")
        

async def next(telid, context: ContextTypes.DEFAULT_TYPE, strict_next: bool,lesson_strict=CURRENT_LESSON,once=False):
    try:
        with Session(engine) as session:
            returned = False
            count = 0
            check_day = DAY_NUMBER
            check_week = WEEK_TYPE
            check_lesson = CURRENT_LESSON if not strict_next else lesson_strict
            while not returned:
                if not strict_next:
                    cond = and_(Subject.day.in_(day_convert(check_day)),Subject.lesson > check_lesson)
                else:
                    cond = and_(Subject.day.in_(day_convert(DAY_NUMBER)),Subject.lesson == check_lesson+1)
                cond2 = and_(cond,or_(Subject.weektype == check_week, Subject.weektype == 3))
            #stmt = select(Subject,Lector).join(Subject.lector).where(cond2)
                for sub in session.query(Subject,Lector).join(Subject.lector).where(cond2):#session.scalars(stmt):
                    returned = True
                    await context.bot.send_message(chat_id=telid,
                                 text=f"{sub[0].__repr__()}",parse_mode='html')
                if strict_next: break
                check_lesson = 0
                if check_day <= 6:
                    check_day = check_day+1
                else:
                    check_day = 1
                    if check_week == 1:
                        check_week = 2
                    else:
                        check_week = 1
                if count > 7: break
                count+=1
                if once: return
    except:
        print("Error while requesting database")

async def next_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await next(update.effective_chat.id,context,False,once=True)
async def now_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await next(update.effective_chat.id,context,True,CURRENT_LESSON-1,True)

async def allow_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with Session(engine) as session:
            exists = session.query(BindAlarm.alarm).filter_by(telid=update.effective_chat.id).first()
            if exists is not None:
                session.query(BindAlarm).where(BindAlarm.telid.in_([update.effective_chat.id])).update({BindAlarm.alarm: not exists[0]})
                exists = exists[0]
            else:
                session.add(BindAlarm(telid = update.effective_chat.id,alarm = True))
                exists = False
            session.commit()
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Сповіщення {'увімкненно' if not exists else 'вимкнено'}",parse_mode='Markdown')
    except:
        print("Error while requesting database")

if __name__ == "__main__":
    config = open(f"{SRC_PATH}config.json","r")
    _config = json.loads(config.read())

    updater = ApplicationBuilder().token(_config["token"]).job_queue(JobQueue()).build()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.ERROR
    )
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
    _handlers['get_by_day'] = CommandHandler('day',get_by_day)
    _handlers['next'] = CommandHandler('next',next_command)
    _handlers['allow_alarm'] = CommandHandler('alarm',allow_alarm)
    _handlers['now'] = CommandHandler('now', now_command)
    _handlers['week_type'] = CommandHandler('week_type', week_type)

    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        updater.add_handler(_handler)
    updater.job_queue.run_repeating(poll_handle, timedelta(minutes=1),first=5)

    updater.run_polling()
