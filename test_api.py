import os
from settings import *
from tencent_cloud_api import updataIngress,getPolicyset,describeIns
import sys

def setup_tencent_instance():
    from tencentcloud.common import credential
    cred = credential.Credential(
#                                  django_settings.TC_SECRET_ID,
#                                  django_settings.TC_SECRET_KEY
                                 os.getenv('TENCENTCLOUD_SECRET_ID'),
                                 os.getenv('TENCENTCLOUD_SECRET_KEY')
                                )
    # return a instance
    instance=describeIns(cred)
    # instance = updataIngress(cred)
    # instance = getPolicyset(cred)

    # adding to the host list,this is the ip address
    # host = instance.public_dns_name
    # env.host_string = host
    # print(instance)
if __name__=="__main__":
    setup_tencent_instance()
    # print(sys.stdout.read())

