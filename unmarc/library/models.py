from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import ShortIdToLowerCaseMixin


class Library(ShortIdToLowerCaseMixin, models.Model):
    name = models.CharField(_('official name of the library'),
                            max_length=160,
                            help_text=_('Eg. "Asiatic Society Library", "Buguri Children\'s Library" etc.'))

    short_id = models.SlugField(_('unique short label'),
                                max_length=32,
                                unique=True,
                                allow_unicode=True,
                                help_text=_('A unique identifier for the library (similar to a user\'s username). '
                                            'Eg. "buguri", "asiatic-society" etc.<br/>'
                                            'Only letters, numbers, underscores or hyphens (no spaces) allowed.'))

    class Meta:
        verbose_name_plural = 'Libraries'

    def __str__(self):
        return self.name


class Branch(ShortIdToLowerCaseMixin, models.Model):
    name = models.CharField(max_length=160)

    library = models.ForeignKey(Library,
                                on_delete=models.CASCADE,
                                related_name='branches',
                                verbose_name=_('belongs to library'))

    address = models.CharField(max_length=255, blank=True)

    short_id = models.SlugField(_('unique short label'),
                                max_length=32,
                                unique=True,
                                allow_unicode=True,
                                help_text=_('A unique identifier for the branch (similar to a user\'s username). '
                                            'Eg. "mg-road", "santacruz-west-2" etc.<br/>'
                                            'Only letters, numbers, underscores or hyphens (no spaces) allowed.'))

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name
