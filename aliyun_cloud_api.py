#!/usr/bin/env python
#coding=utf-8

import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from util import apidebug,apiinfo
import json
from funtest.util.util import objectview


# def deserialize(param):

#     param=json.loads(param)
#     top = objectview(param)

#     permissions_param=top.Permissions
#     Permissions=objectview(permissions_param.copy())

#     if permissions_param.get('Permission') is not None:

#         Permissions.Permission=[]
#         for item in permissions_param.get('Permission'):
#             item=objectview(item)
#             Permissions.Permission.append(item)
#     # apidebug(Permissions.Permission[0])

#     top.Permissions=Permissions
#     return top

# # def util():
# #     Permission=[]
# #     Permission.append(objectview(param))


def describeIns(*key):

    def deserialize(param):

        param=json.loads(param)
        top = objectview(param)

        instances_param=top.Instances
        Instances=objectview(instances_param.copy())

        if instances_param.get('Instance') is not None:

            Instances.Instance=[]
            for item in instances_param.get('Instance'):
                item=objectview(item)
                Instances.Instance.append(item)
        # apidebug(Permissions.Permission[0])

        top.Instances=Instances
        return top

    apidebug(key)

    client = AcsClient(
                    key[0],
                    key[1],
                    'cn-beijing')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-05-26')
    request.set_action_name('DescribeInstances')

    resp_jsonByte = client.do_action_with_exception(request)

    if os.environ.get("API_JSON_INFO")=="1":
        apiinfo("Json Response")
        print(str(resp_jsonByte, encoding = 'utf-8'))

    resp_json=deserialize(resp_jsonByte.decode())
    return resp_json

def describeSec(*key):

    def deserialize(param):

        param=json.loads(param)
        top = objectview(param)

        permissions_param=top.Permissions
        Permissions=objectview(permissions_param.copy())

        if permissions_param.get('Permission') is not None:

            Permissions.Permission=[]
            for item in permissions_param.get('Permission'):
                item=objectview(item)
                Permissions.Permission.append(item)
        # apidebug(Permissions.Permission[0])

        top.Permissions=Permissions
        return top

# def util():
#     Permission=[]
#     Permission.append(objectview(param))
    # apidebug(key)

    client = AcsClient(
                    key[0],
                    key[1],
                    'cn-beijing')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-05-26')
    request.set_action_name('DescribeSecurityGroupAttribute')

    request.add_query_param('RegionId', 'cn-beijing')
    request.add_query_param('SecurityGroupId', 'sg-2zeiafyiu5nh8zsuy1u6')

    resp_jsonByte = client.do_action_with_exception(request)

    if os.environ.get("API_JSON_INFO")=="1":
        apiinfo("Json Response")
        print(str(resp_jsonByte, encoding = 'utf-8'))

    # resp_param=json.loads(resp_jsonByte.decode())

    resp_json=deserialize(resp_jsonByte.decode())

    # apiinfo(resp_json.Permissions.Permission[0].SourceCidrIp)

    # apidebug(resp_json.)

    return resp_json

def modifySec(host_ip,*key):
    # apidebug(key)

    client = AcsClient(
                    key[0],
                    key[1],
                    'cn-beijing')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-05-26')
    request.set_action_name('AuthorizeSecurityGroup')

    request.add_query_param('RegionId', 'cn-beijing')
    request.add_query_param('SecurityGroupId', 'sg-2zeiafyiu5nh8zsuy1u6')
    request.add_query_param('IpProtocol', 'tcp')
    request.add_query_param('PortRange', '22/22')
    # request.add_query_param('SourceCidrIp', '223.87.240.203')
    # host_ip = key[2]
    apiinfo(host_ip)
    request.add_query_param('SourceCidrIp', host_ip)
    request.add_query_param('Policy', 'accept')
    request.add_query_param('Priority', '1')

    response = client.do_action_with_exception(request)
    apiinfo(response)
    # python2:  print(response)
    # print(str(response, encoding = 'utf-8'))
    return response

def stopInst_rmlater(inst_id,*key):

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    client = AcsClient(
                    key[0],
                    key[1],
                    'cn-beijing')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-05-26')
    request.set_action_name('StopInstance')

    # request.add_query_param('InstanceId', 'i-2ze88p52tbikbgndl5ze')
    request.add_query_param('InstanceId', inst_id)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding = 'utf-8'))

def startstopInst(inst_id,flag,*key):

    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest

    client = AcsClient(
                    key[0],
                    key[1],
                    'cn-beijing')


    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('ecs.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2014-05-26')
    if flag:
        request.set_action_name('StartInstance')
    else:
        request.set_action_name('StopInstance')

    # request.add_query_param('InstanceId', 'i-2ze88p52tbikbgndl5ze')
    request.add_query_param('InstanceId', inst_id)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding = 'utf-8'))
