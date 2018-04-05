from django.db import models
from actions.models import ActionLoggableModel


class Report_Field_Category(models.Model):
    name = models.CharField('название', max_length=255)
    order = models.IntegerField('порядок', default=10)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Report_field_categories'

    def __str__(self):
        return self.name


class Report_Field_Type(models.Model):
    category = models.ForeignKey(
        'Report_Field_Category',
        verbose_name='категория')
    name = models.CharField('название', max_length=255)
    placeholder = models.TextField('подсказка', blank=True)
    project_types = models.ManyToManyField(
        'projects.Project_type',
        blank=True,
        verbose_name='типы проектов')
    has_status = models.BooleanField('имеет статус', default=True)
    has_url = models.BooleanField('имеет ссылку', default=True)
    order = models.IntegerField('порядок', default=10)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return self.name


class Report_Field(ActionLoggableModel):
    OK = 'OK'
    PRC = 'PRC'
    MINPR = 'MINPR'
    MAJPR = 'MAJPR'
    NN = 'NN'
    NA = 'NA'

    STATUSES = (
        (OK, 'Выполнено'),
        (PRC, 'Выполняется'),
        (MINPR, 'Есть проблемы'),
        (MAJPR, 'Требуется решение проблем'),
        (NA, 'Не актуально'),
        (NN, 'Не требуется'),
    )

    field_type = models.ForeignKey('Report_Field_Type', verbose_name='тип поля')
    content = models.TextField('содержание', blank=True)
    status = models.CharField('статус', max_length=10, blank=True, choices=STATUSES)
    link = models.URLField('ссылка', blank=True)
    link_description = models.CharField('описание ссылки', max_length=255, blank=True)
    project = models.ForeignKey('projects.Project', verbose_name='проект')
    date = models.DateTimeField('дата редактирования', auto_now=True)

    class Meta:
        ordering = ['field_type']
        unique_together = ('project', 'field_type',)

    def __str__(self):
        return '{tp} отчета {pr}'.format(
            tp=str(self.field_type),
            pr=str(self.project))
