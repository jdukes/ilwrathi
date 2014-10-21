#!/usr/bin/env python2
from sys import path
path.insert(0,'..')
from ilwrathi import IdempotentAccessor
import docker
from random import choice


class DockerIAC(IdempotentAccessor):
    
    def __init__(self, client):
        self.client = client
        self.name = "docker"
        self.image_search = 'hex29a'

    def get_image(self):
        #don't want to just run anyone's shit
        img = choice(self.client.search(self.image_search))
        self.client.pull(img["name"])
        return img["name"]

    def check_image(self, val):
        return bool(self.client.images(name=val))

    def del_image(self):
        self.client.remove_image(self["image"])

    def get_container(self):
        container = self.client.create_container(self["image"])
        return self.client.inspect_container(container["Id"])

    def check_container(self, val):
        try:
            newval = self.client.inspect_container(val["ID"])
        except docker.APIError:
            return False
        return val == newval
    
    def del_container(self):
        if self["container"]["State"]["Running"]:
            self.client.kill(self["container"]["ID"])
        self.client.remove_container(self["container"]["ID"])
        
    def get_live_container(self):
        if not self["container"]["State"]["Running"]:
            self.client.start(self["container"]["ID"])
        return self.client.inspect_container(self["container"]["ID"])

    def check_live_container(self, val):
        newval = self.client.inspect_container(val["ID"])
        return val == newval and val["State"]["Running"] 

    def del_live_container(self):
        self.client.kill(self["live_container"]["ID"])

    def get_container_ip(self):
        return self["live_container"]['NetworkSettings']["IPAddress"]
        

        
d = DockerIAC(client=docker.Client(base_url='unix://var/run/docker.sock', 
                                   version='1.3.0', 
                                   timeout=10))
