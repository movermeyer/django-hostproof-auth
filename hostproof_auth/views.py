from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from hostproof_auth.models import *

import json
import rsa

@csrf_exempt
@require_POST
def register(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    encrypted_challenge = request.POST.get('encrypted_challenge')
    challenge = request.POST.get('challenge')
    if username and email and encrypted_challenge and challenge:
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            return HttpResponse(status=409, content="Account Already Exists")
        user = User.objects.create_user(username=username,
                                        email=email,
                                        encrypted_challenge=encrypted_challenge,
                                        challenge=challenge)
        return HttpResponse()
    else:
        return HttpResponseBadRequest('Invalid or missing parameters')

@csrf_exempt
def challenge(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                return HttpResponse(json.dumps({
                    'encrypted_challenge' : user.encrypted_challenge,
                }))
            except User.DoesNotExist:
                return HttpResponseNotFound('Account Not Found')
        else:
            return HttpResponseBadRequest('Invalid or missing parameters')
    elif request.method == 'POST':
        username = request.POST.get('username')
        challenge = request.POST.get('challenge')
        if username and challenge:
            user = authenticate(username=username, challenge=challenge)
            if user:
                login(request, user)
                (pubkey, privkey) = rsa.newkeys(512)
                request.session['rsa_private'] = privkey.save_pkcs1()
                return HttpResponse(json.dumps({
                    'rsa_public' : pubkey.save_pkcs1(),
                }))
            else:
                return HttpResponse(status=403, content='Bad Credentials')
        else:
            return HttpResponseBadRequest('Invalid or missing parameters')
    else:
        return HttpResponseNotAllowed()
