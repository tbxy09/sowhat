from invoke import task
# from fabric.contrib import django
from settings import *
from util import taskinfo,taskdebug
import tempfile
cache_file='cache_ip'
cache_inst_file='cache_inst'
import json.tool as jsonprint

@task
def get_ip(c):
    # ret=c.run('curl ipinfo.io/ip').stdout.strip()
    ret=c.run('curl ip.cip.cc ').stdout.strip()

    # with tempfile.NamedTemporaryFile() as input_file:
    with open(cache_file,'wb') as input_file:
        input_file.write(ret.encode())
        # cache_file=input_file.name

    ret=c.run('cat {}'.format(cache_file))

    # ret=c.run('curl ipinfo.io/ip').stdout.strip()
    # ret=c.run('whence -v curl').stdout.strip()
    # print(ret)

@task
def show_platform(c):
    uname = c.run("uname -s").stdout.strip()
    print(uname)
    if uname == 'Darwin':
        print("You paid the Apple tax!")
    elif uname == 'Linux':
        print("Year of Linux on the desktop!")

def update_hosts(c):

    from aliyun_cloud_api import describeIns

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]

    inst=describeIns(*cred)
    inst_focus=inst.Instances.Instance[0]
    Status=inst_focus.InstanceId,inst_focus.Status
    IpAddress= inst_focus.PublicIpAddress['IpAddress'][0]

    with open('/etc/hosts','ab') as io:
       io.write('{} aliyun_host'.format(IpAddress).encode())

    taskdebug(inst_focus)
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.Status))
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.PublicIpAddress['IpAddress'][0]))

@task
def des_aliIns(c):

    from aliyun_cloud_api import describeIns

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]

    inst=describeIns(*cred)
    inst_focus=inst.Instances.Instance[0]
    Status=inst_focus.InstanceId,inst_focus.Status
    # IpAddress= inst_focus.PublicIpAddress['IpAddress'][0]

    taskdebug('save the InstanceId')

    with open(cache_inst_file,'wb') as input_file:
        input_file.write(inst_focus.InstanceId.encode())


    taskdebug(inst_focus)
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.Status))
    # taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.PublicIpAddress['IpAddress'][0]))

@task
def des_aliIns_ip(c):

    from aliyun_cloud_api import describeIns

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]

    inst=describeIns(*cred)
    inst_focus=inst.Instances.Instance[0]
    Status=inst_focus.InstanceId,inst_focus.Status
    IpAddress= inst_focus.PublicIpAddress['IpAddress'][0]

    taskdebug(inst_focus)
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.Status))
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.PublicIpAddress['IpAddress'][0]))

@task
def update_aliIngress(c):

    from aliyun_cloud_api import modifySec,describeSec
    # ret=c.run('curl ipinfo.io/ip').stdout.strip()

    with open(cache_file,'rb') as input_file:
        host_ip=input_file.read().decode()
    taskinfo(host_ip)

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]


    resp = describeSec(*cred)

    taskinfo(host_ip==resp.Permissions.Permission[0].SourceCidrIp)

    if host_ip is not resp.Permissions.Permission[0].SourceCidrIp:
        taskinfo('need to update the ip address')
        modifySec(host_ip,*cred)

    resp = describeSec(*cred)

    taskinfo(resp.Permissions.Permission[0].SourceCidrIp)
    taskinfo(host_ip==resp.Permissions.Permission[0].SourceCidrIp)

    # taskinfo(resp.Permissions.Permission[0].SourceCidrIp)

@task
def get_aliIngress(c):

    from aliyun_cloud_api import describeIns,describeSec,modifySec
    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]

    resp = describeSec(*cred)
    taskinfo(resp.Permissions.Permission[0].SourceCidrIp)

@task
def des_tcIns(c):

    from tencentcloud.common import credential
    from tencent_cloud_api import updateIngress,getPolicyset,describeIns

    cred = credential.Credential(
                                 # django_settings.TC_SECRET_ID,
                                 # django_settings.TC_SECRET_KEY
                                 os.getenv('TENCENTCLOUD_SECRET_ID'),
                                 os.getenv('TENCENTCLOUD_SECRET_KEY')
                                )

    # return a instance
    inst = describeIns(cred)
    # instance = updataIngress(cred)
    taskinfo("the TotalCount of Inst: {}".format(inst.TotalCount))
    # taskinfo("InstanceId of Inst: {}".format(inst.Instances.Instance.InstanceId))

    # adding to the host list,this is the ip address
    # host = instance.public_dns_name
    # env.host_string = host

@task
def update_tcIngress(c):

    from tencentcloud.common import credential
    from tencent_cloud_api import updateIngress,getPolicyset,describeIns

    # TODO using a cache file to store the ip, but the ip must updated daily
    # ret=c.run('curl ipinfo.io/ip').stdout.strip()
    with open(cache_file,'rb') as input_file:
        host_ip=input_file.read()
        # taskinfo(host_ip)

    cred = credential.Credential(
                                 # django_settings.TC_SECRET_ID,
                                 # django_settings.TC_SECRET_KEY
                                 os.getenv('TENCENTCLOUD_SECRET_ID'),
                                 os.getenv('TENCENTCLOUD_SECRET_KEY')
                                )

    inst = updateIngress(cred,host_ip)
    # taskinfo("the TotalCount of Inst: {}".format(inst.TotalCount))

    # adding to the host list,this is the ip address
    # host = instance.public_dns_name
    # env.host_string = host

@task
def get_tcIngress(c):

    from tencentcloud.common import credential
    from tencent_cloud_api import updateIngress,getPolicyset,describeIns

    cred = credential.Credential(
                                 # django_settings.TC_SECRET_ID,
                                 # django_settings.TC_SECRET_KEY
                                 os.getenv('TENCENTCLOUD_SECRET_ID'),
                                 os.getenv('TENCENTCLOUD_SECRET_KEY')
                                )

    inst = getPolicyset(cred)
    # taskinfo("the TotalCount of Inst: {}".format(inst.TotalCount))
    taskinfo("The Ingress IP Address of Security Group {}".format(inst.SecurityGroupPolicySet.Ingress[3].CidrBlock))
    taskinfo("The Version of Security Group {}".format(inst.SecurityGroupPolicySet.Version))

    # adding to the host list,this is the ip address
    # host = instance.public_dns_name
    # env.host_string = host

@task
def start_aliIns(c):

    from aliyun_cloud_api import startstopInst,describeIns

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]

    with open(cache_inst_file,'rb') as file_input:
        inst_id=file_input.read().decode()

    if not inst_id:
        taskdebug('empty inst_id')
        return

    startstopInst(inst_id,True,*cred)
    inst=describeIns(*cred)

    inst_focus=inst.Instances.Instance[0]
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.Status))

@task
def stop_aliIns(c):

    from aliyun_cloud_api import startstopInst,describeIns

    cred=[os.getenv('ALIYUN_SECRET_ID'),
          os.getenv('ALIYUN_SECRET_KEY')]

    with open(cache_inst_file,'rb') as file_input:
        inst_id=file_input.read().decode()

    if not inst_id:
        taskdebug('empty inst_id')
        return

    startstopInst(inst_id,False,*cred)
    inst=describeIns(*cred)

    inst_focus=inst.Instances.Instance[0]
    taskinfo("Inst: {0}:{1}".format(inst_focus.InstanceId,inst_focus.Status))
