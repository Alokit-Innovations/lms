from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_sync_schema'),
    ]

    operations = [
        # This migration uses PostgreSQL-specific syntax, skipped for SQLite
        migrations.RunSQL(
            sql=migrations.RunSQL.noop,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
