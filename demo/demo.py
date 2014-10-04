#!/usr/bin/env python
from sys import path
path.insert(0,'..')
from ilwrathi import IdempotentAccessor
from client import PetStoreClient
from random import randint

try:
    import rstr
except ImportError:
    print "easy_install rstr"
    raise

URL = "http://petstore.swagger.wordnik.com:80/api"

class PetItempotentAccessor(IdempotentAccessor):

    def _setup(self, name="petItempotentAccessor"):
        self.client = PetStoreClient(URL)
        
    def get_pet(self):
        pet_d = {"id": randint(100, 500),
                 "category": {
                     "id": randint(100, 500),
                     "name": rstr.letters(5),
                 },
                 "name": rstr.letters(5),
                 "photoUrls": [
                     ""
                 ],
                 "tags": [
                     {
                         "id": 0,
                         "name": rstr.letters(5)
                     }
                 ],
                 "status": ""}
        resp = self.client.post_pet(pet_d)
        assert resp.status_code == 200, "shit broke"
        return pet_d

    def del_pet(self):
        resp = self.client.delete_pet(self["pet"]["id"])
        assert resp.status_code == 200, "shit broke"

    def set_pet(self, value):
        self.client.put_pet(value)
        return value
        
    def get_order(self):
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
        
    def del_order(self):
        resp = self.client.delete_order(self["order"]["id"])
        assert resp.status_code == 200, "shit broke"

    def set_order(self, value):
        self.client.put_order(value)
        
    def check_pet(self, value):
        r = self.client.get_pet(value["id"])
        return r.status_code == 200

    def check_order(self, value):
        r = self.client.get_store_order(value["id"])
        return r.status_code == 200

#p = PetItempotentAccessor()
#p.client.delete_store_order(p["order"]["id"])
