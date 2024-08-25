from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
import razorpay ,logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import UserProfile,CarCategory,Car,Payment,Booking
from .forms import CustomUserCreationForm,customloginform,BookingForm,PaymentForm
from django.contrib.auth import login,authenticate,logout
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.db.models import Q




# Create your views here.
def index(request):
  return render(request,'carapp/index.html')
def about(request):
  return render(request,'carapp/about.html')

# def car(request):
#   data_value = Car.objects.all().order_by('-id')
#   return render(request,'carapp/car.html',{'datas':data_value})
def contact(request):
  return render(request,'carapp/contact.html')
def pricing(request):
  return render(request,'carapp/pricing.html')
def booksuccess(request):
  return render(request,'carapp/booksuccess.html')
def services(request):
  return render(request,'carapp/services.html')
def payment(request):
  return render(request,'carapp/payment.html')

def index(request):
  return render(request,'carapp/index.html')

def signup(request):
  if request.method== 'POST':
    form=CustomUserCreationForm(request.POST)
    if form.is_valid():
      user=form.save()
      UserProfile.objects.create(user=user)
      msg='Signup completed'
      return render(request,'carapp/signup.html',{'form':form,'msg':msg})
    else:
      return render(request,'carapp/signup.html',{'form':form})
  else:
      form=CustomUserCreationForm()
      return render(request,'carapp/signup.html',{'form':form})


def category(request, id):
    categories=CarCategory.objects.all()
    category = get_object_or_404(CarCategory, id=id)
    car_names = Car.objects.filter(category=category)
    return render(request, 'carapp/category.html', {'category': category, 'car_names': car_names, 'categories':categories})




def login_page(request):
        if request.method == 'POST':

            form=customloginform(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                request.session['username']=username
                if user is not None:
                    request.session['id']=user.id
                    login(request, user)
                    return redirect(index)
                else:
                    return render(request,'carapp/login_page.html',{'form':form})
            else:
                    return render(request,'carapp/login_page.html',{'form':form})
        else:
            form=customloginform()
            return render(request,'carapp/login_page.html',{'form':form})


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))




def book_now(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.user = request.user
            duration = (booking.end_date - booking.start_date).days
            if duration == 0:
                duration = 1
            booking.total_price = duration * car.daily_rental_rate

            amount = int(booking.total_price * 100)
            order = razorpay_client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            })

            if car.book_car():
                try:
                    booking.save()
                    Payment.objects.create(
                        user=request.user,
                        booking=booking,
                        amount=booking.total_price,
                        razorpay_order_id=order['id']
                    )

                    context = {
                        'form': form,
                        'car': car,
                        'order_id': order['id'],
                        'amount': amount,
                        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                        'booking_id': booking.id
                    }
                    return render(request, 'carapp/payment.html', context)
                except Exception as e:
                    car.stock += 1
                    car.save()
                    form.add_error(None, "An error occurred while processing your booking.")
            else:
                form.add_error(None, "Sorry, this car is no longer available.")
    else:
        form = BookingForm()

    context = {
        'form': form,
        'car': car,
    }

    return render(request, 'carapp/book_now.html', context)





def payment(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        print("Pay completed")
        try:
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'Paid'
            payment.save()

            booking = payment.booking
            booking.status = 'Confirmed'
            booking.save()

            context = {
                'payment': payment,
                'booking': booking,
                'car': booking.car
            }
            return render(request, 'carapp/booksuccess.html', context)
        except razorpay.errors.SignatureVerificationError:
            # Handle signature verification error
            return JsonResponse({'status': 'failure'}, status=400)




def car_single(request,id):
  datas=get_object_or_404(Car, id=id)
  return render(request,'carapp/car_single.html',{'data':datas})

def paylist(request):
    payments = Payment.objects.all()
    return render(request, 'carapp/paylist.html', {'payments': payments})




def logout_page(request):
    if 'username' in request.session:
        del request.session['username']
        logout(request)
        return redirect('index')



logger = logging.getLogger(__name__)


def payment_success(request):
    return render('booksuccess.html')


# def payment_success(request):
#     if request.method == "POST":
#         razorpay_payment_id = request.POST.get('razorpay_payment_id')
#         razorpay_order_id = request.POST.get('razorpay_order_id')
#         razorpay_signature = request.POST.get('razorpay_signature')
#         payment_id = request.POST.get('payment_id')

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': razorpay_payment_id,
#             'razorpay_signature': razorpay_signature
#         }

#         try:
#             client.utility.verify_payment_signature(params_dict)
#             payment = Payment.objects.get(id=payment_id)
#             payment.razorpay_payment_id = razorpay_payment_id
#             payment.razorpay_signature = razorpay_signature
#             payment.status = 'Success'
#             payment.save()
#             return render(request, 'booksuccess.html')
#         except razorpay.errors.SignatureVerificationError:
#             return HttpResponseBadRequest("Payment verification failed.")
#     return HttpResponseBadRequest("Invalid request method.")

from django.shortcuts import render

def car(request):
    today = timezone.now().date()

    active_bookings = Booking.objects.filter(
        Q(start_date__lte=today, end_date__gte=today, status='Confirmed') |
        Q(status='Pending')
    ).values_list('car', flat=True)

    available_cars = Car.objects.filter(
        stock__gt=0
    ).order_by('-id')

    for car in available_cars:
        print(f'Car ID: {car.id}, Make: {car.make}, Model: {car.model}, Stock: {car.stock}')

    return render(request, 'carapp/car.html', {'datas': available_cars})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    car = booking.car
    booking.delete()


    car.stock += 1
    car.save()

    return redirect('car')


