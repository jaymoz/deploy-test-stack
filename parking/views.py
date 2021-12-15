from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import random
import string
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from parking.models import Bookings, Parking_Space
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware
from .decorators import allowed_users
from .forms import Parking_SpaceForm, BookingForm

def get_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret

def create_booking_number():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

@login_required
def home(request):
    user = request.user
    user_bookings = Bookings.objects.filter(owner=user)
    all_bookings = Bookings.objects.all()
    context = {'user':user, 'user_bookings':user_bookings, 'all_bookings':all_bookings}
    return render(request, 'parking/dashboard.html', context)

@login_required
def get_parking_spaces(request):
    park = Parking_Space.objects.all()
    context = {'park':park}
    return render(request, "parking/parking.html", context)

@login_required
def booking(request, pk):
    park = get_object_or_404(Parking_Space, id=pk)
    form = BookingForm()
    if (request.method == 'POST'):
            form = BookingForm(request.POST or None)
            no = create_booking_number()
            if form.is_valid:
                if park.ft_is_available():
                    start = form.data['start_period']
                    end = form.data['end_period']
                    if ((get_datetime(start) >= timezone.now()) and (timezone.now() < get_datetime(end)) and (get_datetime(start) < get_datetime(end))):
                        booking = Bookings(
                            owner = request.user,
                            manufacturer = form.data['manufacturer'],
                            car_model = form.data['car_model'],
                            color = form.data['color'],
                            plate_number = form.data['plate_number'],
                            start_period = form.data['start_period'],
                            end_period = form.data['end_period'],
                            is_booked = True,
                            ticket = no,
                            phone = form.data['phone'],
                            parking_space = park
                        )
                        booking.save()
                        park.no_of_spaces = park.ft_remove_space()
                        park.save()
                        messages.success(request, "Booking was succesfully placed")
                        return redirect("/")
                    else:
                        messages.info(request, "Date fields are invalid")
                        return redirect("booking", pk=pk)
                else:
                    messages.info(request, "sorry there are curently no parking spaces available")
                    return redirect("booking", pk=pk)
            else:
                messages.warning(request, "Please ensure to fill in valid details!!!")
                return redirect("booking", pk=pk)
    context = {'form':form}
    return render(request, "parking/booking.html", context)

@login_required
@allowed_users(allowed_roles=['Manager'])
def edit_booking(request, pk):
    booking = get_object_or_404(Bookings, id=pk)
    form = BookingForm(instance=booking)

    if (request.method == 'POST'):
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid:
            start = form.data['start_period']
            end = form.data['end_period']
            if ((get_datetime(start) >= timezone.now()) and (timezone.now() < get_datetime(end)) and (get_datetime(start) < get_datetime(end))):
                form.save()
                messages.success(request, "Successfully updated!")
                return redirect("/")
            else:
                messages.info(request, "Date fields are invalid")
                return redirect("edit-booking", pk=pk)
        else:
            messages.info(request, "Please ensure to fill in valid details")
            return redirect("edit-booking", pk=pk)
    
    context = {'booking':booking, 'form':form}
    return render(request, "parking/edit-booking.html", context)

@login_required
@allowed_users(allowed_roles=['Manager'])
def cancel_booking(request, pk):
    booking = get_object_or_404(Bookings, id=pk)
    if request.method == 'POST':
        booking.is_booked = False
        booking.parking_space.no_of_spaces = booking.parking_space.ft_add_space()
        booking.save()
        booking.parking_space.save()
        messages.success(request, "Booking successfully cancelled")
        return redirect("/")
    context = {'booking':booking}
    return render(request, "parking/cancel-booking.html", context)

@login_required
@allowed_users(allowed_roles=['Manager'])
def add_parking_space(request):
    form = Parking_SpaceForm()
    if (request.method == 'POST'):
            form = Parking_SpaceForm(request.POST or None)
            if form.is_valid:
                space = Parking_Space(
                    park_name = form.data['park_name'],
                    no_of_spaces = form.data['no_of_spaces'],
                    )
                space.save()
                messages.success(request, "Parking Space succcessfully created")
                return redirect("/")
            else:
                messages.info(request, "Please provide valid details")
                return redirect("add-parking-space")
    context = {'form':form}
    return render(request, "parking/add-space.html", context)

@login_required
@allowed_users(allowed_roles=['Manager'])
def update_parking_space(request, pk):
    parking_space = get_object_or_404(Parking_Space, id=pk)
    form = Parking_SpaceForm(instance=parking_space)
    if (request.method == 'POST'):
            form = Parking_SpaceForm(request.POST or None, instance=parking_space)
            if form.is_valid:
                form.save()
                messages.success(request, "Parking Space succcessfully updated")
                return redirect("/")
            else:
                messages.info(request, "Please provide valid details")
                return redirect("update-space", pk=pk)
    context = {'form':form}
    return render(request, "parking/update-space.html", context)

@login_required
@allowed_users(allowed_roles=['Manager'])
def delete_parking_space(request, pk):
    parking_space = get_object_or_404(Parking_Space, id=pk)
    if (request.method == 'POST'):
        parking_space.delete()
        messages.success(request, "Parking Space succcessfully deleted")
        return redirect("/")
    return render(request, "parking/delete-space.html")