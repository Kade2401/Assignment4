import uuid
from django.db import migrations

def fill_qr(apps, schema_editor):
    Event = apps.get_model("events", "Event")
    for e in Event.objects.filter(qr_token__isnull=True):
        e.qr_token = uuid.uuid4()
        e.save(update_fields=["qr_token"])

class Migration(migrations.Migration):
    dependencies = [
        ("events", "0010_event_description_event_invite_only_event_is_global_and_more"), 
    ]

    operations = [
        migrations.RunPython(fill_qr, migrations.RunPython.noop),
    ]
