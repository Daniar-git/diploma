from django.db import models
from django.utils.translation import gettext_lazy as _

from diplom.common.models import Base
from diplom.user.models import User


class Petition(Base):
    user = models.ForeignKey(User, verbose_name=_("User created petition"), on_delete=models.SET_NULL, null=True)
    title = models.CharField(verbose_name=_("Title of petition"), max_length=255)
    description = models.TextField(verbose_name=_("Description of petition"))


class Likes(Base):
    user = models.ForeignKey(User, verbose_name=_("User liked petition"), on_delete=models.SET_NULL, null=True)
    petition = models.ForeignKey(Petition, verbose_name=_("Petition liked by user"), on_delete=models.SET_NULL, null=True)


class Dislikes(Base):
    user = models.ForeignKey(User, verbose_name=_("User disliked petition"), on_delete=models.SET_NULL, null=True)
    petition = models.ForeignKey(Petition, verbose_name=_("Petition disliked by user"), on_delete=models.SET_NULL, null=True)


class Comment(Base):
    user = models.ForeignKey(User, verbose_name=_("User commented petition"), on_delete=models.SET_NULL, null=True)
    petition = models.ForeignKey(Petition, verbose_name=_("Petition commented by user"), on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name=_("comment for petition"))