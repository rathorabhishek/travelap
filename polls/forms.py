from django import forms
from .models import DriverDetail, Person, City,TravelOneWayInput, Bookings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import datetime

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    last_name = forms.CharField(max_length=30, widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    username = forms.CharField(max_length=254, widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    password1=forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'d-form form-control'}))
    password2=forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'d-form form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form form-control'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form form-control'}))

    class Meta:
        model = User

# PersonCreationForm will be delete ,only kept for learning .
class PersonCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class DriverDetailForm(forms.ModelForm):
    # car_type_choice =[("sedan", "Sedan"),("sport", "Sport"), ("luxury", "Luxury"),]
    # firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'fs-form form-control', 'placeholder': 'FirstName'}), required=True)
    # middlename = forms.CharField(widget=forms.TextInput(attrs={'class': 'fs-form form-control', 'placeholder': 'MiddleName'}), required=True)
    # lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'fs-form form-control', 'placeholder': 'LastName'}), required=True)
    # experience = forms.CharField(widget=forms.TextInput(attrs={'class': 'fs-form form-control', 'placeholder': 'Exp.'}), required=True)
    # carname = forms.CharField(widget=forms.TextInput(attrs={'class': 'fs-form form-control', 'placeholder': 'Your Car e.g Hyundai .Suzuki'}), required=True)
    # carType = forms.ChoiceField(choices=car_type_choice)

    class Meta:
            model = DriverDetail
            fields = '__all__'
            #fields = ['firstname', 'middlename', 'lastname', 'experience', 'carname','cartype', 'carnumber', 'address', 'mobilenumber', 'adharnumber', 'hiringdate']


class TravelOneWayInputForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, label='DATE', widget=forms.TextInput)
    class Meta:
        model = TravelOneWayInput
        fields = '__all__'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['car', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }