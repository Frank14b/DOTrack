from django import forms
from .models import *


class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('login', 'password')


class LoginAdmin(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('login', 'password')


class RegisterAdmin(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('login', 'password', 'email', 'dates', 'status')


class usersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('login','email', 'cic', 'typ', 'role','nom', 'prenom', 'tel')


class entrForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ('libelle', 'tel', 'slogan', 'web', 'descript',
                  'slogan', 'logo', 'status', 'dates')


class SircuForm(forms.ModelForm):
    class Meta:
        model = Cicursale
        fields = ('pays', 'ville', 'tel1', 'tel2', 'email', 'status')


class TypusersForm(forms.ModelForm):
    class Meta:
        model = Typeuser
        fields = ('libeler', 'code', 'statut')


class AccederForm(forms.ModelForm):
    class Meta:
        model = Acceder
        fields = ('ids', 'mod', 'status')


class dossierForm(forms.ModelForm):
    class Meta:
        model = Dossiers
        fields = ('cic', 'libelle', 'status', 'abreviation', 'dos', 'dates')


class docForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('for_field', 'libelle', 'descipt', 'status', 'dates')

class formatForm(forms.ModelForm):
    class Meta:
        model = Format
        fields = ('libelle', 'extension', 'status', 'ent')

class typecourrierForm(forms.ModelForm):
    class Meta:
        model = Typecourrier
        fields = ('libeler', 'abreviation', 'statut', 'ent')

class typearchivesForm(forms.ModelForm):
    class Meta:
        model = Typearchives
        fields = ('libelle', 'code', 'status', 'ent')

class moucherdForm(forms.ModelForm):
    class Meta:
        model = Mouchard
        fields = ('ip', 'tache', 'page', 'use', 'ent', 'date', 'statut', 'adm')

class chatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('use', 'use_id2', 'libelle', 'status', 'dates')