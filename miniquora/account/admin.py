from django.contrib import admin
from .models import MyUser

@admin.register(MyUser)

class ACtiveUserAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','is_active','is_superuser','username']
    search_fields=['first_name','username','email']
    '''
    def get_queryset(self,request):
        return self.model.objects.filter(is_superuser=True)
    '''
   # actions_on_bottom=True
# Register your models here.
