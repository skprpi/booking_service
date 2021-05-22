from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Price)
admin.site.register(Lesson)
admin.site.register(PriceDiscipline)
admin.site.register(Discipline)
admin.site.register(DisciplineDescription)