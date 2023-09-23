from django.db import models


from users.models import NULLABLE, User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    place = models.CharField(max_length=200, verbose_name='Место')
    time = models.DateTimeField(verbose_name='Время')
    action = models.CharField(max_length=300, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Связанная привычка')
    frequency = models.SmallIntegerField(default=1, verbose_name='Периодичность')
    reward = models.CharField(max_length=200, **NULLABLE, verbose_name='Вознаграждение')
    execution_time = models.TimeField(default='00:01:00', verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('id',)
