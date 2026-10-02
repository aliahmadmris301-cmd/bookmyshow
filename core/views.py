from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Event, Booking
from .forms import SignUpForm
def home(request):
    return render(request,'core/home.html')
def signup(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        form=SignUpForm()
    return render(
        request,
        'core/signup.html',
        {'form':form}
    )
def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        form=AuthenticationForm()
    return render(
        request,
        'core/login.html',
        {'form':form}
    )
@login_required
def dashboard(request):
    if request.method=='POST':
        event_id=request.POST.get('event_id')
        quantity=int(
            request.POST.get('quantity', 1)
        )
        event=Event.objects.get(id=event_id)
        if quantity<=event.available_seats:
            Booking.objects.create(
                user=request.user,
                event=event,
                quantity=quantity
            )
            event.available_seats-=quantity
            event.save()
            messages.success(
                request,
                'Booking successful!'
            )
        else:
            messages.error(
                request,
                'Not enough seats available.'
            )
        return redirect('dashboard')
    events=Event.objects.all()
    return render(
        request,
        'core/dashboard.html',
        {'events':events}
    )
@login_required
def bookings(request):
    user_bookings=Booking.objects.filter(
        user=request.user
    ).select_related('event')
    return render(
        request,
        'core/bookings.html',
        {'bookings': user_bookings}
    )
@login_required
def cancel_booking(request,booking_id):
    booking=Booking.objects.get(
        id=booking_id,
        user=request.user
    )
    event=booking.event
    event.available_seats+=booking.quantity
    event.save()
    booking.delete()
    messages.success(
        request,
        'Booking cancelled successfully.'
    )
    return redirect('bookings')