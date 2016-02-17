from django.contrib import admin
from django import forms

# Register your models here.
from waypoints.models import Projecten

class ProjectenAdmin(admin.ModelAdmin):
    fields = ('project_name','project_status')
    list_display = ('project_name', 'username', 'DateCreated', 'project_status')
    list_filter = ['project_status', 'username']
    readonly_fields = ['project_name',]
    #project_status = MyModelForm   #http://stackoverflow.com/questions/12626171/django-admin-choice-field
    # def formfield_for_project_status(self, db_field, request, **kwargs):
    #     if db_field.name == "project_status":
    #     kwargs['project_status'] = (('accepted', 'Accepted'),('denied', 'Denied'))
    #     return super(ProjectenAdmin, self).formfield_for_project_status(db_field, request, **kwargs)


# class MyModelForm(forms.ModelForm):
#     MY_CHOICES = (
#         ('A', 'Choice A'),
#         ('B', 'Choice B'),
#     )
#    	stuff = forms.ChoiceField(choices=MY_CHOICES)

admin.site.register(Projecten, ProjectenAdmin)