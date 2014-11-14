#!/usr/bin/env python2
#docker pull hex29a/dvws-dvwa
#docker run dvws -d
## get dvws container id
#docker inspect --format '{{ .NetworkSettings.IPAddress }}' container_id
# pip install PySimpleSoap

from sys import path
path.insert(0,'..')
from ilwrathi import IdempotentAccessor
from suds.client import Client as SoapClient

from time import sleep

class DvwsIAC(IdempotentAccessor):

    def setup(self, ip):
        self.client = SoapClient('http://%s/%s' % (ip, self.wsdl_path))


class HelloIAC(DvwsIAC):
    wsdl_path = "webservices-standalone/ws-helloWorld.php?wsdl"
    

    def get_hello(self):
        return self.client.service.hello("asdf")


class CommandinjIAC(DvwsIAC):
    wsdl_path = "webservices-standalone/ws-commandinj.php?wsdl"


if __name__ == "__main__":
    from docker_demo import DockerIAC
    d = DockerIAC(client=docker.Client(
        base_url='unix://var/run/docker.sock', 
        version='1.3.0', 
        timeout=10))
    h = HelloIAC(d["container_ip")
    c = CommandinjIAC(d["container_ip")
