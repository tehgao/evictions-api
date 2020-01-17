from django.contrib import admin
from cases.models import Address, Party, Person, Attorney, Company, Case, Event

case_models = [Address, Party, Person,
               Attorney, Company, Case, Event]
admin.site.register(case_models)
