from django.db import migrations

def set_owner(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    User = apps.get_model('auth', 'User')
    admin = User.objects.first()

    for event in Event.objects.filter(owner__isnull=True):
        event.owner = admin
        event.save()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_owner'),
    ]

    operations = [
        migrations.RunPython(set_owner),
    ]
