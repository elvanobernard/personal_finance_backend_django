# Generated by Django 4.1.1 on 2022-09-15 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finances_record', '0002_alter_expenseentry_monthly_summary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashentry',
            name='cash_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cash_entries', to='finances_record.cashaccount'),
        ),
        migrations.AlterField(
            model_name='cashentry',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_entries', to='finances_record.transaction'),
        ),
        migrations.AlterField(
            model_name='expenseentry',
            name='expense_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expense_entries', to='finances_record.expensecategory'),
        ),
        migrations.AlterField(
            model_name='expenseentry',
            name='monthly_summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_entries', to='finances_record.monthlyexpensesummary'),
        ),
        migrations.AlterField(
            model_name='expenseentry',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_entries', to='finances_record.transaction'),
        ),
        migrations.AlterField(
            model_name='incomeentry',
            name='income_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='income_entries', to='finances_record.incomecategory'),
        ),
        migrations.AlterField(
            model_name='incomeentry',
            name='monthly_summary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='income_entries', to='finances_record.monthlyincomesummary'),
        ),
        migrations.AlterField(
            model_name='incomeentry',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income_entries', to='finances_record.transaction'),
        ),
        migrations.AlterField(
            model_name='monthlyincomesummary',
            name='income_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monthly_income_summaries', to='finances_record.incomecategory'),
        ),
        migrations.AlterField(
            model_name='payable',
            name='cash_entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payables', to='finances_record.cashentry'),
        ),
        migrations.AlterField(
            model_name='payable',
            name='expense_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payables', to='finances_record.expenseentry'),
        ),
        migrations.AlterField(
            model_name='receivable',
            name='cash_entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='receivables', to='finances_record.cashentry'),
        ),
        migrations.AlterField(
            model_name='receivable',
            name='income_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receivables', to='finances_record.incomeentry'),
        ),
    ]
