# Generated migration for BlacklistedIP model

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = False

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('reason', models.CharField(blank=True, max_length=255)),
                ('attempt_count', models.PositiveIntegerField(default=1)),
                ('first_attempt', models.DateTimeField(auto_now_add=True)),
                ('last_attempt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-last_attempt'],
            },
        ),
    ]
