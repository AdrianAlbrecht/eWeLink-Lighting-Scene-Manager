import copy
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect

class Headers(dict):
    def __init__(self, appid: str, nonce: str, token: str, post: bool = False):
        super().__init__()
        if post:
            self["Content-Type"] = "application/json"
        self["X-CK-Appid"] = appid
        self["X-CK-Nonce"] = nonce
        self["Authorization"] = f"Bearer {token}"
        self["Host"] = "eu-apia.coolkit.cc"
        

@api_view(['GET'])
def authorize_app(request, pk):
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response("Cannot find configuration for your app", status=status.HTTP_404_NOT_FOUND)
        
        return redirect(config.createCodeLink())
    
@api_view(['GET'])
def use_code(request, pk):
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response("Cannot find configuration for your app", status=status.HTTP_404_NOT_FOUND)
        
        code = request.GET.get('code')
        
        json = config.createToken(code)
        
        return Response(json)
    
@api_view(['GET'])
def refresh_tokens(request, pk):
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response("Cannot find configuration for your app", status=status.HTTP_404_NOT_FOUND)
        
        json = config.refreshTokens()
        
        return Response(json)
    
@api_view(['GET'])
def get_device_list(request, pk):
    url = "https://eu-apia.coolkit.cc/v2/device/thing"
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response("Cannot find configuration for your app", status=status.HTTP_404_NOT_FOUND)
        
        headers = Headers(config.appid, config.nonce, config.accessToken, False)
        try:
            response = requests.get(url, headers=headers)
        except:
            return Response("Cannot connect to server. Check your internet connection and try again.", status=status.HTTP_408_REQUEST_TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            return Response(data['data']['thingList'], status=status.HTTP_200_OK)
        else:
            return Response("Error:", response.status_code, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def get_device_status(request, pk, name):
    url = "https://eu-apia.coolkit.cc/v2/device/thing/status"
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response("Cannot find configuration for your app", status=status.HTTP_404_NOT_FOUND)
        
        try:
            device = Device.objects.get(name=name)
        except Device.DoesNotExist:
            return Response(f"Cannot find device with name {name}", status=status.HTTP_404_NOT_FOUND)
        
        headers = Headers(config.appid, config.nonce, config.accessToken, False)
        
        try:
            response = requests.get(url, params=device.get_payload(), headers=headers)
        except:
            return Response("Cannot connect to server. Check your internet connection and try again.", status=status.HTTP_408_REQUEST_TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            return Response(data['data']['params'], status=status.HTTP_200_OK)
        else:
            return Response("Error:", response.status_code, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def get_scene_list(request, pk):
    if request.method == 'GET':
        scenes = Scene.objects.all()
        serializer = SceneSerializer(scenes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_scene_details(request, pk, name):
    if request.method == 'GET':
        try:
            scene = Scene.objects.get(name=name)
        except Scene.DoesNotExist:
            return Response(f"Cannot find scene with name {name}", status=status.HTTP_404_NOT_FOUND)
        
        return Response(scene.create_payload(), status=status.HTTP_200_OK)
    
@api_view(['GET'])
def scene_activate(request, pk, name):
    url = "https://eu-apia.coolkit.cc/v2/device/thing/batch-status"
    if request.method == 'GET':
        try:
            config = Configuration.objects.get(pk=pk)
        except Configuration.DoesNotExist:
            return Response("Cannot find configuration for your app", status=status.HTTP_404_NOT_FOUND)
        
        try:
            scene = Scene.objects.get(name=name)
        except Scene.DoesNotExist:
            return Response(f"Cannot find scene with name {name}", status=status.HTTP_404_NOT_FOUND)
        
        headers = Headers(config.appid, config.nonce, config.accessToken, True)
        
        try:
            response = requests.post(url, json=scene.create_payload(), headers=headers)
        except:
            return Response("Cannot connect to server. Check your internet connection and try again.", status=status.HTTP_408_REQUEST_TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            if data['error'] == 0:
                return Response(f"Scene activated! :)", status=status.HTTP_200_OK)
            return Response(f"Error code: {data['error']}\nError message: {data['msg']}", status=status.HTTP_200_OK)
        else:
            return Response("Error:", response.status_code, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def create_scene(request, pk):
    if request.method == 'GET':
        example = {"name": "bulb_detect",
        "device": [
            "1001f4bec4 <= Light GP",
            "1001f6e2b9 <= Light 2",
            "1001f6ea62 <= Light 3",
            "1001f6ebe8 <= Light 1"
        ],
        "statuses": {
            "1001f6ebe8": {
                "switch": "on",
                "ltype": "white",
                "white": {
                    "br": 100,
                    "ct": 100
                }
            },
            "1001f6e2b9": {
                "switch": "on",
                "ltype": "color",
                "color": {
                    "br": 100,
                    "r": 255,
                    "g": 0,
                    "b": 0
                }
            },
            "1001f6ea62": {
                "switch": "on",
                "ltype": "color",
                "color": {
                    "br": 100,
                    "r": 0,
                    "g": 255,
                    "b": 0
                }
            },
            "1001f4bec4": {
                "switch": "on",
                "ltype": "color",
                "color": {
                    "br": 100,
                    "r": 0,
                    "g": 0,
                    "b": 255
                }
            }
        }}
        response = {
            "Message": "Create a new scene!! :)",
            "Example": example
        }
        return Response(response, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = SceneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def create_scene_form(request, pk):
    devices = Device.objects.all()
    url = 'http://localhost:8000/ewelink/' + str(pk) + '/scene_create_by_form/'
    if request.method == 'GET':
        return render(request, 'create_scene.html', {'devices': devices, 'url': url})

    elif request.method == "POST":
        serializer = SceneSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect(f'http://localhost:8000/ewelink/{pk}/scene/{serializer.data["name"]}')
        data = copy.deepcopy(serializer.data)
        data['statuses'] = str(serializer.data['statuses']).replace("'", "\"")[1:-1]  
        return render(request, 'create_scene.html', {'form': data, 'devices': devices, 'url': url, 'response_message': serializer.errors})

@api_view(['GET','POST'])
def edit_scene_form(request, pk, name):
    devices = Device.objects.all()
    url = 'http://localhost:8000/ewelink/' + str(pk) + '/scene/' + name + '/edit/'
    try:
        scene = Scene.objects.get(name=name)
    except Scene.DoesNotExist:
        return Response(f"Cannot find scene with name {name}", status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SceneSerializer(scene)
        
        data = copy.deepcopy(serializer.data)
        data['statuses'] = str(serializer.data['statuses']).replace("'", "\"")[1:-1]  
        return render(request, 'edit_scene.html', {'devices': devices, 'url': url, 'form': data})
    
    elif request.method == "POST":
        serializer = SceneSerializer(scene, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect(f'http://localhost:8000/ewelink/{pk}/scene/{serializer.data["name"]}')
        data = copy.deepcopy(serializer.data)
        data['statuses'] = str(serializer.data['statuses']).replace("'", "\"")[1:-1]  
        return render(request, 'edit_scene.html', {'form': data, 'devices': devices, 'url': url, 'response_message': serializer.errors})
        