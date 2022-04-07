from django.db import models
from django.urls import reverse
class Person(models.Model):
    name = models.CharField(max_length=50, blank=False)
    surname = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return "{} {}".format(self.name, self.surname)

    def get_absolute_url(self):
        return reverse("detail", args=[self.pk])

    def get_phone_numbers(self):
        phone_numbers = []
        for number in self.phone.all():
            if number != '':
                phone_numbers.append(number.phone)
        return phone_numbers

    def get_mails(self):
        mails = []
        for mail in self.mail.all():
            mails.append(mail)
        return mails

    def is_mail_or_number(self):
        if self.get_mails() or self.get_phone_numbers():
            return True
        return False

class Phone(models.Model):
    person = models.ForeignKey(Person, editable=False, on_delete=models.CASCADE, related_name='phone')
    phone = models.CharField(max_length=50, blank=True)

    def get_absolute_url(self):
        return reverse('edit_number', args=[self.pk])

class Mail(models.Model):
    person = models.ForeignKey(Person, editable=False, on_delete=models.CASCADE, related_name='mail' )
    mail = models.EmailField(blank=True,default='')
    def get_absolute_url(self):
        return reverse('edit_mail', args=[self.pk])

    def __str__(self):
        return self.mail