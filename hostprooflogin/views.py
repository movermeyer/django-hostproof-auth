from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from hostprooflogin.models import *

@csrf_exempt
@require_POST
def register(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    encrypted_challenge = request.POST.get('encrypted_challenge')
    decrypted_challenge = request.POST.get('decrypted_challenge')
    if username and email and encrypted_challenge and decrypted_challenge:
        if User.objects.filter(username=username).exists():
            return HttpResponse(status=409, content="Account Already Exists")
        user = User.objects.create_user(username=username,
                                        email=email,
                                        encrypted_challenge=encrypted_challenge,
                                        decrypted_challenge=decrypted_challenge)
        return HttpResponse()

    else:
        return HttpResponseBadRequest('Invalid or missing parameters')
