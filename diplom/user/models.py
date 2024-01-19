from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    course = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Course of the student"))

    def save(self, *args, **kwargs):
        self.course = 1
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')