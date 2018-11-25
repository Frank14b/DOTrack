from django.shortcuts import render
from django.contrib.staticfiles import*
from django.shortcuts import redirect, get_object_or_404
from django.db.models import manager
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import RedirectView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import uuid
import shutil
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .language import *
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import json
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Q
#from docx import Document

import mammoth
import os
import csv

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

# Create your views here.

uri = 0
d_Entr = None
d_Entrid = None

global active
active = "active"

global newLink
global pddf


def baseUrl():
    global uri
    uri = "https://demo-dotrack.herokuapp.com/"
    return uri


def sendMail(sujet, message, emailFrom, emailTo):
    send_mail(
        sujet,
        message,
        emailFrom,
        [emailTo],
        fail_silently=False,
        html_message=None,
    )

def img(request, pk):
    return render('<img src="dotracks/'+pk+'.jpg"/>')


def home(request):
    return HttpResponseRedirect("/"+defaultLang())


def TraceMouchard(request):
    if request.method == "POST":
        form = moucherdForm(request.POST)
        if form.is_valid():
            if 'd_Entrid' in request.session:
                ent = Entreprise.objects.get(id=request.session['d_Entrid'])
            else:
                ent = None
            
            if 'd_userid' in request.session:
                admin = Admin.objects.get(id=request.session['d_userid'])
            else:
                admin = None

            if 'd_memberid' in request.session:
                user = Users.objects.get(id=request.session['d_memberid'])
            else:
                user = None

            post = form.save(commit=False)
            post.date = timezone.now()
            post.use = user
            post.ent = ent
            post.adm = admin
            post.statut = 0
            post.ip = get_client_ip(request)
            post.save()
            rp = 0
        else:
            rp = 'echec'
    return HttpResponse(rp)

def addNotif(request):
    
    if request.method == "POST":
        form = notifForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.dates = timezone.now()
            post.use = Users.objects.get(id=request.POST['use'])
            post.libeller = request.POST['libeller']
            post.details = request.POST['details']
            post.status = 0
            post.lien = request.POST['lien']
            post.other = request.POST['other']
            post.save()
            rp = 0
        else:
            rp = 'echec'
    return HttpResponse(rp)

def nnadminLang(request):
    return HttpResponseRedirect(baseUrl()+"connexion/"+defaultLang())

