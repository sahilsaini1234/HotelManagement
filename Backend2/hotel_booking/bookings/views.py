# bookings/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Room, Booking
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
import json
from datetime import datetime
import pytz
from django.utils import timezone

 # Or your specific timezone

def convert_naive_to_aware(naive_datetime):
    return timezone.localize(naive_datetime)
def overlap_exists(room_id, start_time, end_time, exclude_booking_id=None):
    overlap_booking = Booking.objects.filter(
        room_id=room_id,
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    if exclude_booking_id:
        overlap_booking = overlap_booking.exclude(id=exclude_booking_id)
    
    return overlap_booking.exists()
@csrf_exempt
@require_http_methods(['GET','POST'])
def create_booking(request):
    print("sahil")
    data = json.loads(request.body.decode('utf-8'))
    user_email = data['user_email']
    room_id = data['room_number']
    start_time = parse_datetime(data['start_time'])
    end_time = parse_datetime(data['end_time'])
    print("sahil")
    room = Room.objects.get(id=room_id)
    print(type(room))
    print(room.availability)
    if not room.availability:
        return JsonResponse({'success': False, 'message': 'Room not available'}, status=400)

    if overlap_exists(room_id, start_time, end_time):
        return JsonResponse({'success': False, 'message': 'Overlapping booking exists.'}, status=400)

    duration_hours = (end_time - start_time).total_seconds() / 3600
    total_price = duration_hours * room.price_per_hour

    booking = Booking(user_email=user_email, room=room, start_time=start_time, end_time=end_time, total_price=total_price)
    booking.save()

    room.availability = False
    room.save()

    return JsonResponse({'success': True, 'message': 'Booking created successfully'})
@csrf_exempt
@require_http_methods(["PUT"])
def edit_booking(request, booking_id):
    data = json.loads(request.body.decode('utf-8'))
    user_email = data['user_email']
    start_time = parse_datetime(data['start_time'])
    end_time = parse_datetime(data['end_time'])

    booking = Booking.objects.get(id=booking_id)

    room_id = data['room_number']
    room = Room.objects.get(id=room_id)

    if overlap_exists(room_id, start_time, end_time, exclude_booking_id=booking_id):
        return JsonResponse({'success': False, 'message': 'Overlapping booking exists.'}, status=400)

    duration_hours = (end_time - start_time).total_seconds() / 3600
    total_price = duration_hours * room.price_per_hour

    booking.user_email = user_email
    booking.start_time = start_time
    booking.end_time = end_time
    booking.total_price = total_price
    booking.room = room
    booking.save()

    return JsonResponse({'success': True, 'message': 'Booking updated successfully'})
    
@csrf_exempt
@require_http_methods(["DELETE"])
def cancel_booking(request, booking_id):
    if request.method == 'DELETE':
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Booking not found.'}, status=404)

        room = booking.room
        current_time = timezone.now()  # Correct usage to get the current time with timezone awareness

        if booking.start_time > current_time + timedelta(hours=48):
            refund_amount = booking.total_price
        elif current_time + timedelta(hours=24) <= booking.start_time <= current_time + timedelta(hours=48):
            refund_amount = booking.total_price / 2
        else:
            refund_amount = 0.0

        room.availability = True
        room.save()
        booking.delete()

        return JsonResponse({'success': True, 'message': 'Booking canceled successfully', 'refund_amount': refund_amount})
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)

@csrf_exempt
@require_http_methods(["GET"])
def view_bookings(request):
    filters = request.GET
    query = Booking.objects.all()

    if 'room_type' in filters and filters['room_type']:
        room_type = filters['room_type']
        query = query.filter(room__room_type=room_type)

    if 'start_time' in filters and 'end_time' in filters and filters['start_time'] and filters['end_time']:
        start_time = parse_datetime(filters['start_time'])
        end_time = parse_datetime(filters['end_time'])
        query = query.filter(start_time__gte=start_time, end_time__lte=end_time)

    if 'user_email' in filters and filters['user_email']:
        user_email = filters['user_email']
        query = query.filter(user_email=user_email)

    bookings_list = list(query.values('id', 'user_email', 'room__room_type', 'start_time', 'end_time', 'total_price'))

    return JsonResponse({'bookings': bookings_list})
