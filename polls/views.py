from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import  Questions, Choice, DriverDetail, Person, City, CarDetails,Bookings
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic
from .forms import DriverDetailForm, PersonCreationForm,SignUpForm,TravelOneWayInputForm,BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def hotelsview(request):
    return render(request, "hotels.html")

def cardetailview(request):
    cars = CarDetails.objects.filter(available=True)
    return render(request, 'car_detail.html', {'cars': cars})

def travelonewayinput(request):
    form = TravelOneWayInputForm()
    if request.method == 'POST':
        form = TravelOneWayInputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:cardetailview')
    return render(request, 'travelonewayinput.html', {'form': form})

@login_required()
def book_car_view(request):
    # return HttpResponse(f"User id --> {request.user}")
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            booking.car.available = False
            booking.car.save()
            return redirect('polls:booking_success')
    return render(request, 'book_car.html', {'form': form})
@login_required
def booking_success(request):
    return render(request, 'booking_success.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect after successful login
        else:
            return render(request, 'polls/login.html', {'error': 'Invalid credentials'})
    return render(request, 'polls/login.html')
def registerView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:login')
    else:
            form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    #return HttpResponse("This is your Index Page")
    return render(request, "index.html")

def bookyourride(request):
    #return HttpResponse("Here you can book your ride")
    return render(request, "bookyourride.html")

def create_driver_detail(request):
    if request.method == 'POST':
        form = DriverDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('polls:index'))
    else:

        form = DriverDetailForm()

    return render(request, 'create_driver_detail.html', {'form': form})

def success(request):
    return render(request, 'success.html')

@login_required
def driverdertail(request):
    driverdetail = DriverDetail.objects.all()
    context = {'driverdetail': driverdetail}
    return render(request, "driverdetail.html", context)
    # output = '<br> '.join([q.firstname for q in driverdetail])
    # return HttpResponse(output)

    # #latest_question_list = Questions.objects.order_by('pub_date')[:5]
    # latest_question_list = Questions.objects.all()
    # template = loader.get_template("polls/index.html")
    # context ={'latest_question_list': latest_question_list}
    # #output = '<br> '.join([q.question_text for q in latest_question_list])
    # #return HttpResponse(output)
    # #return  HttpResponse(template.render(context,request))
    # return  render(request,"polls/index.html",context)

def detail(request,question_id):
    # try:
    #     question= Questions.objects.get(pk=question_id)
    #     #return HttpResponse("you are looking for question %s" % question_id)
    # except Questions.DoesNotExist:
    #     raise Http404("Question does not Exist")
    question = get_object_or_404(Questions,pk=question_id)
    return render(request,"polls/details.html", {'question': question})

# for drop Down Person Craete Views
def person_create_view(request):
    form = PersonCreationForm()
    if request.method == 'POST':
        form = PersonCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'polls/home.html', {'form': form})

def person_update_view(request, pk):
    person = get_object_or_404(Person, pk=pk)
    form = PersonCreationForm(instance=person)
    if request.method == 'POST':
        form = PersonCreationForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_change', pk=pk)
    return render(request, 'polls/home.html', {'form': form})

def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, "results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        return render(request, "results.html", {'question': question})


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Questions.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Questions
    template_name = "details.html"


class ResultsView(generic.DetailView):
    model = Questions
    template_name = "results.html"