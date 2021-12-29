from django.contrib import admin
from .models import Respondent, Submit, Answer

admin.site.register(Answer)
admin.site.register(Submit)
admin.site.register(Respondent)
