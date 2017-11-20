from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.html import escape
import datetime


# Create your models here.

class Level(models.Model):
    A0=1
    A1=2
    A2=3
    B1=4
    B2=5
    C1=6
    C2=7
    UNKNOWN=8
    LEVEL_CHOICES = (
        (A0, 'A0'),
        (A1, 'A1'),
        (A2, 'A2'),
        (B1, 'B1'),
        (B2, 'B2'),
        (C1, 'C1'),
        (C2, 'C2'),
        (UNKNOWN, 'Unbekannt'),
        )


class Teilnehmer(models.Model):
    WAIT_STATE = 1
    CHANGE_STATE = 2
    LEARNING_STATE = 3
    STATUS_CHOICES = (
        (WAIT_STATE, 'Warteliste'),
        (CHANGE_STATE, 'Bearbeitung'),
        (LEARNING_STATE, 'Schueler'),
        )
    VM = 1
    NM = 2
    AB = 3
    UN = 4
    EG = 5
    AVAIL_CHOICES = (
        (VM, 'Vormittags'),
        (NM, 'Nachmittags'),
        (AB, 'Abends'),
        (UN, 'Unbekannt'),
        (EG, 'Egal'),
        )

    name = models.CharField(max_length=200)
    geburtsdatum = models.DateField(blank=True, null=True)
    nationalitaet = models.CharField(max_length=200,blank=True)
    muttersprache = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    level = models.CharField(max_length = 3, blank=True)
    status = models.IntegerField(choices = STATUS_CHOICES, default= CHANGE_STATE)
    zeiten = models.IntegerField(choices = AVAIL_CHOICES, default= UN)
    prev_status = None
    kurse = models.ManyToManyField('Kurs', blank=True)
    sonstiges = models.TextField(max_length=500, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    wait_date = models.DateTimeField(blank=True, null = True)
    def __str__(self):
        return '%s %s' % (self.name, self.level) # escape(reverse("admin:courses_teilnehmer_change", args=(self.pk,)))
    class Meta:
        verbose_name_plural='Teilnehmer'
    def __init__(self, *args, **kwargs):
        super(Teilnehmer, self).__init__(*args, **kwargs)
        self.prev_status = self.status

    def save(self, force_insert=False, force_update=False):
        if self.wait_date is None:
            if self.prev_status != self.WAIT_STATE and self.status==self.WAIT_STATE:
                self.wait_date = datetime.datetime.now()
        #if self.prev_status == self.WAIT_STATE and self.status != self.WAIT_STATE:
            #self.wait_date = None
        self.prev_status = self.status
        super(Teilnehmer, self).save(force_insert, force_update)





class Trainer(models.Model):
    name = models.CharField(max_length=200)
    geburtsdatum = models.DateField(blank=True, null=True)
    levels = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, default='test@test.com')

    addresse = models.CharField(max_length=200, blank=True)
    telefon = models.CharField(max_length=200, blank=True)
    kurse = models.ManyToManyField('Kurs', blank=True)
    sonstiges = models.TextField(max_length=500, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='Trainer'


# class Raum(models.Model):
#     name = models.CharField(max_length=50)
#     addresse = models.CharField(max_length=200)
#     kapazitaet = models.IntegerField(default=0)
#     def __str__(self):
#             return self.name

#     class Meta:
#         verbose_name_plural='Raeume'

#     def get_absolute_url(self):
#         return reverse('event_ics_export', kwargs={'room_id': self.id})

class Kurs(models.Model):
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=3, blank=False)
    ort = models.CharField(max_length=300)
    zeit = models.CharField(max_length=300)
    kapazitaet = models.IntegerField(default=0)
    trainers = models.ManyToManyField(Trainer, through=Trainer.kurse.through, blank=True)
    teilnehmers = models.ManyToManyField(Teilnehmer, through=Teilnehmer.kurse.through, blank=True)
    sonstiges = models.TextField(max_length=500, blank=True)
    def __str__(self):
            return "%s     %d/%d" % (self.name, self.teilnehmers.count(), self.kapazitaet)
    class Meta:
        verbose_name_plural='Kurse'
        
class Anfrage(models.Model):
    betreff = models.CharField(max_length=200)
    erstellt_von = models.CharField(max_length=200)
    teilnehmer = models.ForeignKey(Teilnehmer, blank=True, null=True, on_delete=models.SET_NULL)
    inhalt = models.TextField(max_length=500, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural='Anfragen'



    
