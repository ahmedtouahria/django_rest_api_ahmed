from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status , generics,mixins
from .serializers import *
from rest_framework.views import APIView
from django.http import Http404
# 1 FBV function BASED view
# 1.1 LIST  & CREATE == GET & POST
@api_view(["GET","POST"])
def FBV_list(request):   
################ GET ####################
    
    #GET إذا جاء طلب من المستخدم من نوع  
    if request.method=="GET":
    # فإننا نعمل كويري من قاعدة البيانات حسب طلب المستخدم ونضعها في متغير    
        guests = Guest.objects.all()
    #JSON ثم نعمل سيريالايز لهذه البيانات الذي طلبها المستخدم ونحولها إلى     
        serializer = GuestSerializer(guests,many=True)
    #JSON و بعد ذلك نرد الإجابة ب     
        return Response(serializer.data)
######### POST ##################
    #POST إذا جاء طلب من المستخدم من نوع 
    elif request.method=="POST":
    # معناها المستخدم سيدخل بيانات في قاعدة البيانات لذلك سنضع بعض البروتوكولات 
    #JSON نقوم هنا بتحويل البيانات المراد إدخالها إلى     
        serializer = GuestSerializer(data = request.data)
        #ثم نتحقق من أن البيانات صحيحة و سليمة
        if serializer.is_valid():
            #إذا كانت سليمة سنحفظها في قاعدة البيانات
            serializer.save()
            #ثم نقوم بالإستجابة ببروتوكول 201
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        #إذا كانت غير صحيحة نقوم بالإستجابة ببروتوكول 400
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    
# 1.2 pk (UNIQUE) ==> GET  & PUT & DELETE
    
@api_view(["GET","PUT","DELETE"])
def FBV_pk(request , pk):  
    #pk إذا عمل المستخدم ريكوست على شيئ معين نرمز له ب  
    #نقوم أولا بتحقق اذا كان هاذ الشيئ موجود في قاعدة البيانات 
    try:
        guest = Guest.objects.get(pk=pk)
         #إذا كان غير موجود فسنرد له ب بروتوكول 404
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
######### GET unique ##################
    if request.method=="GET":
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
######### PUT == UPDATE ##################
    elif request.method=="PUT":
        serializer = GuestSerializer(guest , request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method=="DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#2 CBV class BASED view   
class CBV_list(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializers = GuestSerializer(guests,many=True)
        return Response(serializers.data)
    def post(self, request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        return Response(status=status.HTTP_400_BAD_REQUEST)  

class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk) 
        except Guest.DoesNotExist:
            raise Http404   
    def get(self, request, pk):
            guest = self.get_object(pk)
            serializer=GuestSerializer(guest)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self,request, pk):
           guest = self.get_object(pk)
           serializer=GuestSerializer(guest, request.data)
           if serializer.is_valide():
               serializer.save()
               return Response(serializer.data, status.HTTP_202_ACCEPTED)
           return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT )   
    
# 3 mixins
#Mixing list 3.1
# used for most programmmers because it easy and cleaned code
class mixins_list(mixins.CreateModelMixin,mixins.ListModelMixin,generics.GenericAPIView):
    # يسهلو من كتابة الكود يعني هم اختصروا الكثير من الأسطر Mixins
    #  json هم لي يحولو البيانات الى Generics 
     queryset = Guest.objects.all()
     serializer_class = GuestSerializer
    
     def get(self,request):
        return self.list(request)
     def post(self,request):
        return self.create(request)
class mixins_pk(mixins.RetrieveModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    # يسهلو من كتابة الكود يعني هم اختصروا الكثير من الأسطر Mixins
    #  json هم لي يحولو البيانات الى Generics 
     queryset = Guest.objects.all()
     serializer_class = GuestSerializer
    
     def get(self,request,pk):
        return self.retrieve(request)
    
     def put(self,request,pk):
        return self.update(request) 
    
     def delete(self,request,pk):
        return self.destroy(request)    