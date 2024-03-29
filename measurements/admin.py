from django.contrib import admin
from .models import Measurement
from django.contrib.auth.models import Group
# Register your models here.

admin.site.site_header = "System SIG NoSql Admin Panel "
admin.site.site_title = "System SIG NoSql "
# admin.site.index_title = "Bonjour Dans Projet SIG NOSqls"

# class InlineName(admin.StackedInline ): 
#     model = modelName
# ou bien vous pouvez utiliser 
# class InlineName(admin.TabularInline ): 
#     model = modelName
# pour remplir une tableau a partir d'une autre tableau avec la quel il ya une relation 
# class modelNameadmin(admin.ModelAdmin):
#     inlines = [InlineTopic]
#     extra = 1 

class  MeasurementAdmin(admin.ModelAdmin):
    fields = ['destination']
    list_display = ['address','location','destination','distance','created','combine_destination_and_distance']
    list_display_links = ['location','combine_destination_and_distance']
    list_editable = ['destination']
    list_filter = ['location','destination','distance','created']
    search_fields = ['location','destination','distance']
    
    def combine_destination_and_distance(self,obj):
        return "{} - {}".format(obj.destination,obj.distance)

admin.site.register(Measurement, MeasurementAdmin)
admin.site.unregister(Group)