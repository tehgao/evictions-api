# Generated by Django 3.0.2 on 2020-01-18 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=255)),
                ('street_address_2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.CharField(max_length=255)),
                ('file_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cases.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('FC', 'First Cause Hearing'), ('SC', 'Second Cause Hearing')], max_length=2)),
                ('is_pro_se', models.BooleanField()),
                ('date_time', models.DateTimeField()),
                ('assoc_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='additional_parties',
            field=models.ManyToManyField(blank=True, to='cases.Party'),
        ),
        migrations.AddField(
            model_name='case',
            name='defendants',
            field=models.ManyToManyField(related_name='case_defendants', to='cases.Party'),
        ),
        migrations.AddField(
            model_name='case',
            name='plaintiffs',
            field=models.ManyToManyField(related_name='case_plaintiffs', to='cases.Party'),
        ),
        migrations.CreateModel(
            name='Attorney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('associated_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Party')),
            ],
        ),
    ]
