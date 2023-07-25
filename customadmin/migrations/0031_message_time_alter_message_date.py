from django.db import migrations, models
import datetime

def convert_to_date(apps, schema_editor):
    Message = apps.get_model('customadmin', 'Message')
    for message in Message.objects.all():
        # Extract the date from the existing "date" field
        date_with_time = message.date
        converted_date = date_with_time.date()
        message.date_with_time = date_with_time
        message.date = converted_date
        message.save()

class Migration(migrations.Migration):

    dependencies = [
        ('customadmin', '0030_message_datetime_alter_message_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_with_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.RunPython(convert_to_date),
        migrations.RemoveField(
            model_name='message',
            name='date',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='date_with_time',
            new_name='date',
        ),
    ]
