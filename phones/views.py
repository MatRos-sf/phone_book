from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PersonForms, MailForms, PhoneForms, AddRandomPeopleForms
from django.views.generic import ListView, DetailView
from .models import Person, Phone, Mail


class HomeView(ListView):
    model = Person
    template_name = "phones/home_page.html"
    context_object_name = 'people'


    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(name__icontains=query) | Q(surname__icontains=query) |
                                                    Q(phone__phone__icontains=query) | Q(mail__mail__icontains=query))
            object_list = object_list.distinct()
        else:
            object_list = self.model.objects.all()
        return object_list

class DetailPersonView(DetailView):
    model = Person
    template_name = "phones/detail.html"
    context_object_name = 'person'

# --------------------------- ADD------------------------------------------------
#add new user
def add_user(request):
    add_person = False
    if request.method == "POST":
        form_person = PersonForms(request.POST)
        form_mail = MailForms(request.POST)
        form_phone= PhoneForms(request.POST)
        if form_person.is_valid():
            user = form_person.save()
            if form_phone.is_valid():
                cd = form_phone.cleaned_data
                if cd['phone']:
                    #Phone
                    number_phone = form_phone.save(commit=False)
                    #Przypisywanie numeru do użytkownika
                    number_phone.person = user
                    number_phone.save()
            if form_mail.is_valid():
                cd = form_mail.cleaned_data
                if cd['mail']:
                    #Email
                    mail = form_mail.save(commit=False)
                    #Przypisane maila
                    mail.person = user
                    mail.save()
            add_person = True
    else:
        form_person = PersonForms()
        form_mail = MailForms()
        form_phone= PhoneForms()
    return render(request, "phones/add.html", {"add": add_person,
                                               "form_person": form_person,
                                               "form_mail": form_mail,
                                               "form_phone": form_phone})

#add new phone number
def add_phone(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PhoneForms()
    add = False
    if request.method == 'POST':
        form = PhoneForms(request.POST)
        if form.is_valid():
            phone = form.save(commit=False)
            cd = form.cleaned_data
            if cd['phone']:
                phone.person = person
                phone.save()
                add = True
    return render(request,"phones/add_item.html", {"form": form,
                                                   'item': 'Numer',
                                                   'add': add})

#add new mail
def add_mail(request, id):
    person = get_object_or_404(Person, pk=id)
    form = MailForms()
    add = False
    if request.method == 'POST':
        form = MailForms(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            cd = form.cleaned_data
            if cd['mail']:
                mail.person = person
                mail.save()
                add = True
    return render(request,"phones/add_item.html", {"form": form,
                                                   'person': person,
                                                   'item': 'Mail',
                                                   'add': add})


# ----------------------------- EDIT function ------------------------------
def edit(request, id):
    person = get_object_or_404(Person, pk=id)
    return render(request, "phones/edit.html", {"person": person})

def edit_personal_data(request, id):
    person = get_object_or_404(Person, pk=id)
    form_person = PersonForms(instance=person)
    person_update = False
    if request.method == "POST":
        form_person = PersonForms(request.POST)

        if form_person.is_valid():
            cd = form_person.cleaned_data
            if cd['name'] != person.name:
                person.name = cd['name']
            if cd['surname'] != person.surname:
                person.surname = cd['surname']
            person.save()
            person_update=True

    return render(request, "phones/edit_person.html", {'person': form_person,
                                                       'update': person_update})

def edit_number(request, id):
    item = get_object_or_404(Phone, pk=id)
    form_phone = PhoneForms(instance=item)
    phone_update = False
    if request.method =='POST':
        form_phone = PhoneForms(request.POST)
        if form_phone.is_valid():
            cd = form_phone.cleaned_data
            if cd['phone'] != item.phone:
                item.phone = cd['phone']
                phone_update=True
            item.save()
    return render(request, "phones/edit_item.html", {"form": form_phone,
                                                     "update": phone_update,
                                                     "item": 'Numer'})
def edit_mail(request, id):
    item = get_object_or_404(Mail, pk=id)
    form_mail = MailForms(instance=item)
    mail_update = False
    if request.method =='POST':
        form_mail = MailForms(request.POST)
        if form_mail.is_valid():
            cd = form_mail.cleaned_data
            if cd['mail'] != item.mail:
                item.mail = cd['mail']
                mail_update=True
            #sprawdzanie czy coś zostało zmienione
            if mail_update:
                item.save()
    return render(request, "phones/edit_item.html", {"form": form_mail,
                                                     "update": mail_update,
                                                     "item": 'Mail'})


#---------------------- DELETE USER ------------------------------------
#https://doit.ansta.pl/op/pomoc/artykul/generuj/1432/

def delete_person(request, id):
    person = get_object_or_404(Person, pk=id)
    can_delete = True
    is_delete = False
    if not person.is_mail_or_number():
        if request.method == 'POST':
            person.delete()
            is_delete = True
    else:
        can_delete = False
    return render(request, "phones/delete.html", {'can_delete':can_delete,
                                                  'person': person,
                                                  'is_delete': is_delete})

from .generation_fake_data import data_fake

def add_random_people(request):
    #password: dodaj
    form = AddRandomPeopleForms()
    add = False
    added = 0
    if request.method == "POST":
        form = AddRandomPeopleForms(request.POST)
        if form.is_valid() and request.POST.get('code') == 'dodaj':
            amount_people = int(request.POST.get('amount',0))
            add = True
            for i in range(amount_people):
                person = Person.objects.create(**data_fake.data_person())

                # czy twozymy numer telefonu?
                if data_fake.create_or_no():
                    amount = data_fake.hom_many()
                    for i in range(amount):
                        person.phone.create(**data_fake.data_phone())
                # czy tworzymy maial
                if data_fake.create_or_no():
                    amount = data_fake.hom_many()
                    for i in range(amount):
                        person.mail.create(**data_fake.data_email())
                added +=1


    return render(request,"phones/generation/generation.html", {'form': form,
                                                                'add': add,
                                                                'item': added})





