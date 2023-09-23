from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings

from habits.models import Habit
from users.models import User
import requests

tg_token = settings.TELEGRAM_API_KEY


@shared_task
def get_chat_id():
    users = User.objects.filter(chat_id=None)
    response = requests.get(f'https://api.telegram.org/bot{tg_token}/getUpdates')
    updates = response.json()['result']
    for user in users:
        for u in updates:
            if user.telegram == u['message']['from']['username']:
                user.chat_id = u['message']['chat']['id']
                user.save()


@shared_task
def send_message():
    time_now = datetime.now()
    start_time = time_now - timedelta(minutes=1)
    finish_time = time_now + timedelta(seconds=20)
    habits = Habit.objects.filter(time__gte=start_time).filter(time__lte=finish_time)

    for habit in habits:
        message = f'Напоминание {habit.action} в {habit.time.strftime("%H:%M")}. Место выполнения: {habit.place}'
        chat_id = habit.user.chat_id

        data_for_request = {
            'chat_id': chat_id,
            'text': message
        }

        response = requests.get(f'https://api.telegram.org/bot{tg_token}/sendMessage', data_for_request)
        habit.time += timedelta(days=habit.frequency)
        habit.save()
        return response.json()
