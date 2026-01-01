from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_add_team_members_id'),
    ]

    operations = [
        # This migration uses PostgreSQL-specific syntax, skipped for SQLite
        migrations.RunSQL(
            sql=migrations.RunSQL.noop,
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
