# Generated by Django 4.2.11 on 2024-03-19 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0002_alter_item_assigned_alter_item_attachments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='kanban.board'),
        ),
    ]
