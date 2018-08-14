# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acceder(models.Model):
    status = models.IntegerField(blank=True, null=True)
    ids = models.ForeignKey('Typeuser', models.DO_NOTHING, db_column='ids', blank=True, null=True)
    mod = models.ForeignKey('Module', models.DO_NOTHING, db_column='Mod_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'acceder'
        unique_together = (('mod', 'ids'),)


class Admin(models.Model):
    login = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    totalconnect = models.IntegerField(blank=True, null=True)
    lastconnect = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admin'


class Archives(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    descript = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    cic = models.ForeignKey('Cicursale', models.DO_NOTHING, db_column='Cic_id')  # Field name made lowercase.
    dos = models.ForeignKey('Dossiers', models.DO_NOTHING, db_column='Dos_id')  # Field name made lowercase.
    ran = models.ForeignKey('Rangement', models.DO_NOTHING, db_column='Ran_id', blank=True, null=True)  # Field name made lowercase.
    typ = models.ForeignKey('Typearchives', models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'archives'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Chat(models.Model):
    libelle = models.CharField(max_length=255)
    status = models.IntegerField(blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.
    use_id2 = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id2')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'chat'


class Cicursale(models.Model):
    pays = models.CharField(max_length=254, blank=True, null=True)
    ville = models.CharField(max_length=254, blank=True, null=True)
    tel1 = models.IntegerField(blank=True, null=True)
    tel2 = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    ent = models.ForeignKey('Entreprise', models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cicursale'


class Courriers(models.Model):
    intituler = models.CharField(max_length=254, blank=True, null=True)
    expediteur = models.CharField(max_length=254, blank=True, null=True)
    recepteur = models.CharField(max_length=254, blank=True, null=True)
    datee = models.DateTimeField(db_column='dateE', blank=True, null=True)  # Field name made lowercase.
    statut = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    tel = models.IntegerField(blank=True, null=True)
    dater = models.DateTimeField(db_column='dateR', blank=True, null=True)  # Field name made lowercase.
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id', blank=True, null=True)  # Field name made lowercase.
    typ = models.ForeignKey('Typecourrier', models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id', blank=True, null=True)  # Field name made lowercase.
    use_id2 = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'courriers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documents(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    descipt = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id')  # Field name made lowercase.
    dos = models.ForeignKey('Dossiers', models.DO_NOTHING, db_column='Dos_id')  # Field name made lowercase.
    for_field = models.ForeignKey('Format', models.DO_NOTHING, db_column='For_id', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.
    files = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'


class Dossiers(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    abreviation = models.CharField(max_length=254, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id')  # Field name made lowercase.
    dos = models.ForeignKey('self', models.DO_NOTHING, db_column='Dos_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dossiers'


class Entreprise(models.Model):
    libelle = models.CharField(unique=True, max_length=254, blank=True, null=True)
    descript = models.CharField(max_length=254, blank=True, null=True)
    slogan = models.CharField(max_length=254, blank=True, null=True)
    logo = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    web = models.CharField(unique=True, max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    tel = models.CharField(max_length=254, blank=True, null=True)
    adm = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Adm_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'entreprise'


class Fichierc(models.Model):
    libeler = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    cou = models.ForeignKey(Courriers, models.DO_NOTHING, db_column='Cou_id')  # Field name made lowercase.
    typ = models.ForeignKey('Typefich', models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fichierc'


class Format(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    extension = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'format'


class Module(models.Model):
    libele = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    modules = models.IntegerField(blank=True, null=True)
    mod = models.ForeignKey('self', models.DO_NOTHING, db_column='Mod_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'module'


class Mouchard(models.Model):
    page = models.CharField(max_length=254, blank=True, null=True)
    ip = models.CharField(max_length=254, blank=True, null=True)
    tache = models.CharField(max_length=254, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id', blank=True, null=True)  # Field name made lowercase.
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id', blank=True, null=True)  # Field name made lowercase.
    adm = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Adm_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mouchard'


class Notifications(models.Model):
    use_id = models.IntegerField(db_column='Use_id')  # Field name made lowercase.
    libeller = models.CharField(max_length=254)
    details = models.CharField(max_length=254, blank=True, null=True)
    lien = models.TextField()
    status = models.IntegerField()
    dates = models.DateTimeField()
    other = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Perception(models.Model):
    status = models.IntegerField(blank=True, null=True)
    ids = models.ForeignKey('Typecourrier', models.DO_NOTHING, db_column='ids')
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'perception'
        unique_together = (('use', 'ids'),)


class Rangement(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    ran = models.ForeignKey('self', models.DO_NOTHING, db_column='Ran_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rangement'


class Resultat(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    fichier = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    dos = models.ForeignKey(Dossiers, models.DO_NOTHING, db_column='Dos_id')  # Field name made lowercase.
    tra = models.ForeignKey('Traitement', models.DO_NOTHING, db_column='Tra_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resultat'


class Traitement(models.Model):
    datep = models.DateTimeField(db_column='dateP', blank=True, null=True)  # Field name made lowercase.
    datet = models.DateTimeField(db_column='dateT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=254, blank=True, null=True)
    observation = models.CharField(max_length=254, blank=True, null=True)
    doc = models.ForeignKey(Documents, models.DO_NOTHING, db_column='Doc_id')  # Field name made lowercase.
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'traitement'


class Typearchives(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'typearchives'


class Typecourrier(models.Model):
    libeler = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    typ = models.ForeignKey('self', models.DO_NOTHING, db_column='Typ_id', blank=True, null=True)  # Field name made lowercase.
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.
    abreviation = models.CharField(max_length=253)

    class Meta:
        managed = False
        db_table = 'typecourrier'


class Typefich(models.Model):
    libeler = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'typefich'


class Typeuser(models.Model):
    libeler = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'typeuser'


class UserProfile(models.Model):
    use_id = models.IntegerField(db_column='Use_id', blank=True, null=True)  # Field name made lowercase.
    photo = models.CharField(max_length=255)
    status = models.IntegerField()
    dates = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'


class Users(models.Model):
    nom = models.CharField(max_length=254, blank=True, null=True)
    prenom = models.CharField(max_length=254, blank=True, null=True)
    role = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    tel = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    login = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    adm = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Adm_id', blank=True, null=True)  # Field name made lowercase.
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id', blank=True, null=True)  # Field name made lowercase.
    typ = models.ForeignKey(Typeuser, models.DO_NOTHING, db_column='Typ_id', blank=True, null=True)  # Field name made lowercase.
    lastconnect = models.DateTimeField(blank=True, null=True)
    totalconnect = models.IntegerField(blank=True, null=True)
    about = models.CharField(max_length=253, blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
