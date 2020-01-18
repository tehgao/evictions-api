from django.contrib import admin
from cases.models import Address, Party, Attorney, Case, Event

case_models = [Address, Party, Attorney, Case, Event]
admin.site.register(case_models)
