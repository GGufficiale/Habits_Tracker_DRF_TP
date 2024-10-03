from celery import shared_task
from habits.models import Habits

import datetime
from habits.services import send_telegram_message


@shared_task
def send_habit():
    habits = Habits.objects.all()
    current_date = datetime.datetime.now()  # Текущее время
    for habit in habits:
        if habit.time == current_date:
            tg_chat = habit.user.tg_chat_id
            message = f"Я буду {habit.action} в {habit.time} в {habit.place}."
            send_telegram_message(tg_chat, message)  # Отправляем привычку в Telegram чат
