from django.db import models
from django.contrib.auth.models import User

from main.current_user import get_current_user


class Action(models.Model):
    NEW = 'NEW'
    EDIT = 'EDIT'
    DEL = 'DEL'

    ACTIONS = (
        (NEW, 'Создание'),
        (EDIT, 'Редактирование'),
        (DEL, 'Удаление'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        default=get_current_user,
        related_name='actions',
        blank=True,
        null=True)
    time = models.DateTimeField('дата действия', auto_now_add=True)
    action = models.CharField('тип действия', max_length=10, choices=ACTIONS)
    obj_name = models.TextField('наименование объекта', blank=True)
    obj_url = models.URLField('ссылка на объект', blank=True)

    class Meta:
        ordering = ['time', ]

    def __str__(self):
        return '{action} пользователем {user} в {time:%H-%M %d.%m.%y}'.format(
            action=self.get_action_display(),
            user=self.user,
            time=self.time)


class ActionLoggableModel(models.Model):
    actions = models.ManyToManyField('actions.Action', related_name='+')

    class Meta:
        abstract = True

    @property
    def url(self):
        return ''

    def save(self, *args, **kwargs):
        if self.id:
            act = Action.EDIT
        else:
            act = Action.NEW

        super(ActionLoggableModel, self).save(*args, **kwargs)

        self.actions.add(
            Action.objects.create(
                action=act,
                obj_name=str(self),
                obj_url=self.url))

    def delete(self, *args, **kwargs):
        Action.objects.create(
            action=Action.DEL,
            obj_name=str(self))

        super(ActionLoggableModel, self).delete(*args, **kwargs)
