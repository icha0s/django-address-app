import django.db.models.deletion
from django.db import migrations, models

import swapper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('code', models.CharField(blank=True, default='', max_length=2, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ('name',),
                'abstract': False,
                'swappable': swapper.swappable_setting("django_address", "Country"),
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('code', models.CharField(blank=True, default='', max_length=5, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
                'ordering': ('region', 'name'),
                'abstract': False,
                'swappable': swapper.swappable_setting("django_address", "District"),
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('postal_code', models.CharField(blank=True, default='', max_length=10, verbose_name='Postal code')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='localities', to=swapper.get_model_name("django_address", "District"), verbose_name='District')),
            ],
            options={
                'verbose_name': 'Locality',
                'verbose_name_plural': 'Localities',
                'ordering': ('region', 'district', 'name'),
                'abstract': False,
                'swappable': swapper.swappable_setting("django_address", "Locality"),
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Street name')),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=swapper.get_model_name("django_address", "Locality"), verbose_name='Locality')),
            ],
            options={
                'verbose_name': 'Street',
                'verbose_name_plural': 'Streets',
                'ordering': ('name',),
                'abstract': False,
                'swappable': swapper.swappable_setting("django_address", "Street"),
                'unique_together': {('locality', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('code', models.CharField(blank=True, default='', max_length=5, verbose_name='Code')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=swapper.get_model_name("django_address", "Country"), verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
                'ordering': ('country', 'name'),
                'abstract': False,
                'swappable': swapper.swappable_setting("django_address", "REGION"),
                'unique_together': {('name', 'country')},
            },
        ),
        migrations.AddField(
            model_name='locality',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localities', to=swapper.get_model_name("django_address", "Region"), verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to=swapper.get_model_name("django_address", "Region"), verbose_name='Region'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw', models.CharField(blank=True, default='', max_length=256, verbose_name='Raw')),
                ('route', models.CharField(default='', max_length=256, verbose_name='Route')),
                ('street_number', models.CharField(blank=True, default='', max_length=20, verbose_name='Street number')),
                ('formatted_address', models.CharField(blank=True, default='', max_length=200, verbose_name='Formatted address')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='Longitude')),
                ('apartment', models.CharField(blank=True, default='', max_length=10, verbose_name='Apartment')),
                ('locality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=swapper.get_model_name("django_address", "Locality"), verbose_name='Locality')),
                ('street', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=swapper.get_model_name("django_address", "Street"), verbose_name='Street')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'abstract': False,
                'swappable': swapper.swappable_setting("django_address", "Address"),
            },
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together={('name', 'region')},
        ),
    ]
