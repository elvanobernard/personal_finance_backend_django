# Generated by Django 4.1.2 on 2022-10-12 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finances_record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashentry',
            name='cash_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='finances_record.cashaccount'),
        ),
        migrations.AlterField(
            model_name='expenseentry',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='finances_record.expensecategory'),
        ),
        migrations.AlterField(
            model_name='expenseentry',
            name='monthly_summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='finances_record.monthlyexpensesummary'),
        ),
        migrations.AlterField(
            model_name='incomeentry',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='finances_record.incomecategory'),
        ),
        migrations.AlterField(
            model_name='incomeentry',
            name='monthly_summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entries', to='finances_record.monthlyincomesummary'),
        ),
        migrations.AlterField(
            model_name='monthlyexpensesummary',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monthly_summaries', to='finances_record.expensecategory'),
        ),
        migrations.AlterField(
            model_name='monthlyincomesummary',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monthly_summaries', to='finances_record.incomecategory'),
        ),
    ]
