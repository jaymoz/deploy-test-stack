from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK,HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .serializers import BookingsSerializer,ParkingSpaceSerializer, UpdateBookingsSerializer
from parking.models import Bookings, Parking_Space
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, BasePermission, SAFE_METHODS
from rest_framework import generics
from rest_framework.authtoken.models import Token
from .decorators import allowed_users
from parking.views import create_booking_number
from rest_framework import permissions
import json
from parking.views import get_datetime
from rest_framework import serializers
from rest_framework import generics
from copy import deepcopy
from django.forms.models import model_to_dict
from django.core import serializers as core_serializers


class   AdminManagerPermission(permissions.BasePermission):
    message = "You are not authorized to view this page"

    def has_permission(self, request, view):
        allowed_roles = ["Manager"]
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group in allowed_roles or request.user.is_superuser:
            return True
        else:
            return False

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Api_parking_space(request):
    spaces = Parking_Space.objects.all()
    serializer = ParkingSpaceSerializer(spaces, many=True)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AdminManagerPermission,))
def Api_create_space(request):
    serializer = ParkingSpaceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['PUT'])
@permission_classes((AdminManagerPermission,))
def Api_update_parking_space(request, pk):
    space = get_object_or_404(Parking_Space, id=pk)
    serializer = ParkingSpaceSerializer(instance=space, data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((AdminManagerPermission,))
def Api_delete_parking_space(request, pk):
    space = get_object_or_404(request, pk)
    space.delete()
    return Response("Parking space has been deleted", status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((AdminManagerPermission,))
def Api_all_bookings(request):
    bookings = Bookings.objects.all()
    serializer = BookingsSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def Api_book_parking_space(request, pk):
    park = get_object_or_404(Parking_Space, id=pk)
    no = create_booking_number()
    serializer_data = deepcopy(request.data)
    serializer_data['owner'] = request.user.id
    serializer_data['ticket'] = no
    serializer_data['is_booked'] = True
    serializer_data['parking_space'] = park.id
    serializer = BookingsSerializer(data=serializer_data)
    if serializer.is_valid():
        if park.ft_is_available():
            start = str(serializer.validated_data['start_period'])
            end = str(serializer.validated_data['end_period'])
            if ((get_datetime(start) >= timezone.now()) and (timezone.now() < get_datetime(end)) and (get_datetime(start) < get_datetime(end))):
                serializer.save()
                park.no_of_spaces = park.ft_remove_space()
                park.save()
            else:
                return Response("Date fields are invalid")
        else:
            return Response("Sorry there are currently no spaces available")
    else:
        return Response(serializer.errors)
    return Response(serializer.data, HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AdminManagerPermission,))
def Api_update_booking(request, pk):
    booking = get_object_or_404(Bookings, id=pk)
    serializer = UpdateBookingsSerializer(instance=booking, data=request.data)
    if serializer.is_valid():
        start = str(serializer.validated_data['start_period'])
        end = str(serializer.validated_data['end_period'])
        if ((get_datetime(start) >= timezone.now()) and (timezone.now() < get_datetime(end)) and (get_datetime(start) < get_datetime(end))):
            serializer.save()
        else:
            return Response("Date fields are invalid")
    else:
        return Response(serializer.errors)
    return Response(serializer.data, HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes((AdminManagerPermission,))
def Api_cancel_booking(request, pk):
    booking = get_object_or_404(Bookings, id=pk)
    park = get_object_or_404(Parking_Space, id=booking.parking_space.id)
    park.no_of_spaces = park.ft_add_space()
    park.save()
    booking.is_booked = False
    booking.save()
    return Response("Booking has been cancelled", HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Api_get_booking_detail(request, pk):
    user_booking = Bookings.objects.filter(id=pk, owner=request.user)
    serializer = BookingsSerializer(user_booking, many=True)
    return Response(serializer.data, HTTP_200_OK)