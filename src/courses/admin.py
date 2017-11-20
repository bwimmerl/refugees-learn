from django import forms
from django.contrib import admin
from django.contrib.sites.models import Site

# Register your models here.
from .models import Kurs, Teilnehmer, Trainer, Level, Anfrage
from django.core.urlresolvers import reverse

class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Kurs
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        #if kurs:
        self.fields['teilnehmers'].queryset = Teilnehmer.objects.filter(status=Teilnehmer.WAIT_STATE).order_by('wait_date')

    
    
class AnfrageInline(admin.StackedInline):
    model= Anfrage
    extra = 1
    classes = ['collapse']
    
class AnfrageAdmin(admin.ModelAdmin):
    list_display = ('teilnehmer', 'betreff', 'erstellt_von', 'date')
    



class CourseAdmin(admin.ModelAdmin):
    def get_free(self, obj):
        return "%s/%s" % (obj.teilnehmers.count(), obj.kapazitaet)
    get_free.short_description = 'Freie Plaetze'
    get_free.allow_tags = True    
    def get_trainer(self,obj):
        trainer = obj.trainers.all()
        return ' + '.join([t.name for t in trainer])


    list_display = ('name','get_free', 'get_trainer', 'ort', 'zeit')
    form = CourseModelForm
    filter_horizontal = ('teilnehmers', 'trainers',)
    readonly_fields = ('teilnehmerliste', 'get_free')

    fieldsets = (
        (None, {
            'fields': ('name', ('level', 'kapazitaet'), ('ort', 'zeit',), 'trainers', ('teilnehmers', 'teilnehmerliste'))
            }),
        )

    
    get_trainer.short_description = 'Trainer'


    def teilnehmerliste(self,obj):
        url = reverse('admin:courses_teilnehmer_changelist')
        return '<a href="{0}?kurse__id__exact={1}">Teilnehmerliste</a>'.format(url, obj.id)
    teilnehmerliste.allow_tags = True

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name','geburtsdatum', 'nationalitaet', 'muttersprache', 'get_kurse', 'level', 'status', 'zeiten', 'wait_date', 'join_date')
    list_filter = ('zeiten', 'status',)
    fieldsets = (
        (None, {
            'fields': ('name','geburtsdatum', 'nationalitaet', 'muttersprache', 'level', 'status', 'zeiten',)
        }),
        (None, {
            'classes': ('wide',),
            'fields': ('kurse',),
        }),
        ('Mehr', {
            'classes': ('collapse',),
            'fields': ('sonstiges', 'wait_date'),
        }),
    )
    search_fields = ['name', 'level', 'nationalitaet',]
    filter_horizontal = ('kurse',)
    inlines = [AnfrageInline]
    
    def get_kurse(self,obj):
        t = obj.kurse.all()
        return ' | '.join([t.name for t in t])
   

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'levels', 'geburtsdatum')
    search_fields= ['name', 'levels']
    filter_horizontal = ('kurse',)



admin.site.register(Kurs, CourseAdmin)
admin.site.register(Teilnehmer, ParticipantAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Anfrage, AnfrageAdmin)
admin.site.unregister(Site)
#admin.site.register(Termin, admin.ModelAdmin)
