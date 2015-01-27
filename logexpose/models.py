from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Record(models.Model):

    time = models.DateTimeField(_('Logged at'))
    logger = models.CharField(_('Logger'), max_length=50)
    lvl = models.CharField(_('Level'), max_length=20)
    msg = models.TextField(_('Message'))
    gid = models.CharField(_('Group ID'), max_length=200)
    mid = models.CharField(_('Message ID'), max_length=200)
    pid = models.CharField(_('Parent ID'), max_length=200, null=True)
    props = models.TextField(_('Properties'))

    class Meta:
        verbose_name = _('Record')
        verbose_name_plural = _('Records')

    def __str__(self):
        return '%s %s: %s' % (self.time, self.lvl.upper(), self.msg)
