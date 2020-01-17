from django.db import models
from polymorphic.models import PolymorphicModel


class Address(models.Model):
    street_address = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return '{} {}\n{}, {} {}'.format(self.street_address, self.street_address_2, self.city, self.state, self.zip)


class Party(PolymorphicModel):
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, blank=True, null=True)


class Person(Party):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Attorney(Person):
    associated_party = models.ForeignKey(Party, on_delete=models.CASCADE)


class Company(Party):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Case(models.Model):
    case_number = models.CharField(max_length=255)
    file_date = models.DateField()
    plaintiffs = models.ManyToManyField(Party, related_name='case_plaintiffs')
    defendants = models.ManyToManyField(Party, related_name='case_defendants')
    additional_parties = models.ManyToManyField(
        Party, blank=True)

    def __str__(self):
        return self.case_number


class Event(models.Model):
    TYPES = (
        ('FC', 'First Cause Hearing'),
        ('SC', 'Second Cause Hearing')
    )
    event_type = models.CharField(choices=TYPES, max_length=2)
    is_pro_se = models.BooleanField()
    date_time = models.DateTimeField()

    assoc_case = models.ForeignKey(Case, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_type
