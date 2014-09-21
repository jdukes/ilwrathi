#!/usr/bin/env python
import json
from string import letters, digits
from random import randint, choice

from sys import path
path.insert(0,'..')
from ilwrath import Sac
from client import PetStoreClient


def _rnd_str(length):
    #shitty rand, don't use for anything but demo
    return ''.join(choice(letters + digits) for _ in range(length))

URL = "http://petstore.swagger.wordnik.com:80/api"

class PetSac(Sac):

    def __init__(self, name="petsac"):
        self.name = name
        self.client = PetStoreClient(URL)
        
    def get_pet(self):
        pet_d = {"id": randint(100, 500),
                 "category": {
                     "id": randint(100, 500),
                     "name": _rnd_str(5),
                 },
                 "name": _rnd_str(5),
                 "photoUrls": [
                     ""
                 ],
                 "tags": [
                     {
                         "id": 0,
                         "name": _rnd_str(5)
                     }
                 ],
                 "status": ""}
        resp = self.client.post_pet(pet_d)
        assert resp.status_code == 200, "shit broke"
        return pet_d

    def get_orderid(self):
        order_dict = {
            "id": randint(1,5),
            "petId": self["pet"]["id"],
            "quantity": randint(1,5),
            "status": "",
            "shipDate": ""
        }
        r = self.client.post_store_order(order_dict)
        assert r.status_code == 200, "shit fucked up"
        return order_dict
        
    def validate(self, key, value):
        if key == "pet":
            r = self.client.get_pet(value["id"])
            return r.status_code == 200
        if key == "orderid":
            r = self.client.get_store_order(value["id"])
        else:
            return True


#p = PetSac()
#p.client.delete_store_order(p["orderid"]["id"])