def acceuil(request, lang):
    if "d_user" in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        request.session['tacheMouchard'] = "Acces Acceuil DOTrack"

        return render(request, 'dotracks/index.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})

def addNbrConnexionAdmin(idA, actuel, request):
    if request.method == "POST":
        try:
            nbr = Admin.objects.get(id=idA)
            nbr.totalconnect = sum((actuel, 1),0)
            nbr.lastconnect = timezone.now()
            nbr.save()
            data = True
        except ObjectDoesNotExist:
            data = False
        return HttpResponse(data)

def Loginadmin(request, lang):
    if "d_user" in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        if request.method == "POST":
            try:
                dotrack = Admin.objects.filter(email=request.POST['email'])[0]
            except ObjectDoesNotExist:
                dotrack = None
            if dotrack != None:
                if check_password(request.POST['password'], dotrack.password):
                    if "d_memberid" in request.session:
                        try:
                            del request.session["d_memberid"]
                            del request.session["d_member"]
                        except ObjectDoesNotExist:
                            answ =  None

                    request.session['d_userid'] = dotrack.id
                    request.session['d_user'] = dotrack.login

                    #addNbrConnexionAdmin(dotrack.id, dotrack.totalconnect, request)

                    # return HttpResponseRedirect("/connexion/")
                    request.session['tacheMouchard'] = "DOTrack Connexion Administrateur "+request.session['d_user']
                    return HttpResponse('0')
                else:
                    # return HttpResponseRedirect("/connexion/")
                    request.session['tacheMouchard'] = "Mot de passe | incorrect Connexion Administrateur "+request.POST['email']
                    return HttpResponse('Mot de passe incorrect veuillez reesayer !')
            else:
                return HttpResponse('Email ou Pass incorrect veuillez reesayer !')
        else:
            # form = UserForm()
            return render(request, 'dotracks/Login.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})


def About(request, lang):
    if "d_user" in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        request.session['tacheMouchard'] = "Acces Apropos DOTrack"

        return render(request, 'dotracks/about.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})

def CourrierUs(request, lang):
    if "d_user" in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        request.session['tacheMouchard'] = "Acces Espace Courrier DOTrack"

        return render(request, 'dotracks/courrier.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})

def memberCourrier(request, lang):
    if "d_member" in request.session:
        id = request.session['d_memberid']

        if checkMyAccess(2, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        request.session['tacheMouchard'] = "Acces Espace Courrier DOTrack"

        return render(request, 'dotracks/dashboard/courrier.html', {"userInfo": get_Userby_id(id), 'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))
        

def FindEntr(request):
    if 'd_user' in request.session:
        return HttpResponseRedirect("/")
    else:
        if request.method == "POST":
            try:
                res = Cicursale.objects.filter(Q(email__contains=request.POST['email'])).values('id','pays','ville','email')
                if res.count() != 0:
                    dat = list(res)
                else:
                    dat = 0
            except ObjectDoesNotExist:
                dat = 0
            return JsonResponse(dat, safe=False)

def LoginFacebook(request):
    if 'd_user' in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        if request.method == "POST":
            try:
                dotrack = Admin.objects.filter(email=request.POST['email'])[0]
            except ObjectDoesNotExist:
                dotrack = None
            if dotrack == None:
                form = RegisterAdmin(request.POST)
                uform = usersForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.dates = timezone.now()
                    post.status = "0"
                    #post.password = make_password(request.POST['password'])
                    post.save()
                    # 
                    # Mailmess = "Merci d'avoir souscrit a DoTrack veuillez activer votre compte en suivant ce lien:"
                    # """sendMail("Account_Validation", Mailmess,
                    # "franckfontcha@gmail.com", post.email)"""    
                    #request.session['tacheMouchard'] = "Nouvelle Inscription Administrateur "+request.POST['email']
                    
                    if "d_memberid" in request.session:
                        try:
                            del request.session["d_memberid"]
                            del request.session["d_member"]
                        except ObjectDoesNotExist:
                            answ =  None

                    dotrack2 = Admin.objects.filter(email=request.POST['email'])[0]

                    request.session['d_userid'] = dotrack2.id
                    request.session['d_user'] = dotrack2.login

                    # return HttpResponseRedirect("/connexion/")
                    request.session['tacheMouchard'] = "DOTrack Connexion Administrateur "+request.session['d_user']
                    return HttpResponse('0')

                else:
                    return HttpResponse('echec')
            else:
                if "d_memberid" in request.session:
                    try:
                        del request.session["d_memberid"]
                        del request.session["d_member"]
                    except ObjectDoesNotExist:
                        answ =  None

                request.session['d_userid'] = dotrack.id
                request.session['d_user'] = dotrack.login

                # return HttpResponseRedirect("/connexion/")
                request.session['tacheMouchard'] = "DOTrack Connexion Administrateur "+request.session['d_user']
                return HttpResponse('0')
        else:
            return render(request, 'dotracks/register.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "reponseActive": "none"})


def Register(request, lang):
    if 'd_user' in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        if request.method == "POST":
            form = RegisterAdmin(request.POST)
            uform = usersForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.dates = timezone.now()
                post.status = "0"
                post.password = make_password(request.POST['password'])
                post.save()

                Mailmess = "Merci d'avoir souscrit a DoTrack veuillez activer votre compte en suivant ce lien:"
                """sendMail("Account_Validation", Mailmess,
                         "franckfontcha@gmail.com", post.email)"""

                request.session['tacheMouchard'] = "Nouvelle Inscription Administrateur "+request.POST['email']

                return HttpResponse('0')

            else:
                return HttpResponse('echec')
        else:
            return render(request, 'dotracks/register.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "reponseActive": "none"})


def ContactUs(request, lang):
    if "d_user" in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        request.session['tacheMouchard'] = "Acces Espace Contacts"

        return render(request, 'dotracks/contact.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})

def CourrierSend(request, lang, pk):
    if "d_user" in request.session:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
    else:
        request.session['tacheMouchard'] = "Acces Espace Envoi du Courrier"

        return render(request, 'dotracks/sendMail.html', {'active': active, 'send':pk, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})

def Logout(request, lang):
    try:
        if "d_memberid" in request.session:
            try:
                del request.session["d_memberid"]
                del request.session["d_member"]
            except ObjectDoesNotExist:
                answ =  None

        del request.session['d_userid']
        del request.session['d_user']
        request.session['tacheMouchard'] = "Nouvelle Deconnexion Administrateur "+request.session['d_user']
        return HttpResponseRedirect("/connexion/"+checkLangAbbr(lang))
    except KeyError:
        return HttpResponseRedirect("/connexion/"+checkLangAbbr(lang))


def adminIndex(request, lang):
    if "d_user" in request.session:
        id = request.session["d_userid"]
        if "d_Entrid" in request.session:
            idEnt = request.session["d_Entrid"]

            if get_Entr_by_id(idEnt, id) == None:
                return HttpResponseRedirect(baseUrl()+'dashboard/company/logout/'+checkLangAbbr(lang))
        else:
            idEnt = 0
            request.session['tacheMouchard'] = "Espace Acceuil Administrateur "+request.session['d_user']

        return render(request, 'dotracks/dashboard/index.html', { "allMouchard": getAdminMouchard(id), "nbrUser": get_nbrUser_by_Entr(idEnt), 'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrEntr": get_nbrEntr_by_me(id), "listentr": get_Entr_by_me(id), "nbrCicr": get_nbrCic_by_me(idEnt), "listsircur": get_Cic_by_ent(idEnt), "nbrTypUser": get_nbrTypUser_by_Entr(idEnt), "typuserlist": get_TypUser_by_Entr(idEnt), "userList": get_User_by_Entr_limit(idEnt), "preg": pregUser(get_nbrUser_by_Entr(idEnt))})
    else:
        return HttpResponseRedirect(baseUrl()+"/connexion/"+checkLangAbbr(lang))

def courrier(request, lang):
    if "d_Entr" in request.session:
        id = request.session["d_userid"]
        if "d_Entrid" in request.session:
            idEnt = request.session["d_Entrid"]

            if get_Entr_by_id(idEnt, id) == None:
                return HttpResponseRedirect(baseUrl()+'dashboard/company/logout/'+checkLangAbbr(lang))
        else:
            idEnt = 0
            request.session['tacheMouchard'] = "Espace Courrier Entreprise "+request.session['d_Entr']

        return render(request, 'dotracks/dashboard/admin/mail.html', {"nbrUser": get_nbrUser_by_Entr(idEnt), 'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrEntr": get_nbrEntr_by_me(id), "listentr": get_Entr_by_me(id), "allCourrier":getCourrierByEnt(idEnt)})
    else:
        return HttpResponseRedirect(baseUrl()+checkLangAbbr(lang))

def courriers(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]
        idEnt = 0
        request.session['tacheMouchard'] = "Espace Courrier Entreprise "+request.session['d_member']

        return render(request, 'dotracks/dashboard/mail.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang),"userInfo": get_Userby_id(id),"allCourrier":getCourrierByUser(id)})
    else:
        return HttpResponseRedirect(baseUrl()+checkLangAbbr(lang))

def post_addEntr(request):
    if 'd_user' in request.session:
        if request.method == "POST":
            form = entrForm(request.POST)
            if form.is_valid():

                if not os.path.exists('dotracks/entreprises/'+request.POST["libelle"]):
                    os.makedirs('dotracks/entreprises/'+request.POST["libelle"])

                    post = form.save(commit=False)
                    post.dates = timezone.now()
                    post.status = 0
                    post.adm = Admin.objects.get(
                        id=request.session["d_userid"])
                    post.save()
                    return HttpResponse('0')
                else:
                    return HttpResponse('Echec Entreprise existante veuillez modifier le nom')

            else:
                return HttpResponse('Echec denregistrement : Erreur des champs')
    else:
        return HttpResponseRedirect("/")


def post_addSucur(request):
    if 'd_Entr' in request.session:
        if request.method == "POST":
            form = SircuForm(request.POST)
            if form.is_valid():

                libeleEnt = get_Entr_by_id(
                    request.session["d_Entrid"], request.session["d_userid"])

                if not os.path.exists('dotracks/entreprises/'+libeleEnt.libelle+'/'+request.POST["ville"]+'_'+request.POST["pays"]):
                    os.makedirs('dotracks/entreprises/'+libeleEnt.libelle +
                                '/'+request.POST["ville"]+'_'+request.POST["pays"])

                    post = form.save(commit=False)
                    post.status = 0
                    post.ent = Entreprise.objects.get(
                        id=request.session["d_Entrid"])
                    post.save()
                    return HttpResponse('0')
                else:
                    return HttpResponse('Echec Sucursale existante veuillez Modifier')
            else:
                return HttpResponse('Echec denregistrement : Erreur des champs')
    else:
        return HttpResponseRedirect("/")


def addTypeuse(request):
    if 'd_Entr' in request.session:
        if request.method == "POST":
            form = TypusersForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.statut = 0
                post.ent = Entreprise.objects.get(
                    id=request.session["d_Entrid"])
                post.save()
                return HttpResponse('0')

            else:
                return HttpResponse('Echec denregistrement : Erreur des champs')
    else:
        return HttpResponseRedirect("/")


def addUse(request):
    if request.method == "POST":
        form = usersForm(request.POST)
        if form.is_valid():
            data = Users.objects.filter(
                Q(login=request.POST['login']) | Q(email=request.POST['email']))
            if(data.count() == 0):
                post = form.save(commit=False)
                post.statut = 0
                post.photo = 0
                post.totalconnect = 0
                post.dates = timezone.now()
                post.password = make_password(request.POST['login'])
                post.save()
                return HttpResponse('0')
            else:
                return HttpResponse('Echec Login ou Email existant veuillez le modifier')
        else:
            return HttpResponse('Echec d\'enregistrement : Erreur des champs')


def chargerNotification(request):
    try:
        id = request.session['d_memberid']
        notif = Notifications.objects.filter(use=id).order_by('-id').values("id", "libeller", "lien", "details","dates","status").exclude(status="1")
        if notif.count() != 0:
            rs = list(notif)
        else:
            rs = 1
    except ObjectDoesNotExist:
            rs = 'erreur not mach'
    return JsonResponse(rs, safe=False)

def conterNotification(request):
    try:
        id = request.session['d_memberid']
        notif = Notifications.objects.filter(use=id, status=0).count()
    except ObjectDoesNotExist:
        notif = ''
    return HttpResponse(notif)

def get_nbrEntr_by_me(id):
    nbr = Entreprise.objects.filter(
        adm=id).exclude(status="@alphaLock").count()
    return nbr


def get_Entr_by_me(id):
    try:
        entr = Entreprise.objects.filter(adm=id).exclude(status="@alphaLock")
    except ObjectDoesNotExist:
        entr = None
    return entr

def getCourrierByEnt(id):
    try:
        cour = Courriers.objects.get(cic__ent=id)
    except ObjectDoesNotExist:
        cour = None
    return cour

def getCourrierByUser(id):
    try:
        cour = Courriers.objects.get(Q(use_id=id) | Q(use_id2=id))
    except ObjectDoesNotExist:
        cour = None
    return cour

def get_Entr_by_id(id, user):
    try:
        entr = Entreprise.objects.get(adm=user, id=id)
    except ObjectDoesNotExist:
        entr = None
    return entr


def get_nbrCic_by_me(id):
    nbr = Cicursale.objects.filter(ent=id).exclude(status="@alphaLock").count()
    return nbr


def get_Cic_by_ent(id):
    Cicr = Cicursale.objects.filter(ent=id).exclude(status="@alphaLock")
    return Cicr


def get_nbrTypUser_by_Entr(id):
    try:
        typeUse = Typeuser.objects.filter(
            ent=id).exclude(statut="@alphaLock").count()
    except ObjectDoesNotExist:
        typeUse = None
    return typeUse


def get_nbrUser_by_Entr(id):
    try:
        typeUse = Users.objects.filter(cic__ent=id).exclude(
            statut="@alphaLock").count()
    except ObjectDoesNotExist:
        typeUse = None
    return typeUse


def get_TypUser_by_Entr(id):
    try:
        typeUse = Typeuser.objects.filter(ent=id).exclude(statut="@alphaLock")
    except ObjectDoesNotExist:
        typeUse = None
    return typeUse


def get_User_by_cic(id, myID):
    try:
        typeUse = Users.objects.filter(cic=id, statut=0).values(
            'id', 'nom', 'prenom', 'typ__libeler', 'role', 'statut', 'cic__ville', 'cic__pays', 'photo').exclude(id=myID)
    except ObjectDoesNotExist:
        typeUse = None
    return typeUse


def get_User_by_Entr(id):
    try:
        typeUse = Users.objects.filter(cic__ent=id).values(
            'id', 'nom', 'prenom', 'typ__libeler', 'role', 'statut', 'cic__ville', 'cic__pays', 'photo').exclude(statut="@alphaLock")
    except ObjectDoesNotExist:
        typeUse = None
    return typeUse


def get_User_by_Entr_limit(id):
    try:
        typeUse = Users.objects.filter(cic__ent=id).order_by('-id').exclude(statut="@alphaLock")[0:8].values(
            'id', 'nom', 'prenom', 'typ__libeler', 'role', 'statut', 'cic__ville', 'cic__pays', 'photo')
    except ObjectDoesNotExist:
        typeUse = None
    return typeUse


def checkAdminMembership(id, userid):
    try:
        member = Users.objects.filter(
            cic=id, adm__id=userid).exclude(statut="@alphaLock")
        if member.count() != 0:
            mem = member
        else:
            mem = None
    except ObjectDoesNotExist:
        mem = None
    return mem


def accesSucur(request, lang, pk):
    userid = request.session['d_userid']

    if checkAdminMembership(pk, userid) != None:
        try:
            member = Users.objects.filter(
                cic=pk, adm__id=userid, statut=0).exclude(statut="@alphaLock")[0]
            request.session["d_memberid"] = member.id
            request.session["d_member"] = member.login
            request.session["dmemberid"] = member.id

            request.session['tacheMouchard'] = "Synchronisation Administrateur au compte Member "

            return HttpResponseRedirect("/dashboard/Member/"+checkLangAbbr(lang))
        except ObjectDoesNotExist:
    
            return HttpResponseRedirect("/dashboard/admin/error/"+checkLangAbbr(lang))
    else:
        return HttpResponseRedirect("/dashboard/admin/error/"+checkLangAbbr(lang))


def adminError(request, lang):
    id = request.session["d_userid"]
    idEnt = request.session["d_Entrid"]
    request.session['tacheMouchard'] = "Tentative de synchronisation Administrateur au compte Member"

    return render(request, 'dotracks/dashboard/index.html', {"allMouchard": getAdminMouchard(id), "errorSucuLog": "error", "nbrUser": get_nbrUser_by_Entr(idEnt), 'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrEntr": get_nbrEntr_by_me(id), "listentr": get_Entr_by_me(id), "nbrCicr": get_nbrCic_by_me(idEnt), "listsircur": get_Cic_by_ent(idEnt), "nbrTypUser": get_nbrTypUser_by_Entr(idEnt), "typuserlist": get_TypUser_by_Entr(idEnt), "userList": get_User_by_Entr_limit(idEnt), "preg": pregUser(get_nbrUser_by_Entr(idEnt))})


def pregUser(user):
    if user == 0:
        return "12345678"
    if user == 1:
        return "1234567"
    if user == 2:
        return "123456"
    if user == 3:
        return "12345"
    if user == 4:
        return "1234"
    if user == 5:
        return "123"
    if user == 6:
        return "12"
    if user == 7:
        return "7"
    if user == 8:
        return "1"


def startEntr(request, lang, pk):
    try:
        check = Entreprise.objects.get(id=pk, adm=request.session["d_userid"])
    except ObjectDoesNotExist:
        check = None
    if check != None:
        request.session['d_Entrid'] = check.id
        request.session['d_Entr'] = check.libelle

        request.session['tacheMouchard'] = "Nouvelle Connexion Entreprise "+request.session['d_Entr']

    return HttpResponseRedirect(baseUrl()+'dashboard/admin/'+checkLangAbbr(lang))


def LogoutEntr(request, lang):
    try:
        del request.session['d_Entrid']
        del request.session['d_Entr']

        request.session['tacheMouchard'] = "Nouvelle Deconnexion Entreprise "+request.session['d_Entr']

        return HttpResponseRedirect(baseUrl()+'dashboard/admin/'+checkLangAbbr(lang))
    except KeyError:
        return HttpResponseRedirect(baseUrl()+'dashboard/admin/'+checkLangAbbr(lang))


def allEntr(request, lang):
    if 'd_user' in request.session:
        id = request.session["d_userid"]
        if "d_Entrid" in request.session:

            idEnt = request.session["d_Entrid"]

            if get_Entr_by_id(idEnt, id) == None:
                return HttpResponseRedirect(baseUrl()+'dashboard/company/logout/'+checkLangAbbr(lang))
        else:
            idEnt = 0
        ent = Entreprise.objects.filter(
            adm=request.session["d_userid"]).exclude(status="@alphaLock")
        paginator = Paginator((list(ent)), 10)
        page = request.GET.get('Page')
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        request.session['tacheMouchard'] = "Espace Consultation Enteprises"

        return render(request, 'dotracks/dashboard/admin/Ent_setting.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrUser": get_nbrUser_by_Entr(idEnt), "nbrEntr": get_nbrEntr_by_me(id), "listentr": result, "nbrCicr": get_nbrCic_by_me(idEnt), "listsircur": get_Cic_by_ent(idEnt)})


def sucurUsers(request, pk, lang):
    if 'd_user' in request.session:
        id = request.session["d_userid"]

        if "d_Entrid" in request.session:

            idEnt = request.session["d_Entrid"]

            if get_Entr_by_id(idEnt, id) == None:
                return HttpResponseRedirect(baseUrl()+'dashboard/company/logout/'+checkLangAbbr(lang))
        else:
            idEnt = 0

        use = Users.objects.filter(cic=pk)

        request.session['tacheMouchard'] = "Liste Utilisateurs Sucursale Entreprise "+request.session['d_Entr']

        return render(request, 'dotracks/dashboard/admin/listUsers.html', {"synchro": checkSynchroMemberAdmin(pk, id), "listentr": get_Entr_by_me(id), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrEntr": get_nbrEntr_by_me(id), "listuser": use, "nbrCicr": get_nbrCic_by_me(idEnt), "listsircur": get_Cic_by_ent(idEnt), "nbrTypUser": get_nbrTypUser_by_Entr(idEnt), "typuserlist": get_TypUser_by_Entr(idEnt)})


def checkSynchroMemberAdmin(pk, id):
    try:
        member = Users.objects.get(cic=pk, adm=id)
    except ObjectDoesNotExist:
        member = None
    return member


def synchroMemberAdmin(request):
    if request.method == "POST":
        try:
            Users.objects.filter(id=request.POST['id']).update(
                adm=request.session['d_userid'], login=None)
            return HttpResponseRedirect('0')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('erreur not mach')


def droitTypeusers(request):
    if request.method == "POST":
        try:
            v = Acceder.objects.filter(ids=request.POST['id']).values(
                "mod__id", "mod__libele", "id")
            if v.count() != 0:
                rs = list(v)
            else:
                rs = 1
        except ObjectDoesNotExist:
            rs = 'erreur not mach'
        return JsonResponse(rs, safe=False)
        # return HttpResponse(rs)


def droitTypeusersMenus(request):
    if request.method == "POST":
        try:
            v = Module.objects.filter(mods=request.POST['id']).values("id", "libele")
            if v.count() != 0:
                rs = list(v)
            else:
                rs = 1
        except ObjectDoesNotExist:
            rs = 'erreur not mach'
        return JsonResponse(rs, safe=False)
        # return HttpResponse(rs)


def removedroitTypeusers(request):
    req = request

    if request.method == "POST":
        try:
            v = Acceder.objects.filter(id=request.POST['ida'])
            v.delete()
            rs = 0
        except ObjectDoesNotExist:
            rs = 'erreur not mach'
        # return JsonResponse(rs, safe=False)
        return HttpResponse(rs)


def senddroitTypeusers(request):
    if 'd_user' in request.session:
        if request.method == "POST":
            try:
                # nbr = request.POST['nmbre']
                form = AccederForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.status = 0
                    post.ids = Typeuser.objects.get(id=request.POST['ids'])
                    post.mod = Module.objects.get(id=request.POST['mod'])
                    post.save()
                    rp = 0
                else:
                    rp = "Echec lors de lenregistrement !"
            except:
                rp = 'Erreur not mach'
            return HttpResponse(rp)


def allEntrUsers(request, lang):
    if 'd_user' in request.session:
        id = request.session["d_userid"]

        if "d_Entrid" in request.session:

            idEnt = request.session["d_Entrid"]

            if get_Entr_by_id(idEnt, id) == None:
                return HttpResponseRedirect(baseUrl()+'dashboard/company/logout/'+checkLangAbbr(lang))
        else:
            idEnt = 0
        use = Users.objects.filter(cic=idEnt)

        return render(request, 'dotracks/dashboard/admin/allEntrUsers.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrEntr": get_nbrEntr_by_me(id), "listentr": use, "nbrCicr": get_nbrCic_by_me(idEnt), "listsircur": get_Cic_by_ent(idEnt), "nbrTypUser": get_nbrTypUser_by_Entr(idEnt), "typuserlist": get_TypUser_by_Entr(idEnt), "userList": get_User_by_Entr(idEnt)})


def administrate(request, lang):
    if "d_Entrid" in request.session:
        id = request.session["d_userid"]
        idEnt = request.session["d_Entrid"]

        request.session['tacheMouchard'] = "Espace Configuration Administrateur"

        #TraceMouchard(id, idEnt, 'administrate parametre')

        return render(request, 'dotracks/dashboard/admin/settings.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "typuserlist": get_TypUser_by_Entr(idEnt), "modules": getModules(), "listentr": get_Entr_by_me(id), "listsircur": get_Cic_by_ent(idEnt), "allFormat": getFormatFichiers(idEnt), "allTypeCourrier": getTypeCourriers(idEnt), "allTypeArchives": getTypeArchives(idEnt)})
    else:
        return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))


def get_EntByID(request):
    if request.method == "POST":
        try:
            liste = Entreprise.objects.filter(id=request.POST['id']).values(
                'libelle', 'descript', 'slogan', 'web', 'tel')
            if liste.count() != 0:
                data = list(liste)
            else:
                data = 1
        except ObjectDoesNotExist:
            data = None
        return JsonResponse(data, safe=False)


def deleteEntreprise(request):
    if request.method == "POST":
        try:
            liste = Entreprise.objects.get(id=request.POST['id'])
            liste.status = "@alphaLock"
            liste.save()
            data = True
        except ObjectDoesNotExist:
            data = False
        return HttpResponse(data)

#================================================= Member =====================================================#


def adminMember(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]
        use = request.session["d_member"]

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        request.session['tacheMouchard'] = "Nouvelle Connexion Membre "

        return render(request, 'dotracks/dashboard/starter.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent), "userList": get_User_by_cic(sucur, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"/connexionMember/"+checkLangAbbr(lang))


def LoginMember2(request):
    request.session['tacheMouchard'] = "Espace Formulaire Connexion Membre"
    return HttpResponseRedirect(baseUrl()+"member/login/"+defaultLang())

def addNbrConnexionMember(idA, actuel, request):
    if request.method == "POST":
        try:
            nbr = Users.objects.get(id=idA)
            nbr.totalconnect = sum((actuel, 1),0)
            nbr.lastconnect = timezone.now()
            nbr.save()
            data = True
        except ObjectDoesNotExist:
            data = False
        return HttpResponse(data)

def LoginMember(request, lang):
    if "d_member" in request.session:
        return HttpResponseRedirect(baseUrl()+"dashboard/Member/"+checkLangAbbr(lang))
    else:
        if request.method == "POST":
            try:
                dotrack = Users.objects.get(login=request.POST['login'])
            except ObjectDoesNotExist:
                dotrack = None
            if dotrack != None:
                
                if check_password(request.POST['password'], dotrack.password):
                    request.session['d_memberid'] = dotrack.id
                    request.session['d_member'] = dotrack.login
                    # return HttpResponseRedirect("/connexion/")

                    addNbrConnexionMember(dotrack.id, dotrack.totalconnect, request)

                    return HttpResponse('0')
                else:
                    # return HttpResponseRedirect("/connexion/")
                    return HttpResponse('Mot de passe incorrect veuillez reesayer !')
            else:
                return HttpResponse('Login ou Pass incorrect veuillez reesayer !')
        else:
            # form = UserForm()
            return render(request, 'dotracks/dashboard/Login.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang)})


def LogoutMember(request, lang):
    try:
        del request.session['d_memberid']
        del request.session['d_member']
        if "d_user" in request.session:
            return HttpResponseRedirect("/dashboard/admin/"+checkLangAbbr(lang))
        else:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))
    except KeyError:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def get_Userby_id(id):
    try:
        use = Users.objects.filter(id=id).values(
            'id', 'nom', 'prenom', 'typ__libeler', 'role', 'statut', 'cic__ville', 'cic__pays', "cic", 'login', 'email', 'tel', 'typ', 'typ__libeler', 'typ__code', 'lastconnect', 'totalconnect', 'about', 'dates', 'photo')[0]
    except ObjectDoesNotExist:
        use = None
    return use


def forgotPassMember(request):
    if request.method == "POST":
        try:
            dotrack = Users.objects.get(email=request.POST['email'])
        except ObjectDoesNotExist:
            dotrack = None
        if dotrack != None:
            try:
                status = make_password(timezone.now())
                Users.objects.filter(
                    email=request.POST['email']).update(statut=status)
                dot = "ok"
            except ObjectDoesNotExist:
                dot = "no"
            if dot != "no":
                try:
                    sujet = "Recuperation Mot de Passe"
                    message = "suivez le lien ci-apres pour reinitialiser votre mot de passe<br><a href='" + \
                        baseUrl()+"/member/resetPass/"+defaultLang()+"'>Reset Password</button></a>"
                    expe = ""
                    recep = request.POST['email']
                    send_mail(sujet, message, expe, recep)
                    return HttpResponseRedirect(0)
                except:
                    return HttpResponseRedirect("Echec d'envoi du mail veuillez reessayer !")
            else:
                return HttpResponseRedirect("Echec lors de la generation du code veuillez reesayer !")

        else:
            return HttpResponseRedirect('Compte inexistant veuillez creer un compte !')


def Profile(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]
        #request.session['tacheMouchard'] = "Espace Profil Membre "+request.session["d_member"]

        return render(request, 'dotracks/dashboard/Profile.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "profilePic":getMemberPicture(id), "allMouchard":getMemberMouchard(id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def profileUserEntr(request, lang, pk):
    if "d_user" in request.session:
        id = pk
        ident = request.session["d_userid"]
        return render(request, 'dotracks/dashboard/admin/Profile.html', {'active': active, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "nbrEntr": get_nbrEntr_by_me(ident), "listentr": get_Entr_by_me(ident), "userInfo": get_Userby_id(id)})
    else:
        return HttpResponseRedirect(baseUrl()+checkLangAbbr(lang))


def ProfileAdmin(request, lang):
    if "d_user" in request.session:
        id = request.session["d_userid"]
        return render(request, 'dotracks/dashboard/admin/Profile.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id)})
    else:
        return HttpResponseRedirect(baseUrl()+checkLangAbbr(lang))


def getMyAccess(request):
    try:
        iduser = request.session["d_memberid"]
        b = Users.objects.filter(id=iduser)[0].typ
        v = Acceder.objects.filter(ids=b, mod=request.POST['id'])
        if v.count() != 0:
            rs = 0
        else:
            rs = 1
    except ObjectDoesNotExist:
        rs = 1
    return HttpResponse(rs)

def checkMyAccess(idpage, id):
    try:
        iduser = id
        b = Users.objects.filter(id=iduser)[0].typ
        v = Acceder.objects.get(ids=b, mod=idpage)
        rs = 0
    except ObjectDoesNotExist:
        rs = 1
    return rs


def Memberusers(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(9, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/MemberUsers.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "userList": get_User_by_cic(idCic, id), "nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def MemberMessagerie(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(3, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        return render(request, 'dotracks/dashboard/MemberChat.html', {'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def MemberMessagerie2(request, lang, pk):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(3, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic
        a, b = pk.split('user')

        mess = Chat.objects.filter(Q(use_id2=b), Q(use=id) | Q(use_id2=id), Q(
            use=b)).values('id', 'use', 'use_id2', 'libelle', 'dates')
        if(mess.count() != 0):
            chat = mess
        else:
            chat = 0

        return render(request, 'dotracks/dashboard/MemberChat.html', {'userID':b, 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "userList": get_User_by_cic(idCic, id), "chat": chat})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def recuperationChat(request):
    if "d_member" in request.session:
        if request.method == "POST":
            id = request.session["d_memberid"]
            b = request.POST['use2']
            mess = Chat.objects.filter(Q(use_id2=b) | Q(use_id2=id), Q(use=id) | Q(use=b)).values('id', 'use', 'use_id2', 'libelle', 'dates','use__nom', 'use_id2__nom','use__photo','use_id2__photo', 'use__prenom', 'use_id2__prenom', 'status').order_by('-id')
            if(mess.count() != 0):
                chat = list(mess)
            else:
                chat = 0

            return JsonResponse(chat, safe=False)

def messageLus(request):
    if 'd_member' in request.session:
        if request.method == "POST":
            try:
                post = Chat.objects.get(id=request.POST['id'])
                post.status = 1
                post.save()
                rp = 0
                return HttpResponse(rp)
            except:
                rp = 'Erreur not mach'
                return HttpResponse(rp)

def vuNotification(request):
    if 'd_member' in request.session:
        if request.method == "POST":
            try:
                post = Notifications.objects.get(id=request.POST['id'])
                post.status = 2
                post.save()
                rp = 0
                return HttpResponse(rp)
            except:
                rp = 'Erreur not mach'
                return HttpResponse(rp)

def EnvoiDuChat(request):
    if 'd_member' in request.session:
        if request.method == "POST":
            try:
                # nbr = request.POST['nmbre']
                form = chatForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.status = 0
                    post.use = Users.objects.get(id=request.session["d_memberid"])
                    post.dates = timezone.now()
                    post.save()
                    rp = 0
                else:
                    rp = "Echec lors de l'envoi du message reéssayer plutard !"
            except:
                rp = 'Erreur not mach'
            return HttpResponse(rp)

def getSearchChat(request):
    if "d_member" in request.session:

        if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

        id = request.session["d_memberid"]
        try:
            idsurcu = Users.objects.get(id=id).cic
            q = request.POST['q']
            v = Users.objects.filter(Q(nom__contains=q) | Q(
                prenom__contains=q)).values('nom', 'prenom', 'id')
            if v.count() != 0:
                use = list(v)
            else:
                use = 0
        except ObjectDoesNotExist:
            use = 0
        return JsonResponse(use, safe=False)


def addDossier(request):
    if 'd_member' in request.session:

        if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

        if request.method == "POST":

            newLink = 0

            form = dossierForm(request.POST)
            if form.is_valid():
                Sucur = Cicursale.objects.filter(id=request.POST['cic'])[0]
                entr = Sucur.entrName()
                post = form.save(commit=False)
                if not request.POST['dos']:
                    if not os.path.exists('dotracks/static/dotracks/entreprises/'+entr+'/'+Sucur.ville+'_'+Sucur.pays+'/'+request.POST['libelle']):
                        os.makedirs('dotracks/static/dotracks/entreprises/'+entr+'/'+Sucur.ville +
                                    '_'+Sucur.pays+'/'+request.POST['libelle'])
                        
                        newLink = 'static/dotracks/entreprises/'+entr+'/'+Sucur.ville +'_'+Sucur.pays+'/'+request.POST['libelle']
                else:
                    libDos = Dossiers.objects.get(
                        id=request.POST['dos']).link
                    if not os.path.exists('dotracks/'+libDos+'/'+request.POST['libelle']):
                        os.makedirs('dotracks/'+libDos+'/'+request.POST['libelle'])

                        newLink = libDos+'/'+request.POST['libelle']

                post.status = 0
                post.link = newLink
                post.dates = timezone.now()
                post.cic = Cicursale.objects.get(id=request.POST['cic'])
                if request.POST['dos']:
                    post.dos = Dossiers.objects.get(id=request.POST['dos'])
                post.save()
                return HttpResponse('0')
            else:
                return HttpResponse('Echec de creation du dossier ! Dossier existant')
        else:
            return HttpResponse('Echec denregistrement : Erreur des champs')
    else:
        return HttpResponseRedirect("/")


def DossierMember(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(15, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/Dossiers.html', {"nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierList": getDossierBySuc(idCic), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def Document(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(4, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/Documents.html', {"myDocument": getDocuments(sucu), "nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierList": getDossierBySuc(idCic), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def DocumentOpen(request, lang, pk):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(4, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/Documents.html', {"openDcument":getDocumentsDetails(pk), "myDocument": getDocuments(sucu), "nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierList": getDossierBySuc(idCic), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def DocumentOperation(request, lang, pk, ob):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(4, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())
        if(ob == "edit"):
            return render(request, 'dotracks/dashboard/Documents.html', {"editDocument":getDocumentsDetails(pk), "myDocument": getDocuments(sucu), "nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierList": getDossierBySuc(idCic), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def openDossier(request, lang, pk):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(15, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/openDossiers.html', {"nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierInfo": getDossierInfos(pk), "predossierInfo": getPreDossierInfos(pk), "sdossierList": getsDossierBySuc(pk), "docList": getDocumentsBySuc(pk), "docListfile":getDocumentFilesBySuc(pk), "docListDOC":getDocumentBySuc(pk), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def addDocuments(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(4, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/ajouterDocuments.html', {"nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent),'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierList": getDossierBySuc(idCic), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def configSuccursale(request, lang):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(18, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

        idCic = Users.objects.get(id=id).cic

        sucu = Users.objects.get(id=id)
        sucur = Cicursale.objects.get(id=sucu.cics())
        ent = Entreprise.objects.get(id=sucur.entr())

        return render(request, 'dotracks/dashboard/configuration.html', {"nbruser": getNbrUserBySuc(id), "typuserlist": get_TypUser_by_Entr(ent),'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "dossierList": getDossierBySuc(idCic), "userList": get_User_by_cic(idCic, id)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))


def addImageDoc(request):
    if "d_member" in request.session:

        if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

        if request.method == 'POST':
            doc = Dossiers.objects.get(id=request.POST['entr'])
            Sucur = Cicursale.objects.get(id=doc.sucur())
            entr = Sucur.entrName()

            pathh = 'dotracks/'+doc.link+'/'
            pathhbd = doc.link+'/'

            handle_uploaded_file(
                request.FILES['imageP'], request.POST['libelle'], request, Sucur, pathh)
            form = docForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.use = Users.objects.get(id=request.session['d_memberid'])
                post.cic = Sucur
                post.dos = doc
                post.libelle = request.POST['libelle']
                post.status = 0
                post.descipt = pathhbd+request.POST['libelle']
                post.dates = timezone.now()
                post.for_field = Format.objects.get(extension=request.POST['ext'])
                post.save()
                return HttpResponse("0")
            else:
                return HttpResponse('Echec lors de la verification des donnees')
        else:
            return HttpResponse("Failed while upload file")


def handle_uploaded_file(file, filename, req, Sucur, pathh):
    if not os.path.exists(pathh):
        os.mkdir(pathh)

    with open(pathh + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def getUserBySuc(user):
    try:
        id = Users.objects.get(id=user).cic
        use = Users.objects.filter(cic=id)
    except ObjectDoesNotExist:
        use = None
    return use


def getDossierBySuc(cic):
    try:
        dos = Dossiers.objects.filter(cic=cic, dos=None)
    except ObjectDoesNotExist:
        dos = None
    return dos

def getChooseDossierBySuc(request):
    try:
        if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

        cic = request.POST['cic']
        dos = Dossiers.objects.filter(cic=cic, dos=None).values('id', 'libelle', 'abreviation', 'status').exclude(status="1")
        if dos.count() != 0:
            rs = list(dos)
        else:
            rs = 0
    except ObjectDoesNotExist:
        rs =0
    return JsonResponse(rs, safe=False)

def getChooseDossierBySuc2(request):
    try:
        if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

        cic = request.POST['cic']
        id = request.POST['dos']
        dos = Dossiers.objects.filter(cic=cic, dos=id).values('id', 'libelle', 'abreviation', 'status').exclude(status="1")
        if dos.count() != 0:
            rs = list(dos)
        else:
            rs = 0     
    except ObjectDoesNotExist:
        rs = 0
    return JsonResponse(rs, safe=False)


def getDossierInfos(dos):
    try:
        doc = Dossiers.objects.filter(id=dos, status=0).values('id', 'libelle', 'abreviation', 'status', 'dos__libelle', 'dos')[0]
    except ObjectDoesNotExist:
        doc = None
    return doc


def getPreDossierInfos(dos):
    try:
        doc = Dossiers.objects.filter(id=dos)[0]
        preDoc = Dossiers.objects.get(id=doc.sDos())
    except ObjectDoesNotExist:
        preDoc = None
    return preDoc


def getsDossierBySuc(dos):
    try:
        doc = Dossiers.objects.filter(dos=dos)
    except ObjectDoesNotExist:
        doc = None
    return doc

def getDocuments(ids):
    try:
        doc = Documents.objects.filter(use=ids, files='0')
    except ObjectDoesNotExist:
        doc = None
    return doc

def getDocumentsDetails(pk):
    try:
        doc = Documents.objects.get(libelle=pk)
    except ObjectDoesNotExist:
        doc = None
    return doc

def getDocumentsBySuc(dos):
    try:
        doc = Documents.objects.filter(dos=dos, for_field__libelle="images")
    except ObjectDoesNotExist:
        doc = None
    return doc

def getDocumentsByDocID(ids):
    try:
        doc = Documents.objects.get(id=ids)
    except ObjectDoesNotExist:
        doc = None
    return doc

def getDocumentFilesBySuc(dos):
    try:
        doc = Documents.objects.filter(dos=dos, for_field__libelle="document").values('id','libelle','for_field__extension', 'status','dates','dos','cic','use')
    except ObjectDoesNotExist:
        doc = None
    return doc

def getDocumentBySuc(dos):
    try:
        doc = Documents.objects.filter(dos=dos, files="0").values('id','libelle','status','dates','dos','cic','use')
    except ObjectDoesNotExist:
        doc = None
    return doc

def getNbrUserBySuc(user):
    try:
        id = Users.objects.get(id=user).cic
        use = Users.objects.filter(cic=id).count()
    except ObjectDoesNotExist:
        use = None
    return use


def getModules():
    try:
        modu = Module.objects.filter(statut=0)
    except ObjectDoesNotExist:
        modu = None
    return modu


def getFormatFichiers(ident):
    try:
        forma = Format.objects.filter(ent=ident).exclude(status="@alphaLock")
    except ObjectDoesNotExist:
        forma = None
    return forma


def getTypeCourriers(ident):
    try:
        forma = Typecourrier.objects.filter(
            ent=ident).exclude(statut="@alphaLock")
    except ObjectDoesNotExist:
        forma = None
    return forma


def getTypeArchives(ident):
    try:
        forma = Typearchives.objects.filter(
            ent=ident).exclude(status="@alphaLock")
    except ObjectDoesNotExist:
        forma = None
    return forma

def getAdminMouchard(iduser):
    try:
        forma =Mouchard.objects.filter(adm=iduser).exclude(statut="@alphaLock").order_by('-id')
    except ObjectDoesNotExist:
        forma = None
    return forma

def getMemberMouchard(iduser):
    try:
        forma = Mouchard.objects.filter(use=iduser).exclude(statut="@alphaLock").order_by('-id')
    except ObjectDoesNotExist:
        forma = None
    return forma

def getMemberPicture(iduser):
    try:
        pic = User_profile.objects.filter(use=iduser).exclude(status="3").order_by('-id')
    except ObjectDoesNotExist:
        pic = None
    return pic

def addFormatDoc(request):
    if 'd_user' in request.session:

        if not request.POST:
            return HttpResponseRedirect(baseUrl())

        if request.method == "POST":
            try:
                form = formatForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.status = 0
                    post.ent = Entreprise.objects.get(
                        id=request.session['d_Entrid'])
                    post.save()
                    rp = 0
                else:
                    rp = "Echec lors de lenregistrement !"
            except:
                rp = 'Erreur not mach'
            return HttpResponse(rp)


def addTypeCourrier(request):
    if 'd_user' in request.session:
        if not request.POST:
            return HttpResponseRedirect(baseUrl())

        if request.method == "POST":
            try:
                form = typecourrierForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.statut = 0
                    post.ent = Entreprise.objects.get(
                        id=request.session['d_Entrid'])
                    post.save()
                    rp = 0
                else:
                    rp = "Echec lors de lenregistrement !"
            except:
                rp = 'Erreur not mach'
            return HttpResponse(rp)

def enregistrerDocument(request):
    if 'd_member' in request.session:

        if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

        if request.method == "POST":
            try:
                form = docForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.status = 0
                    post.files = 0
                    post.descipt = request.POST['descipt']
                    post.libelle = request.POST['libelle'].replace(" ","_")
                    post.dates = timezone.now()
                    post.cic = Cicursale.objects.get(id=request.POST['cic'])
                    post.dos = Dossiers.objects.get(id=request.POST['dos'])
                    post.use = Users.objects.get(id=request.session['d_memberid'])
                    post.save()
                    rp = 0
                else:
                    rp = "Echec lors de lenregistrement !"
            except:
                rp = 'Erreur not mach'
            return HttpResponse(rp)


def addTypeArchives(request):
    if 'd_user' in request.session:
        if not request.POST:
            return HttpResponseRedirect(baseUrl())

        if request.method == "POST":
            try:
                form = typearchivesForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.statut = 0
                    post.ent = Entreprise.objects.get(
                        id=request.session['d_Entrid'])
                    post.save()
                    rp = 0
                else:
                    rp = "Echec lors de lenregistrement !"
            except:
                rp = 'Erreur not mach'
            return HttpResponse(rp)

def allMouchard(request, lang):
    if "d_user" in request.session:
        id = request.session["d_userid"]
        idCic = Users.objects.get(id=id).cic

        return render(request, 'dotracks/dashboard/admin/pagemouchard.html', {"allMouchard": getAdminMouchard(id), 'langue': loadLang(lang), "lang_abbr": checkLangAbbr(lang), "userInfo": get_Userby_id(id), "userList": get_User_by_cic(idCic)})
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def photo_list(request):

    if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

    if request.method == 'POST':

        userpic = Users.objects.get(id=request.POST['use'])

        form = PhotoProfilMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.POST['use'])

            userpic.photo = 'static/dotracks/user_profile/'+request.FILES['photo'].name
            userpic.save()
    else:
        form = PhotoProfilMemberForm()

    return HttpResponseRedirect("profile/"+defaultLang())

def changeProfile(request):

    if not request.POST:
            return HttpResponseRedirect(baseUrl()+"member/login/")

    if request.method == 'POST':
        userpic = Users.objects.get(id=request.session['d_memberid'])
        userpic.photo = request.POST['photo']
        userpic.save()
        return HttpResponse('0')
    else:
        return HttpResponse('1')

def viewsFilesChoose(request):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(4, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login")

        pk = request.POST['id']
        exts = request.POST['exts']

        if exts == "pdf":

            if(exts == "pdf"):
                try:
                    path = "dotracks/"+getDocumentsByDocID(pk).descipt
                    new_f= 'dotracks/'+getDocumentsByDocID(pk).descipt+'_equiv.html'
                    
                    rsrcmgr = PDFResourceManager()
                    retstr = StringIO()
                    codec = 'utf-8'
                    laparams = LAParams()
                    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
                    fp = open(path, 'rb')
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    password = ""
                    maxpages = 0
                    caching = True
                    pagenos=set()

                    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
                        interpreter.process_page(page)
                    lines = retstr.getvalue().splitlines()
                    with open(new_f, 'w+') as f:
                        for line in lines:
                            f.write("<pre>" + line + "</pre>")

                    with open(new_f, 'r') as f:
                        for line in f:
                            html = f.read()
                    
                    fp.close()
                    device.close()
                    retstr.close()

                except:
                    html = '0'
                    
            return HttpResponse(html)
    else:
        return HttpResponseRedirect(baseUrl()+"member/login/"+checkLangAbbr(lang))

def viewsFilesChoos(request):
    if "d_member" in request.session:
        id = request.session["d_memberid"]

        if checkMyAccess(4, id) == 1:
            return HttpResponseRedirect(baseUrl()+"member/login")

        pk = request.POST['id']
        exts = request.POST['exts']

        if exts == "txt" or exts == "html":

            if(exts == "html"):
                try:
                    contents = "dotracks/"+getDocumentsByDocID(pk).descipt
                    with open(contents, 'r') as f:
                        for line in f:
                            html = f.read()
                except:
                    html = '0'
            else:
                try:
                    contents = open("dotracks/"+getDocumentsByDocID(pk).descipt,"r")
                    new_f= 'dotracks/'+getDocumentsByDocID(pk).libelle+'_equiv.html'
                    with open(new_f, 'w+') as f:
                        for line in contents.readlines():
                            f.write("<pre>" + line + "</pre>")

                    with open(new_f, 'r') as f:
                        for line in f:
                            html = f.read()

                    os.unlink(new_f)
                except:
                    html = '0'
        else:
            if exts == "csv":
                hi = []
                with open('dotracks/'+getDocumentsByDocID(pk).descipt, newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        hi = row
                html = '0'
            else:
                try:
                    with open('dotracks/'+getDocumentsByDocID(pk).descipt, "rb") as docx_file:
                        result = mammoth.convert_to_html(docx_file)
                        html = result.value # The generated HTML
                        messages = result.messages # Any messages, such as warnings during conversion
                except:
                    html = '0'

        return HttpResponse(html)
    else:
        return HttpResponse('0')
