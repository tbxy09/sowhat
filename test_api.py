import os
from settings import *
# from tencent_cloud_api import updataIngress,getPolicyset,describeIns
# from tencent_cloud_api import updataIngress,getPolicyset,describeIns
import sys

def setup_tencent_instance():

    from tencentcloud.common import credential
    from tencent_cloud_api import updataIngress,getPolicyset,describeIns

    cred = credential.Credential(
#                                  django_settings.TC_SECRET_ID,
#                                  django_settings.TC_SECRET_KEY
                                 os.getenv('TENCENTCLOUD_SECRET_ID'),
                                 os.getenv('TENCENTCLOUD_SECRET_KEY')
                                )

    # return a instance
    # instance=describeIns(cred)
    instance = updataIngress(cred)
    # instance = getPolicyset(cred)

    # adding to the host list,this is the ip address
    # host = instance.public_dns_name
    # env.host_string = host
    # print(instance)

def setup_aliyun_instance():

    from aliyun_cloud_api import describeIns,describeSec,modifySec

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]
    print(cred)

    # instance=describeIns(*cred)
    # describeSec(*cred)
    modifySec(*cred)


if __name__=="__main__":
    # setup_tencent_instance()
    setup_aliyun_instance()
    # print(sys.stdout.read())

