# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acceder(models.Model):
    mod = models.ForeignKey('Module', models.DO_NOTHING, db_column='Mod_id', primary_key=False)  # Field name made lowercase.
    ids = models.ForeignKey('Typeuser', models.DO_NOTHING, db_column='ids')
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'acceder'
        unique_together = (('mod', 'ids'),)


class Admin(models.Model):
    login = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'admin'


class Archives(models.Model):
    typ = models.ForeignKey('Typearchives', models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.
    cic = models.ForeignKey('Cicursale', models.DO_NOTHING, db_column='Cic_id')  # Field name made lowercase.
    ran = models.ForeignKey('Rangement', models.DO_NOTHING, db_column='Ran_id', blank=True, null=True)  # Field name made lowercase.
    dos = models.ForeignKey('Dossiers', models.DO_NOTHING, db_column='Dos_id')  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    descript = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'archives'


class Chat(models.Model):
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id', related_name="envoie")  # Field name made lowercase.
    use_id2 = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id2', related_name="recoit")  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'chat'


class Cicursale(models.Model):
    ent = models.ForeignKey('Entreprise', models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.
    pays = models.CharField(max_length=254, blank=True, null=True)
    ville = models.CharField(max_length=254, blank=True, null=True)
    tel1 = models.IntegerField(blank=True, null=True)
    tel2 = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)

    def entr(self):
        try:
            return self.ent.id
        except:
            return None
    def entrName(self):
        try:
            return self.ent.libelle
        except ValueError:
            return getattr(self, Cicursale.ent.field.attname)

    class Meta:
        managed = True
        db_table = 'cicursale'


class Courriers(models.Model):
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id', related_name="emet", null=True)  # Field name made lowercase.
    use_id2 = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id2', related_name="percoit", null=True)  # Field name made lowercase.
    typ = models.ForeignKey('Typecourrier', models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id', null=True)  # Field name made lowercase.
    intituler = models.CharField(max_length=254, blank=True, null=True)
    expediteur = models.CharField(max_length=254, blank=True, null=True)
    recepteur = models.CharField(max_length=254, blank=True, null=True)
    datee = models.DateTimeField(db_column='dateE', blank=True, null=True)  # Field name made lowercase.
    statut = models.CharField(max_length=254, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    tel = models.IntegerField(blank=True, null=True)
    dater = models.DateTimeField(db_column='dateR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'courriers'

def docDirectory():
    return '/frank/'

class Documents(models.Model):
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id')  # Field name made lowercase.
    dos = models.ForeignKey('Dossiers', models.DO_NOTHING, db_column='Dos_id')  # Field name made lowercase.
    for_field = models.ForeignKey('Format', models.DO_NOTHING, db_column='For_id')  # Field name made lowercase. Field renamed because it was a Python reserved word.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    descipt = models.CharField(max_length=254, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    dates = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'documents'


class Dossiers(models.Model):
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id')  # Field name made lowercase.
    dos = models.ForeignKey('self', models.DO_NOTHING, db_column='Dos_id', blank=True, null=True)  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    abreviation = models.CharField(max_length=254, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    dates = models.CharField(max_length=254, blank=True, null=True)

    def sucur(self):
        try:
            return self.cic.id
        except:
            return None

    def sDos(self):
        try:
            return self.dos.id
        except:
            return None
    def sDosName(self):
        try:
            return self.dos.libelle
        except ValueError:
            return getattr(self, Dossiers.dos.field.attname)

    class Meta:
        managed = True
        db_table = 'dossiers'


class Entreprise(models.Model):
    adm = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Adm_id')  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    descript = models.CharField(max_length=254, blank=True, null=True)
    slogan = models.CharField(max_length=254, blank=True, null=True)
    logo = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    web = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(db_column='dates', blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(max_length=254, blank=True, null=True)
    

    class Meta:
        managed = True
        db_table = 'entreprise'


class Fichierc(models.Model):
    typ = models.ForeignKey('Typefich', models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.
    cou = models.ForeignKey(Courriers, models.DO_NOTHING, db_column='Cou_id')  # Field name made lowercase.
    libeler = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fichierc'


class Format(models.Model):
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id', null=True)  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    extension = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'format'


class Module(models.Model):
    libele = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    modules = models.IntegerField(blank=True, null=True)
    mods = models.IntegerField(blank=True, db_column='Mod_id', null=True)

    class Meta:
        managed = True
        db_table = 'module'


class Mouchard(models.Model):
    adm = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Adm_id', null=True)  # Field name made lowercase.
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id', null=True)  # Field name made lowercase.
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id', null=True)  # Field name made lowercase.
    page = models.CharField(max_length=254, blank=True, null=True)
    ip = models.CharField(max_length=254, blank=True, null=True)
    tache = models.CharField(max_length=254, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mouchard'


class Perception(models.Model):
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id', primary_key=False)  # Field name made lowercase.
    ids = models.ForeignKey('Typecourrier', models.DO_NOTHING, db_column='ids')
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'perception'
        unique_together = (('use', 'ids'),)


class Rangement(models.Model):
    ran = models.ForeignKey('self', models.DO_NOTHING, db_column='Ran_id', blank=True, null=True)  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rangement'


class Resultat(models.Model):
    tra = models.ForeignKey('Traitement', models.DO_NOTHING, db_column='Tra_id', blank=True, null=True)  # Field name made lowercase.
    dos = models.ForeignKey(Dossiers, models.DO_NOTHING, db_column='Dos_id')  # Field name made lowercase.
    libelle = models.CharField(max_length=254, blank=True, null=True)
    fichier = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'resultat'


class Traitement(models.Model):
    doc = models.ForeignKey(Documents, models.DO_NOTHING, db_column='Doc_id')  # Field name made lowercase.
    use = models.ForeignKey('Users', models.DO_NOTHING, db_column='Use_id')  # Field name made lowercase.
    datep = models.DateTimeField(db_column='dateP', blank=True, null=True)  # Field name made lowercase.
    datet = models.DateTimeField(db_column='dateT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=254, blank=True, null=True)
    observation = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'traitement'


class Typearchives(models.Model):
    libelle = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    status = models.CharField(max_length=254, blank=True, null=True)
    ent = models.ForeignKey('Entreprise', models.DO_NOTHING, db_column='Ent_id')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'typearchives'


class Typecourrier(models.Model):
    typ = models.ForeignKey('self', models.DO_NOTHING, db_column='Typ_id', blank=True, null=True)  # Field name made lowercase.
    libeler = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    abreviation = models.CharField(max_length=254, blank=True, null=True)
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id', null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'typecourrier'


class Typefich(models.Model):
    libeler = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'typefich'


class Typeuser(models.Model):
    ent = models.ForeignKey(Entreprise, models.DO_NOTHING, db_column='Ent_id', null=True)  # Field name made lowercase.
    libeler = models.CharField(max_length=254, blank=True, null=True)
    code = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'typeuser'


class Users(models.Model):
    typ = models.ForeignKey(Typeuser, models.DO_NOTHING, db_column='Typ_id')  # Field name made lowercase.
    cic = models.ForeignKey(Cicursale, models.DO_NOTHING, db_column='Cic_id', null=True)  # Field name made lowercase.
    adm = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Adm_id', null=True)  # Field name made lowercase.
    nom = models.CharField(max_length=254, blank=True, null=True)
    prenom = models.CharField(max_length=254, blank=True, null=True)
    role = models.CharField(max_length=254, blank=True, null=True)
    statut = models.CharField(max_length=254, blank=True, null=True)
    tel = models.CharField(max_length=254, blank=True, null=True)   
    email = models.CharField(max_length=254, blank=True, null=True)
    login = models.CharField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=254, blank=True, null=True)
    dates = models.DateTimeField(blank=True, null=True)
    lastconnect = models.CharField(max_length=200, blank=True, null=True)
    totalconnect = models.IntegerField(blank=True, null=True)
    about = models.CharField(max_length=253, blank=True, null=True)
    photo = models.CharField(max_length=254, blank=True, null=True)

    def cics(self):
        try:
            return self.cic.id
        except:
            return None
    def cicName(self):
        try:
            return self.cic.ville
        except ValueError:
            return getattr(self, Users.cic.field.attname)

    class Meta:
        managed = True
        db_table = 'users'
