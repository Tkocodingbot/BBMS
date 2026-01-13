
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .models import TimeSlot, Booking, Boardroom
from django.http import JsonResponse
from django.utils import timezone # type: ignore
import datetime
from datetime import date, timedelta



def get_time_slots(request):
    """AJAX view to get time slots for a specific date and boardroom"""
    date_str = request.GET.get('date')
    boardroom_id = request.GET.get('boardroom_id')
    
    if not date_str or not boardroom_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        boardroom = Boardroom.objects.get(id=boardroom_id)
    except (ValueError, Boardroom.DoesNotExist):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
    # Get or create time slots for the selected date and boardroom
    time_slots = []
    for slot_value, slot_display in TimeSlot.TIME_SLOTS:
        time_slot, created = TimeSlot.objects.get_or_create(
            date=selected_date,
            time_slot=slot_value,
            boardroom=boardroom,
            defaults={'is_booked': False}
        )
        
        time_slots.append({
            'id': time_slot.id,
            'time_slot': slot_display,
            'is_booked': time_slot.is_booked,
            'slot_value': slot_value,
        })
    
    return JsonResponse({
        'date': selected_date.strftime('%Y-%m-%d'),
        'boardroom': boardroom.name,
        'time_slots': time_slots
    })



@login_required
def book_time_slot(request, slot_id):
    """Book a specific time slot"""
    time_slot = get_object_or_404(TimeSlot, id=slot_id)
    
    if time_slot.is_booked:
        return JsonResponse({'error': 'This time slot is already booked'}, status=400)
    
    if request.method == 'POST':
        subject = request.POST.get('subject', 'Meeting')
        
        # Create booking
        booking = Booking.objects.create(
            subject=subject,
            time_slot=time_slot,
            user=request.user
        )
        
        # Mark time slot as booked
        time_slot.is_booked = True
        time_slot.save()
        
        return JsonResponse({'success': 'Booking confirmed'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



def calendar_view(request):

    boardrooms = Boardroom.objects.filter(available=True)
    
    # Get current date or selected date
    selected_date = request.GET.get('date')
    if selected_date:
        try:
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # Calculate previous and next dates for navigation
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)
    
    context = {
        'boardrooms': boardrooms,
        'selected_date': selected_date,
        'prev_date': prev_date,
        'next_date': next_date,
    }

    return render(request, 'BBMS/calendar.html')


@login_required
def create_booking_view(request):
    """View for creating a booking with subject"""
    if request.method == 'POST':
        slot_id = request.POST.get('slot_id')
        subject = request.POST.get('subject')
        
        time_slot = get_object_or_404(TimeSlot, id=slot_id)
        
        if time_slot.is_booked:
            return render(request, 'BBMS/error.html', {
                'error': 'This time slot is already booked'
            })
        
        # Create booking
        booking = Booking.objects.create(
            subject=subject,
            time_slot=time_slot,
            user=request.user
        )
        
        # Mark time slot as booked
        time_slot.is_booked = True
        time_slot.save()
        
        return render(request, 'BBMS/booking_success.html', {
            'booking': booking
        })
    
    return redirect('calendar_view')




    


