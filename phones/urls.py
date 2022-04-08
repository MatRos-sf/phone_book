from django.urls import path, include
from .views import (add_user, HomeView, DetailPersonView, edit, edit_personal_data, edit_number,
                    edit_mail, add_phone, add_mail, delete_person, add_random_people)
urlpatterns = [

    path("", HomeView.as_view(), name="home"),
    path("detail/<int:pk>/", DetailPersonView.as_view(), name='detail'),
    # EDIT url
    path("edit/<int:id>/", edit, name='edit') ,
    path("edit/<int:id>/personal_data/",edit_personal_data , name='edit_personal_data'),
    path("edit/edit_number/<int:id>/", edit_number, name='edit_number'),
    path("edit/edit_mail/<int:id>/", edit_mail, name='edit_mail'),
    # ADD item
    path("add/", add_user, name='add'),
    path("add/person/<int:id>/number/", add_phone, name='add_phone'),
    path("add/person/<int:id>/mail/", add_mail, name='add_mail'),
    #DELETE url
    path("delete/person/<int:id>/", delete_person, name='delete_person'),
    path("random/", add_random_people, name='random')
]
