from django.conf.urls import url
from .models import Users
from .models import Courriers
from .import views
from django.contrib import admin
from django.conf.urls import include


urlpatterns = {
    url(r'^$', views.home, name='Acceuil'),
    #url(r'^_@r/(?P<lang>\w+)/$', views.AdminR, name='Acceuil'),
    url(r'^(?P<lang>\w+)/$', views.acceuil, name='Acceuil'),
    url(r'^connexion/$', views.Loginadmin, name='Connexion'),
    url(r'^login/facebook', views.LoginFacebook),
    url(r'^connexion/(?P<lang>\w+)/$', views.Loginadmin, name='Connexion'),
    url(r'^inscription/(?P<lang>\w+)/$', views.Register, name='Inscription'),
    url(r'^apropos/(?P<lang>\w+)/$', views.About, name='Apropos'),
    url(r'^contact/(?P<lang>\w+)/$', views.ContactUs, name='Contact'),
    url(r'^courrier/(?P<lang>\w+)/$', views.CourrierUs, name='Courrier'),
    url(r'^courrier/find', views.FindEntr),
    url(r'^courrier/entr/(?P<pk>\d+)/send/(?P<lang>\w+)/$', views.CourrierSend, name='Courrier'), #Formulaire denvoi du courrier.
    url(r'^dashboard/admin/(?P<lang>\w+)/$',
        views.adminIndex, name='Dashboard'),
    url(r'^dashboard/admin/addEntr', views.post_addEntr),
    url(r'^dashboard/company/(?P<pk>\d+)/(?P<lang>\w+)/$', views.startEntr),
    url(r'^dashboard/company/logout/(?P<lang>\w+)', views.LogoutEntr),
    url(r'^dashboard/company/(?P<lang>\w+)/$', views.allEntr, name='Company'),
    url(r'^dashboard/admin/addCicur', views.post_addSucur),
    url(r'^dashboard/sucursale/(?P<pk>\d+)/users/(?P<lang>\w+)/',
        views.sucurUsers, name='Utilisateurs'), #liste utilisateurs entreprise par sucursale.
    url(r'^dashboard/sucursale/(?P<pk>\d+)/acceder/(?P<lang>\w+)/', views.accesSucur),
    url(r'^dashboard/admin/addTypeuser', views.addTypeuse),
    url(r'^dashboard/admin/addUser', views.addUse),
    url(r'^dashboard/company/users/(?P<lang>\w+)/$',
        views.allEntrUsers, name='Utilisateurs'),  #liste utilisateurs entreprise.
        url(r'^dashboard/company/user/(?P<pk>\d+)/profile/(?P<lang>\w+)/$',
        views.profileUserEntr, name='Profile'), #profile utilisateur entreprise.

    url(r'^dashboard/admin/synchroMember', views.synchroMemberAdmin), #synchroniser compte admin-membre.
    url(r'^dashboard/admin/droitTypusers', views.droitTypeusers), #charger droit utilisateur.
    url(r'^dashboard/admin/droitTypeusersMenus', views.droitTypeusersMenus), #charger droit utilisateur Menus
    url(r'^dashboard/admin/removedroitTypusers', views.removedroitTypeusers), #supprimer droit utilisateur
    url(r'^dashboard/admin/senddroitTypusers', views.senddroitTypeusers), #ajouter droit utilisateur
    url(r'^dashboard/admin/editEntrForm', views.get_EntByID), #edit entreprise
    url(r'^dashboard/admin/deleteEntr', views.deleteEntreprise), #delete Entreprise
    url(r'^dashboard/profile/(?P<lang>\w+)/$', views.ProfileAdmin, name='Profile'), #Profile Admin
    url(r'^dashboard/member/checkAcces', views.getMyAccess), #verifier mes droits dacces 

    url(r'^dashboard/courriers/(?P<lang>\w+)/$', views.courrier, name='Courriel Box'), #Courrier Admin
    #url(r'^dashboard/courrier/(?P<lang>\w+)/$', views.courrier, name='Courriel Box'), #Courrier Users

    url(r'^dashboard/administrate/(?P<lang>\w+)/$', views.administrate, name='Administration'),

    url(r'^dashboard/admin/error/(?P<lang>\w+)/$', views.adminError, name='Dashboard'),

    url(r'^member/$', views.LoginMember2, name="Connexion"),
    url(r'^member/login/$', views.LoginMember2, name="Connexion"),
    url(r'^member/login/(?P<lang>\w+)/$', views.LoginMember, name="Connexion"),
    url(r'^dashboard/Member/(?P<lang>\w+)/$', views.adminMember, name='Administration'),
    url(r'^member/forgotPassword', views.forgotPassMember, name="Recuperation"),
    url(r'^Member/profile/(?P<lang>\w+)/$', views.Profile, name="Profile"),
    url(r'^Member/documents/(?P<lang>\w+)/$', views.Document, name="Mes Documents"),

    url(r'^Member/documents/(?P<pk>\w+)/(?P<lang>\w+)/$', views.DocumentOpen, name="Details du Document"),
    url(r'^Member/documents/(?P<pk>\w+)/(?P<ob>\w+)/(?P<lang>\w+)/$', views.DocumentOperation, name="Configuration du Document"),

    url(r'^Member/addMemberProfile', views.photo_list),

    url(r'^Member/users/(?P<lang>\w+)/$', views.Memberusers, name="Utilisateurs"),
    url(r'^Member/chat/(?P<lang>\w+)/$', views.MemberMessagerie, name="Messagerie"),
    url(r'^Member/chat/(?P<pk>\w+)/(?P<lang>\w+)/$', views.MemberMessagerie2, name="Messagerie"),
    url(r'^Member/searchChat', views.getSearchChat),
    url(r'^dashboard/addDossier', views.addDossier),
    url(r'^Member/dossiers/(?P<lang>\w+)/$', views.DossierMember, name="Dossiers"),
    url(r'^Member/dossiers/(?P<pk>\d+)/(?P<lang>\w+)/$', views.openDossier, name="Dossiers"),
    url(r'^Member/addDocx/(?P<lang>\w+)/$', views.addDocuments, name="Documents"),
    url(r'^Member/courrier/(?P<lang>\w+)/$', views.memberCourrier, name="Courrier"),
    url(r'^Member/addFileImage', views.addImageDoc),
    url(r'^Member/addFormatDoc', views.addFormatDoc),
    url(r'^Member/addTypeCourrier', views.addTypeCourrier),
    url(r'^Member/addTypeArchives', views.addTypeArchives),
    url(r'^Member/addMouchard', views.TraceMouchard),
    url(r'^dashboard/company/activite/(?P<lang>\w+)/$', views.allMouchard, name="Mouchard"),
    url(r'^Member/configuration/(?P<lang>\w+)/$', views.configSuccursale, name="Configuration"),

    url(r'^Member/chatValidate', views.EnvoiDuChat),
    url(r'^Member/retriveChat', views.recuperationChat),
    url(r'^Member/chatViews', views.messageLus),
    url(r'^Member/notification', views.addNotif),
    url(r'^Member/loadNotif', views.chargerNotification),
    url(r'^Member/countNotif', views.conterNotification),
    url(r'^Member/vuNotif', views.vuNotification),
    url(r'^Member/ChooseDossierBySuc', views.getChooseDossierBySuc),
    url(r'^Member/ChooseDossierSucById', views.getChooseDossierBySuc2),
    url(r'^Member/saveDOCcontent', views.enregistrerDocument),

    url(r'^Member/viewsOpenFiles/', views.viewsFilesChoose, name="Ouverture du Fichier"),

       url(r'^Member/viewsFilesOpen/', views.viewsFilesChoos),

    url(r'^logout/(?P<lang>\w+)/$', views.Logout, name='logout'),
    url(r'^Member/logout/(?P<lang>\w+)/$', views.LogoutMember, name='logout'),

    url(r'^Member/changeProfil', views.changeProfile),

    #url(r'^admin/', admin.site.urls),
}
