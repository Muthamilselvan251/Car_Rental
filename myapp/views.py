from django.shortcuts import render,redirect,get_object_or_404
from.forms import MyRegistrationForm,LoginData,MyReserveForm
from django.contrib import messages
from .models import Car,MyReserve,RegisterData,message,MyPassword
from django.contrib.auth import authenticate,login
import hashlib
from datetime import datetime
# from django.conf import settings
# from .models import Payment
# import razorpay


def home(request):
    return render(request,'Home.html')
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if not RegisterData.objects.filter(password=password,username=username).exists():
            messages.error(request, "User does not exist.")
            return redirect("/login")
        if user is None:
            login(request,user)
            obj = LoginData()
            obj.username = username
            obj.password = password
            obj.save()
            messages.success(request, "Login is Successfully")
            return redirect("Home")
        else:
            messages.error(request, "Invalid User Name or Password")
            return redirect("/login")
    return render(request, "Loginpage.html")


def forgot_password(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        user = RegisterData.objects.filter(contact=contact).first()

        if not user:
            messages.error(request, "User does not exist.")
            return redirect("/forgot_password")

        # Proceed to reset password page
        return redirect(f"/reset_password/{user.contact}/")

    return render(request, 'forgot_password.html')


def reset_password(request, contact):
    try:
        user = RegisterData.objects.get(contact=contact)
    except RegisterData.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('/forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')

        # Store the old password in Password table
        old_password = user.password
        MyPassword.objects.create(user=user, password=old_password)

        # Update the user's current password
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        user.password = hashed_password
        user.save()

        messages.success(request, "Password updated successfully.")
        return redirect('/login')

    return render(request, 'reset_password.html', {'contact': contact})

def register(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successfully You Can Login Now....!")
            return redirect("/login")
    else:
        form = MyRegistrationForm()
    return render(request, "Register.html",{'form':form})

def rentcar(request):
    query = request.GET.get('q')
    if query:
        MyCar = Car.objects.filter(car_name__icontains=query)
    else:
        MyCar = Car.objects.all()
    return render(request,'Rentcar.html',{'MyCar': MyCar})

def aboutus(request):
    return render(request,'aboutus.html')
def contactus(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['Email']
        tellme = request.POST['tellme']

        obj = message()
        obj.fullname = fullname
        obj.Email = email
        obj.tellme = tellme
        obj.save()
        messages.success(request, "Thank You For Your Message")
        return redirect("Home")

    return render(request,'Contact.html')


def booknow(request):
    if request.method == 'GET':
        # Retrieve car details from GET parameters
        car_id = request.GET.get('car_id')
        car_name = request.GET.get('car_name')
        car_image = request.GET.get('car_image')
        car_price = request.GET.get('car_price')

        # Check if required parameters are missing
        if not car_id or not car_name or not car_image or not car_price:
            return render(request, 'error.html', {'message': 'Missing car details.'})

        # Retrieve car object based on car_id
        car = get_object_or_404(Car, id=car_id)

        # Initialize form with initial data
        form = MyReserveForm(initial={'Car': car_name, 'price': car_price})

        return render(request, 'booknow.html', {
            'car': car,
            'car_name': car_name,
            'car_image': car_image,
            'car_price': car_price,
            'form': form,
        })

    elif request.method == 'POST':
        form = MyReserveForm(request.POST)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.price = request.POST.get('car_price')

            # Calculate total price and days_difference based on form data
            pickdate = request.POST.get('pickdate')
            dropdate = request.POST.get('dropdate')
            price = float(request.POST.get('car_price', 0))

            if pickdate and dropdate:
                try:
                    pickdate = datetime.strptime(pickdate, '%Y-%m-%d')
                    dropdate = datetime.strptime(dropdate, '%Y-%m-%d')
                    days_difference = (dropdate - pickdate).days + 1

                    if days_difference > 0:
                        total_price = price * days_difference
                        reservation.total_price = total_price  # Save total price to the reservation
                        reservation.days_difference = days_difference  # Save days_difference to the reservation
                        reservation.save()
                        phone_number = form.cleaned_data['phone_number']
                        reservation.phone_number = phone_number
                        return render(request, 'back_home.html',
                                      {'total_price': total_price, 'days_difference': days_difference,'upi_id': 'muthamilselvan251@oksbi',  # Replace with your UPI ID
                                              'name': 'Car|Rental',})
                    else:
                        error = "Drop-off date must be after pick-up date."
                except (ValueError, TypeError):
                    error = "Invalid date format."
            else:
                error = "Pick-up date and drop-off date are required."

            # Handle error cases
            return render(request, 'booknow.html', {
                'error': error,
                'form': form,
                'car': get_object_or_404(Car, id=request.POST.get('car_id')),
                'car_name': request.POST.get('car_name'),
                'car_image': request.POST.get('car_image'),
                'car_price': request.POST.get('car_price'),
            })

        else:
            # If form is invalid, re-render the page with form errors
            car_id = request.POST.get('car_id')
            car_name = request.POST.get('car_name')
            car_image = request.POST.get('car_image')
            car_price = request.POST.get('car_price')
            car = get_object_or_404(Car, id=car_id)
            return render(request, 'booknow.html', {
                'car': car,
                'car_name': car_name,
                'car_image': car_image,
                'car_price': car_price,
                'form': form,
            })

    else:
        # Handle other request methods (not expected in this scenario)
        return render(request, 'error.html', {'message': 'Invalid request method.'})
def success_view(request):
    return render(request, 'back_home.html')
def send_message(request):
    return render(request,'send_message.html')


# def reserve_view(request, reservation_id):
#     # Retrieve the reservation object from the database
#     reservation = get_object_or_404(MyReserve, pk=reservation_id)
#
#     if request.method == 'POST':
#         # Approve the reservation
#         reservation.approve_reservation()
#         total_price = reservation.calculate_total_price()
#
#         phone_number = reservation.phone_number
#         message = 'Your reservation has been approved. Thank you!'
#         if send_sms(phone_number, message):
#             return render(request, 'success.html',{'total_price':total_price})
#         else:
#             return render(request, 'error.html')
#
#         # Calculate total price
#
#
#     return render(request, 'approve_reservation.html', {'reservation': reservation})

# def total_price(request):
#     total_price = None
#     error = None
#
#     if request.method == 'POST':
#         pickdate = request.POST.get('pickdate')
#         dropdate = request.POST.get('dropdate')
#         price = request.POST.get('price')
#         form = MyReserveForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.price = request.POST.get('car_price')
#             reservation.save()
#
#         if pickdate and dropdate and price:
#             try:
#                 pickdate = datetime.strptime(pickdate, '%Y-%m-%d')
#                 dropdate = datetime.strptime(dropdate, '%Y-%m-%d')
#                 price = float(price)
#                 days_difference = (dropdate - pickdate).days + 1
#                 if days_difference > 0:
#                     total_price = price * days_difference
#                 else:
#                     error = "Drop-off date must be after pick-up date."
#
#             except (ValueError, TypeError):
#                 error = "Invalid input. Please check the dates and price."
#
#         if total_price is not None:
#             return render(request, 'back_home.html', {
#                 'total_price': total_price
#             })
#         else:
#             return render(request, 'booknow.html', {
#                 'error': error
#             })
#
#     return render(request, 'booknow.html')


# client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
#
#
# def initiate_payment(request, reserve_id):
#     try:
#         reservation = MyReserve.objects.get(id=reserve_id)
#         total_price = reservation.price  # Assuming total_price is stored in the price field
#     except MyReserve.DoesNotExist:
#         # Handle case where reservation with given ID does not exist
#         return render(request, 'error.html', {'error': 'Reservation not found'})
#
#     if request.method == 'POST':
#         amount = (total_price*100)  # Amount in paise
#
#         # Create Razorpay Order
#         payment = client.order.create({
#             'amount': amount,
#             'currency': 'INR',
#             'payment_capture': '1'
#         })
#
#         # Update reservation with order details
#         reservation.order_id = payment['id']
#         reservation.save()
#
#         context = {
#             'api_key': settings.RAZORPAY_API_KEY,
#             'order_id': payment['id'],
#             'amount': amount,
#             'name': reservation.name,
#             'description': f'Reservation for {reservation.Car}',
#             'prefill': {
#                 'name': reservation.name,
#                 'email': reservation.email,
#                 'contact': reservation.phone_number,
#             },
#             'callback_url': 'payment_success/',  # Update with your callback URL
#         }
#         return render(request, 'payment.html', context)
#     return render(request, 'initiate_payment.html', {'total_price': total_price})
#
# import razorpay
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# @csrf_exempt
# def process_payment(request):
#     if request.method == 'POST':
#         data = request.body.decode('utf-8')
#         payment_data = json.loads(data)
#
#         razorpay_payment_id = payment_data['razorpay_payment_id']
#         razorpay_order_id = payment_data['razorpay_order_id']
#         razorpay_signature = payment_data['razorpay_signature']
#
#         # Verify payment details with Razorpay
#         client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
#         try:
#             payment_response = client.utility.verify_payment_signature({
#                 'razorpay_payment_id': razorpay_payment_id,
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_signature': razorpay_signature,
#             })
#             # Payment verification successful, process further as needed
#             return JsonResponse({'status': 'success', 'message': 'Payment verified successfully'})
#         except razorpay.errors.SignatureVerificationError as e:
#             # Payment verification failed
#             return JsonResponse({'status': 'error', 'message': 'Payment verification failed'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

