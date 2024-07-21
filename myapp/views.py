# myapp/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import MyUser
from .serializers import UserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserCode, AttendanceData

class UserCreate(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserLogin(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        UserID = request.data.get("UserID")
        print("UserID", UserID)
        password = request.data.get("password")
        print("password", password)
        user = authenticate(UserID=UserID, password=password)
        print("user", user)
        if user:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({"token": token})
        else:
            return Response({"error": "Invalid Credentials"}, status=400)

@csrf_exempt
def save_code(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('userID')
        code = data.get('code')

        if user_id and code:
            UserCode.objects.create(user_id=user_id, code=code)
            return JsonResponse({'message': 'Code saved successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('userID')
        qr_code = data.get('qrCode')

        if not user_id or not qr_code:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        # Check if the QR code exists in UserCode
        if UserCode.objects.filter(code=qr_code).exists():
            # Check if there is an existing document with the QR code
            attendance, created = AttendanceData.objects.get_or_create(qr_code=qr_code)
            if user_id not in attendance.user_ids:
                attendance.user_ids.append(user_id)
                attendance.save()
            return JsonResponse({'message': 'Attendance saved successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid QR code'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)