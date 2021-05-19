from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .services import mailing
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=(
        ('common','common'),
        ('warrior','warrior')
    ),write_only=True)
    full_name = serializers.CharField(write_only=True)
    image = serializers.ImageField(write_only=True)
    date_birth = serializers.DateField(write_only=True)
    gender = serializers.ChoiceField(choices=(
        ('M', 'M'),
        ('F', 'F')
    ),write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','check_password',
                  'full_name','date_birth','gender','image','user_type']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        image = validated_data.pop('image')
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        full_name = validated_data.pop('full_name')
        date_birth = validated_data.pop('date_birth')
        gender = validated_data.pop('gender')
        user = User.objects.create(**validated_data)
        if password != check_password:
            raise ValidationError("Passwords don't match")
        user.set_password(password)
        if user_type == 'warrior':
            user.is_active = False
            group = Group.objects.get(name='sergeant')
            user.groups.add(group)
            mailing(user.username)
        user.save()
        Dossier.objects.create(full_name=full_name,date_birth=date_birth,gender=gender,image=image,user=user)
        return user


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['id','mark']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school_name']


class WarcraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warcraft
        fields = ['id', 'military_area']

class DosierSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)
    schools = EducationSerializer(many=True)
    war_crfts = WarcraftSerializer(many=True)

    class Meta:
        model = Dossier
        fields = ['id','full_name','image','user','cars','schools','war_crfts','date_birth']

    def create(self, validated_data):
        cars_data = validated_data.pop('cars')
        schools_data = validated_data.pop('schools')
        warcrafts_data = validated_data.pop('war_crfts')
        dossier = Dossier.objects.create(**validated_data)
        for car in cars_data:
            Car.objects.create(dossier=dossier,**car)
        for school in schools_data:
            Education.objects.create(dossier=dossier,**school)
        for wc in warcrafts_data:
            Warcraft.objects.create(dossier=dossier,**wc)
        return dossier
