from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets


class DossierModelViewSet(viewsets.ModelViewSet):
    queryset = Dossier.objects.all()
    serializer_class = DosierSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer