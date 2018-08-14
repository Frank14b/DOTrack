from django import forms
from .models import *
from PIL import Image
from django.core.files import File


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

class notifForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ('use', 'libeller', 'details', 'status', 'lien', 'other', 'dates')

class docForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('libelle', 'status', 'dates')

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

class PhotoProfilMemberForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = User_profile
        fields = ('photo', 'x', 'y', 'width', 'height', )
        widgets = {
            'photo': forms.FileInput(attrs={
                'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            })
        }

    def save(self, user):
        pic = super(PhotoProfilMemberForm, self).save(commit=False)
        pic.status = 0
        pic.use = Users.objects.get(id=user)
        pic.save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(pic.photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(pic.photo.path)

        
        return pic