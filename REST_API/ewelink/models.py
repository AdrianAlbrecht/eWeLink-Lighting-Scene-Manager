import json
import random
import string
import time
import hashlib
import hmac
import base64
from django.db import models
import requests

class Configuration(models.Model):
    state = models.CharField(max_length=8, default=''.join(random.choices(string.ascii_letters + string.digits, k=8)), null = False, blank = False)
    nonce = models.CharField(max_length=8, default=''.join(random.choices(string.ascii_letters + string.digits, k=8)), null = False, blank = False)     
    appid = models.CharField(max_length=40, null = False, blank = False)                                                                               
    secret = models.CharField(max_length=40, null = False, blank = False)                                                                               
    redirect_url = models.CharField(max_length=200, null = False, blank = False)                                                                        
    grant_type = models.CharField(max_length=80, default = "authorization_code", null = False, blank = False)                                           
    accessToken = models.CharField(max_length=200, null = True, blank = True)
    refreshToken = models.CharField(max_length=200, null = True, blank = True)
    
    def _makeSign(self, key, message):
        return (base64.b64encode(hmac.new(key.encode(), message.encode(), digestmod=hashlib.sha256).digest())).decode()
        
    def createCodeLink(self):
        timestamp = int(time.time() * 1000)  # milisekundy
        sign = self._makeSign(self.secret,f'{self.appid}_{timestamp}')

        # Uzupełnianie URL
        url = f"https://c2ccdn.coolkit.cc/oauth/index.html?state={self.state}&clientId={self.appid}&authorization={sign}&seq={timestamp}&redirectUrl={self.redirect_url}&nonce={self.nonce}&grantType={self.grant_type}&showQRCode=false"

        # Wysyłanie żądania GET
        response = requests.get(url)
        return response.url
    
    def createToken(self, code):
        payload = {
            "code": code,
            "redirectUrl": self.redirect_url,
            "grantType": self.grant_type
        }
        
        message = json.dumps(payload)
        sign = self._makeSign(key=self.secret, message=message)
        
        url = "https://eu-apia.coolkit.cc/v2/user/oauth/token"
        headers = {
            "Content-Type": "application/json",
            "X-CK-Appid": self.appid,  
            "X-CK-Nonce": self.nonce,  
            "Authorization": f"Sign {sign}",  
            "Host": "eu-apia.coolkit.cc"
        }

        response = requests.post(url, json=payload, headers=headers)
        
        self.accessToken = response.json()['data']["accessToken"]
        self.refreshToken = response.json()['data']["refreshToken"]
        
        self.save()
        
        return response.json()
        
    def refreshTokens(self):
        url = "https://eu-apia.coolkit.cc/v2/user/refresh"
        headers = {
            "Content-Type": "application/json",
            "X-CK-Appid": self.appid,  
            "X-CK-Nonce": self.nonce,  
            "Authorization": f"Bearer {self.accessToken}",  
            "Host": "eu-apia.coolkit.cc"
        }

        payload = {
            "rt": self.refreshToken,
        }

        response_rt = requests.post(url, json=payload, headers=headers)

        self.accessToken = response_rt.json()['data']["at"]
        self.refreshToken = response_rt.json()['data']["rt"]
        
        self.save()
        
        return response_rt.json()
        
    def __str__(self):
        return self.appid
     
              
class Device(models.Model):
    TYPE_CHOICES = [
        (1, 'Device'),
        (2, 'Group'),
    ]
    
    name = models.CharField(max_length=100, blank= False, null = False, default=''.join(random.choices(string.ascii_letters + string.digits, k=16)))
    id = models.CharField(max_length=20, blank= False, null = False, primary_key=True)
    type = models.IntegerField(choices=TYPE_CHOICES, blank= False, null = False, default=1)
    
    def get_payload(self, params=None):
        payload = {
            "id": self.id,     
            "type" : self.type              
        }
        if params:
            payload["params"] = params
        return payload            
    
    def __str__(self):
        return self.name
    
class Scene(models.Model):
    name = models.CharField(max_length=100, blank= False, null= False, unique=True)
    device = models.ManyToManyField(Device)
    statuses = models.JSONField(default=list)
    
    def create_payload(self):          
        thing_list = [
            device.get_payload(params=self.statuses[device.id]) for device in self.device.all()
        ]
        return {
            "thingList": thing_list,
            "timeout": 0
        }
        
    def __str__(self):
        return self.name
    