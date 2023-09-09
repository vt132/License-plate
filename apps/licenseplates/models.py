from django.db import models
from django.utils.translation import gettext_lazy as _


class Plate(models.Model):
    """License plate model.

        number: plate number
        wanted: check if plate is (criminally) wanted
    """
    number = models.CharField(
        max_length=255,
        verbose_name=_("number"),
        unique=True,
    )
    wanted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.number

    class Meta:
        verbose_name = _("License plate")
