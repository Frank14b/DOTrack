# Generated by Django 2.0 on 2018-06-08 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acceder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'acceder',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(blank=True, max_length=254, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('password', models.CharField(blank=True, max_length=254, null=True)),
                ('dates', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'admin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Archives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('descript', models.CharField(blank=True, max_length=254, null=True)),
                ('dates', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'archives',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('dates', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'chat',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cicursale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pays', models.CharField(blank=True, max_length=254, null=True)),
                ('ville', models.CharField(blank=True, max_length=254, null=True)),
                ('tel1', models.IntegerField(blank=True, null=True)),
                ('tel2', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'cicursale',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Courriers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intituler', models.CharField(blank=True, max_length=254, null=True)),
                ('expediteur', models.CharField(blank=True, max_length=254, null=True)),
                ('recepteur', models.CharField(blank=True, max_length=254, null=True)),
                ('datee', models.DateTimeField(blank=True, db_column='dateE', null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('tel', models.IntegerField(blank=True, null=True)),
                ('dater', models.DateTimeField(blank=True, db_column='dateR', null=True)),
                ('cic', models.ForeignKey(db_column='Cic_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Cicursale')),
            ],
            options={
                'db_table': 'courriers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('descipt', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('dates', models.CharField(blank=True, max_length=254, null=True)),
                ('cic', models.ForeignKey(db_column='Cic_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Cicursale')),
            ],
            options={
                'db_table': 'documents',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Dossiers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('abreviation', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('dates', models.CharField(blank=True, max_length=254, null=True)),
                ('cic', models.ForeignKey(db_column='Cic_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Cicursale')),
                ('dos', models.ForeignKey(blank=True, db_column='Dos_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Dossiers')),
            ],
            options={
                'db_table': 'dossiers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('descript', models.CharField(blank=True, max_length=254, null=True)),
                ('slogan', models.CharField(blank=True, max_length=254, null=True)),
                ('logo', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('web', models.CharField(blank=True, max_length=254, null=True)),
                ('dates', models.DateTimeField(blank=True, db_column='dates', null=True)),
                ('tel', models.CharField(blank=True, max_length=254, null=True)),
                ('adm', models.ForeignKey(db_column='Adm_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Admin')),
            ],
            options={
                'db_table': 'entreprise',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Fichierc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libeler', models.CharField(blank=True, max_length=254, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('cou', models.ForeignKey(db_column='Cou_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Courriers')),
            ],
            options={
                'db_table': 'fichierc',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('extension', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('ent', models.ForeignKey(db_column='Ent_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Entreprise')),
            ],
            options={
                'db_table': 'format',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libele', models.CharField(blank=True, max_length=254, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('modules', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'module',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Mouchard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.CharField(blank=True, max_length=254, null=True)),
                ('ip', models.CharField(blank=True, max_length=254, null=True)),
                ('tache', models.CharField(blank=True, max_length=254, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('adm', models.ForeignKey(db_column='Adm_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Admin')),
                ('ent', models.ForeignKey(db_column='Ent_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Entreprise')),
            ],
            options={
                'db_table': 'mouchard',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Perception',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'perception',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rangement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('code', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('ran', models.ForeignKey(blank=True, db_column='Ran_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Rangement')),
            ],
            options={
                'db_table': 'rangement',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Resultat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('fichier', models.CharField(blank=True, max_length=254, null=True)),
                ('dates', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('dos', models.ForeignKey(db_column='Dos_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Dossiers')),
            ],
            options={
                'db_table': 'resultat',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Traitement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datep', models.DateTimeField(blank=True, db_column='dateP', null=True)),
                ('datet', models.DateTimeField(blank=True, db_column='dateT', null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('observation', models.CharField(blank=True, max_length=254, null=True)),
                ('doc', models.ForeignKey(db_column='Doc_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Documents')),
            ],
            options={
                'db_table': 'traitement',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Typearchives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(blank=True, max_length=254, null=True)),
                ('code', models.CharField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, max_length=254, null=True)),
                ('ent', models.ForeignKey(db_column='Ent_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Entreprise')),
            ],
            options={
                'db_table': 'typearchives',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Typecourrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libeler', models.CharField(blank=True, max_length=254, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('abreviation', models.CharField(blank=True, max_length=254, null=True)),
                ('ent', models.ForeignKey(db_column='Ent_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Entreprise')),
                ('typ', models.ForeignKey(blank=True, db_column='Typ_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typecourrier')),
            ],
            options={
                'db_table': 'typecourrier',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Typefich',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libeler', models.CharField(blank=True, max_length=254, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
            ],
            options={
                'db_table': 'typefich',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Typeuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libeler', models.CharField(blank=True, max_length=254, null=True)),
                ('code', models.CharField(blank=True, max_length=254, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('ent', models.ForeignKey(db_column='Ent_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Entreprise')),
            ],
            options={
                'db_table': 'typeuser',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=254, null=True)),
                ('prenom', models.CharField(blank=True, max_length=254, null=True)),
                ('role', models.CharField(blank=True, max_length=254, null=True)),
                ('statut', models.CharField(blank=True, max_length=254, null=True)),
                ('tel', models.CharField(blank=True, max_length=254, null=True)),
                ('email', models.CharField(blank=True, max_length=254, null=True)),
                ('login', models.CharField(blank=True, max_length=254, null=True)),
                ('password', models.CharField(blank=True, max_length=254, null=True)),
                ('dates', models.DateTimeField(blank=True, null=True)),
                ('adm', models.ForeignKey(db_column='Adm_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Admin')),
                ('cic', models.ForeignKey(db_column='Cic_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Cicursale')),
                ('typ', models.ForeignKey(db_column='Typ_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typeuser')),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='traitement',
            name='use',
            field=models.ForeignKey(db_column='Use_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='resultat',
            name='tra',
            field=models.ForeignKey(blank=True, db_column='Tra_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Traitement'),
        ),
        migrations.AddField(
            model_name='perception',
            name='ids',
            field=models.ForeignKey(db_column='ids', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typecourrier'),
        ),
        migrations.AddField(
            model_name='perception',
            name='use',
            field=models.ForeignKey(db_column='Use_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='mouchard',
            name='use',
            field=models.ForeignKey(db_column='Use_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='fichierc',
            name='typ',
            field=models.ForeignKey(db_column='Typ_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typefich'),
        ),
        migrations.AddField(
            model_name='documents',
            name='dos',
            field=models.ForeignKey(db_column='Dos_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Dossiers'),
        ),
        migrations.AddField(
            model_name='documents',
            name='for_field',
            field=models.ForeignKey(db_column='For_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Format'),
        ),
        migrations.AddField(
            model_name='documents',
            name='use',
            field=models.ForeignKey(db_column='Use_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='courriers',
            name='typ',
            field=models.ForeignKey(db_column='Typ_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typecourrier'),
        ),
        migrations.AddField(
            model_name='courriers',
            name='use',
            field=models.ForeignKey(db_column='Use_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='emet', to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='courriers',
            name='use_id2',
            field=models.ForeignKey(db_column='Use_id2', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='percoit', to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='cicursale',
            name='ent',
            field=models.ForeignKey(db_column='Ent_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Entreprise'),
        ),
        migrations.AddField(
            model_name='chat',
            name='use',
            field=models.ForeignKey(db_column='Use_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='envoie', to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='chat',
            name='use_id2',
            field=models.ForeignKey(db_column='Use_id2', on_delete=django.db.models.deletion.DO_NOTHING, related_name='recoit', to='dotracks.Users'),
        ),
        migrations.AddField(
            model_name='archives',
            name='cic',
            field=models.ForeignKey(db_column='Cic_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Cicursale'),
        ),
        migrations.AddField(
            model_name='archives',
            name='dos',
            field=models.ForeignKey(db_column='Dos_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Dossiers'),
        ),
        migrations.AddField(
            model_name='archives',
            name='ran',
            field=models.ForeignKey(blank=True, db_column='Ran_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Rangement'),
        ),
        migrations.AddField(
            model_name='archives',
            name='typ',
            field=models.ForeignKey(db_column='Typ_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typearchives'),
        ),
        migrations.AddField(
            model_name='acceder',
            name='ids',
            field=models.ForeignKey(db_column='ids', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Typeuser'),
        ),
        migrations.AddField(
            model_name='acceder',
            name='mod',
            field=models.ForeignKey(db_column='Mod_id', on_delete=django.db.models.deletion.DO_NOTHING, to='dotracks.Module'),
        ),
        migrations.AlterUniqueTogether(
            name='perception',
            unique_together={('use', 'ids')},
        ),
        migrations.AlterUniqueTogether(
            name='acceder',
            unique_together={('mod', 'ids')},
        ),
    ]
