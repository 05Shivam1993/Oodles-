from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from TestApp.models import *
from django.http import QueryDict
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class LoginAPI(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        _data = request.data
        response_data = {"status_code":None, "message":None,"error_details":[]}
        username = _data.get("username")
        if not username:
            return Response({"message":"Please provide your username"},status=400)
        pwd = _data.get("password")
        if not pwd:
            return Response({"message":"Please provide your valid password"},status=400)
        email = _data.get("email")
        if not email:
            return Response({"message":"Please provide your email"},status=400)
        try:
            user = User.objects.get(username=username,email=email)
        except Exception:
            user = None
        if user:
             user = authenticate(request,username=username,password=pwd)
             if user is not None:
                 login(request,user)
                 if Token.objects.filter(user=user):
                     token = Token.objects.get(user=user)
                     response_data['token'] = token.key
                 else:
                    token = Token.objects.create(user=user)
                    response_data['token'] = token.key
                 response_data['status_code'] = status.HTTP_200_OK
                 response_data['message'] = "Login Successfull"
                 response_data['error_details'] = []
                 response = Response(response_data)
                 return response
             else:
                 response_data['status_code'] = status.HTTP_401_UNAUTHORIZED
                 response_data['message'] = "Login Unsuccesfull"
                 response_data['error_details'] = "Username already exist, Please provide your valid credential's'"
                 response = Response(response_data)
                 return response
        else:
            user = User(username=username,email=email)
            user.set_password(pwd)
            user.save()
            token = Token.objects.create(user=user)
            response_data['token'] = token.key
            response_data['status_code'] = status.HTTP_200_OK
            response_data['message'] = "Profile Created Successfull"
            response_data['error_details'] = []
            response = Response(response_data)
            return response

class ProfileAPI(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request):
        total_user = []
        _data = request.data
        user_qs = None
        if _data.get('username') and _data.get('key'):
            user_obj = User.objects.get(username=_data.get('username'))
            profile_obj = Profile.objects.get(profile_id=user_obj)
            total_friend = Friends.objects.filter(profile_id=profile_obj).values_list('name')
            if total_friend:
                user_total_friend = [i[0] for i in total_friend]
            user_qs = User.objects.all()
        elif _data.get('username'):
            user_qs = User.objects.filter(username=_data.get('username'))
        if user_qs:
            for user in user_qs:
                mutual_friend = 0
                response_data = {"profile_data":dict(),"company_address":dict(),"permanent_address":dict()}
                try:
                    profile = Profile.objects.get(profile_id = user)
                except:
                    profile = None
                try:
                    com_obj = CompanyAddress.objects.get(user_id = profile)
                except:
                    com_obj = None
                try:
                    perm_obj = PermanentAddress.objects.get(user_id = profile)
                except:
                    perm_obj = None
                try:
                    total_friend=Friends.objects.filter(profile_id=profile).values_list('name')
                    total_friend = [i[0] for i in total_friend]
                    for i in total_friend:
                        if i in user_total_friend:
                            mutual_friend += 1
                except:
                    mutual_friend = 0

                if profile:
                    response_data['profile_data']['name'] = profile.name
                    response_data['profile_data']['email'] = user.email
                    response_data['profile_data']['phone'] = profile.phone_no
                    response_data['profile_data']['gender'] = profile.gender
                    response_data['profile_data']['date_of_birth'] = profile.date_of_birth
                    response_data['profile_data']['profilepic'] = str(profile.profilepic)
                if com_obj:
                    response_data['company_address']['street_address'] = com_obj.street_address
                    response_data['company_address']['city']  = com_obj.city
                    response_data['company_address']['pincode'] = com_obj.pincode
                    response_data['company_address']['state'] = com_obj.state
                    response_data['company_address']['country'] = com_obj.country
                if perm_obj:
                    response_data['permanent_address']['street_address'] = perm_obj.street_address
                    response_data['permanent_address']['city']  = perm_obj.city
                    response_data['permanent_address']['pincode'] = perm_obj.pincode
                    response_data['permanent_address']['state'] = perm_obj.state
                    response_data['permanent_address']['country'] = perm_obj.country
                if user.username != _data.get('username'):
                    if mutual_friend:
                        response_data['profile_data']['mutual_friend'] = mutual_friend or 0
                else:
                    response_data['profile_data']['myprofile'] = "My Profile"
                total_user.append(response_data)
            response_data['status_code'] = status.HTTP_200_OK
            response_data['error_details'] = []
            response = Response(total_user)
            return response

    def put(self,request,pk=None):
        _data = request.data
        phone_no=_data.get('profile_update').get('phone_no')
        if phone_no:
            if len(phone_no) != 10 or phone_no.isnumeric() == False:
                return Response({"message":"Please provide your 10 digit phone number"},status=400)
        name = _data.get('profile_update').get('name')
        if name:
            if not name.isalpha():
                return Response({"message":"Name must contain atleast 4 characters"},status=400)
        gender = (_data.get('profile_update').get('gender'))
        if gender:
            if gender.lower() in ['male','female','other']:
                return Response({"message":"Gender must be Male or Female or Other"},status=400)
        pincode = _data.get('company_addr_update').get('pincode')
        if pincode:
            if pincode.isnumeric()==False:
                return Response({"message":"Pincode must be Integer"},status=400)
        city = _data.get('company_addr_update').get('city')
        if city:
            if not city.isalpha():
                return Response({"message":"City must be string"},status=400)
        state = _data.get('company_addr_update').get('state')
        if state:
            if not state.isalpha():
                return Response({"message":"State must be string"},status=400)
        country = _data.get('company_addr_update').get('pincode')
        if country:
            if not country.isalpha():
                return Response({"message":"Country must be string"},status=400)
        city = _data.get('permanent_addr_update').get('city')
        if city:
            if not city.isalpha():
                return Response({"message":"City must be string"},status=400)
        state = _data.get('permanent_addr_update').get('state')
        if state:
            if not state.isalpha():
                return Response({"message":"State must be string"},status=400)
        country = _data.get('permanent_addr_update').get('pincode')
        if country:
            if not country.isalpha():
                return Response({"message":"Country must be string"},status=400)
        pincode = _data.get('permanent_addr_update').get('pincode')
        if pincode:
            if pincode.isnumeric()==False:
                return Response({"message":"Pincode must be Integer"},status=400)
        response_data = {"status_code":None, "message":None,"error_details":[],"profile_detail":[],"company_addr":[],"permanent_addr":[]}
        if _data.get('username') == str(request.user):
            try:
                user = User.objects.get(username=_data.get('username'))
            except:
                user = None
            if user:
                if _data.get('profile_update'):
                     try:
                         profile = Profile.objects.get(profile_id = user)
                     except:
                         profile = None
                     if profile:
                        profile.name = _data['profile_update'].get('name') or profile.name
                        profile.phone_no = _data['profile_update'].get('phone_no') or profile.phone_no
                        profile.gender = _data['profile_update'].get('gender') or profile.gender
                        profile.date_of_birth = _data['profile_update'].get('date_of_birth') or profile.date_of_birth
                        profile.save()
                        if _data.get('company_addr_update'):
                             try:
                                 comp_obj = CompanyAddress.objects.get(user_id = profile)
                             except:
                                 comp_obj = None
                             if comp_obj:
                                comp_obj.street_address = _data['company_addr_update'].get('street_address') or comp_obj.street_address
                                comp_obj.state = _data['company_addr_update'].get('state') or comp_obj.state
                                comp_obj.city = _data['company_addr_update'].get('city') or comp_obj.city
                                comp_obj.pincode = _data['company_addr_update'].get('pincode') or comp_obj.pincode
                                comp_obj.save()
                        if _data.get('permanent_addr_update'):
                             try:
                                 perm_obj = PermanentAddress.objects.get(user_id = profile)
                             except:
                                 perm_obj = None
                             if perm_obj:
                                perm_obj.street_address = _data['permanent_addr_update'].get('street_address') or perm_obj.street_address
                                perm_obj.state = _data['permanent_addr_update'].get('state') or perm_obj.state
                                perm_obj.city = _data['permanent_addr_update'].get('city') or perm_obj.city
                                perm_obj.pincode = _data['permanent_addr_update'].get('pincode') or perm_obj.pincode
                                perm_obj.save()
                return Response({"message":"Profile Updated Successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Please provide your username"},status=400)

    def post(self,request):
        _data = request.data
        if not _data.get('username'):
            return Response({"message":"Please provide your username"},status=400)
        if not _data.get('friend_name').isalpha():
            return Response({"message":"Friend name must be in string"},status=400)
        if _data.get('username') == str(request.user):
            try:
                user = User.objects.get(username=_data.get('username'))
                profile = Profile.objects.get(profile_id = user)
                friend_obj = Friends.objects.create(profile_id=profile,name=_data.get("friend_name"))
            except:
                print(e)
            return Response({"message":"Friend added successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Please provide your username and friend name"},status=400)


    def delete(self,request):
        _data = request.data
        if not _data.get('username'):
            return Response({"message":"Please provide your username"},status=400)
        if not _data.get('friend_name'):
            return Response({"message":"Please provide your friend name"},status=400)
        if _data.get('username') == str(request.user):
            try:
                user = User.objects.get(username=_data.get('username'))
                profile = Profile.objects.get(profile_id = user)
                friend_obj = Friends.objects.get(profile_id=profile,name=_data.get("name"))
                friend_obj.delete()
            except:
                return Resposne({"message":"There is some issue"},status=400)
            return Response({"message":"Friend deleted successfully"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Please provide your username and friend name"},status=400)

class LogoutAPI(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"success": ("Successfully logged out.")},
                        status=status.HTTP_200_OK)
        except:
            return Response({"message":"There is some issue"},status=400)
