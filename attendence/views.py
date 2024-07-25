from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def create_user(request):
    response = {}
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        response['message'] = 'User created successfully'
        response['status'] = '201'
        return Response(response)
    response['message'] = serializers.errors
    response['status'] = '404'
    return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_shift(request):
    response = {}
    if request.user.role != 'manager':
        response['message'] = 'Only managers can create a shifts'
        response['status'] = '400'
        return Response(response)
    serializer = ShiftSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response['message'] = 'Shift created successfully'
        response['data'] = serializers.data
        response['status'] = '201'
        return Response(response)
    
    response['message'] = serializer.errors
    response['status'] = '400'
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_roster(request):
    response = {}
    if request.user.role != 'manager':
        response['message'] ='Only managers can view the roster'
        response['status'] = '400'
        return Response(response)
    
    staff_members = CustomUser.objects.filter(role='staff')
    serializer = CustomUserSerializer(staff_members, many=True)
    response['data'] = serializer.data
    response['status'] = '200'
    return Response(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_shifts(request):
    response= {}
    if request.user.role == 'staff':
        shifts = Shift.objects.filter(staff=request.user)
    elif request.user.role == 'manager':
        shifts = Shift.objects.all()
    else:
        response['message'] = 'Unauthorized access'
        response['status'] = '403'
        return Response(response)
    

    serializer = ShiftSerializer(shifts, many=True)
    response['data'] = serializer.data
    response['status'] = '200'
    return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance(request):
    response = {}
    if request.user.role != 'staff':
        response['message'] = 'Only staff can mark attendance'
        response['status'] = '400'
        return Response(response)
    
    
    shift_id = request.data.get('shift')
    staff_id = request.user.id
    image = request.FILES.get('image')
    
    try:
        shift = Shift.objects.get(id=shift_id, staff_id=staff_id)
    except Shift.DoesNotExist:
        response['message'] = 'Shift not found'
        response['status'] = '404'
        return Response(response)
    
    
    now = timezone.now()
    shift_start = timezone.make_aware(datetime.combine(now.date(), shift.start_time), timezone.get_current_timezone())
    shift_end = timezone.make_aware(datetime.combine(now.date(), shift.end_time), timezone.get_current_timezone())
    
    
    if shift_start <= now <= shift_end + timedelta(hours=1):
        attendance = Attendance(staff_id=staff_id, shift_id=shift_id, image=image)
        attendance.save()
        response['message'] = 'Attendance marked successfully'
        response['status'] = '201'
        return Response(response)
    
    else:
        response['message'] = 'Attendance not within allowed time'
        response['status'] = '400'
        return Response(response)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_attendance(request):
    response ={}
    if request.user.role != 'manager':
        response['message'] = "Only managers can view attendance records"
        response['status'] = '400'
        return Response(response)
    attendance_records = Attendance.objects.all()
    serializer = AttendanceSerializer(attendance_records, many=True)
    response['attendance'] = serializer.data 
    response['status'] = '200'
    return Response(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_weekly_off(request):
    response = {}
    if request.user.role != 'manager':
        response['message'] = "Only managers can set weekly offs"
        response['status'] = '400'
        return Response(response)   
    

    serializer = WeeklyOffSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response['status'] = '200'
        response['message'] = 'Weekly off days set successfully'
        return Response(response)
    
    response['message'] = serializer.errors
    response['status'] = '400'
    return Response(response)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    response = {}
    if request.user.role != 'manager':
        response['message'] = 'Only managers can update user details'
        response['status'] = '400'
        return Response(response)
    
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        response['message']  = 'User does not exist'
        response['status'] = '404'
        return Response(response)

    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response['message'] = 'user has been updated successfully'
        response['status'] = '200'
        return Response(response)
    
    response['message'] = serializer.errors
    response['status'] = '400'
    return Response(response)

    




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_shift_change(request):
    response = {}
    if request.user.role != 'staff':
        response['message'] = 'Only staff can request shift changes'
        response['status'] = '400'
        return Response(response)
    
    staff1 = request.user
    staff2_id = request.data.get('staff2_id')
    day = request.data.get('day')

    # Ensure the receiving staff exists and is a staff member
    staff2 = get_object_or_404(CustomUser, id=staff2_id, role='staff')

    # Ensure both staff members have shifts on the requested day
    try:
        shift1 = Shift.objects.get(staff=staff1, day=day)
        shift2 = Shift.objects.get(staff=staff2, day=day)
    except Shift.DoesNotExist:
        response['message'] = 'Shift does not exist'
        response['status'] = 404
        return Response(response)

    # Create shift change request
    serializer = ShiftChangeRequestSerializer(data={
        'staff1': staff1.id,
        'staff2': staff2.id,
        'day': day
    })
    if serializer.is_valid():
        serializer.save()
        response['message'] = 'Shift change request submitted successfully'
        response['status'] = '200'
        return Response(response)
    response['message'] = serializer.errors
    response['status'] =  '400'
    return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_shift_change(request):
    response = {}
    if request.user.role != 'manager':
        response['message'] = "Only managers can approve shift changes"
        response['status'] = '400'
        return Response(response)
    
    request_id = request.data.get('request_id')
    approve = request.data.get('approve')
    
    shift_change_request = get_object_or_404(ShiftChangeRequest, id=request_id)

    if approve:
        shift_change_request.status = 'approved'
        shift_change_request.save()

        # Update shifts for both staff members
        staff1_shift = Shift.objects.get(staff=shift_change_request.staff1, day=shift_change_request.day)
        staff2_shift = Shift.objects.get(staff=shift_change_request.staff2, day=shift_change_request.day)

        # Swap shifts
        staff1_shift, staff2_shift = staff2_shift, staff1_shift
        staff1_shift.save()
        staff2_shift.save()
        
    else:
        shift_change_request.status = 'rejected'
        shift_change_request.save()
    response['message'] = 'Shift change request processed successfully'
    response['status'] = '200' if approve else '400'
    return Response(response)
   




