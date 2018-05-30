from django.contrib import admin
from . models import Project, Test_Plan,Bug, Test_Classification,Topic,Short_Name
 
 
 
 
class Test_ClassificationAdmin(admin.ModelAdmin):  
  list_display = ('name', 'topic', 'frequency')
  ordering = ('name',) # The negative sign indicate descendent order

class TopicAdmin(admin.ModelAdmin):  
  list_display = ('name',)
  ordering = ('name',) # The negative sign indicate descendent order

class Short_NameAdmin(admin.ModelAdmin):  
  list_display = ('name','shortName')
  ordering = ('name',) # The negative sign indicate descendent order



#admin.site.register(Abbreviation)
admin.site.register(Project)
admin.site.register(Test_Plan)
admin.site.register(Bug)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Test_Classification, Test_ClassificationAdmin)
admin.site.register(Short_Name, Short_NameAdmin)