#!/usr/bin/env python2
# systemctl start docker

from sys import path
path.insert(0,'..')
from ilwrathi import IdempotentAccessor
import docker
from random import choice
from time import sleep


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
            r = self.client.create_container(self["container"]["Image"])
            self.client.start(r["Id"])
        return self.client.inspect_container(r["Id"])

    def check_live_container(self, val):
        newval = self.client.inspect_container(val["ID"])
        return val["State"]["Running"]

    def del_live_container(self):
        self.client.kill(self["live_container"]["ID"])

    def get_container_ip(self):
        return self["live_container"]['NetworkSettings']["IPAddress"]
        

        
# d = DockerIAC(client=docker.Client(base_url='unix://var/run/docker.sock', 
#                                    version='1.3.0', 
#                                    timeout=10))
