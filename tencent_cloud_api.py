from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import cvm_client
from tencentcloud.cvm.v20170312 import models as cvm_models
from tencentcloud.vpc.v20170312 import vpc_client
from tencentcloud.vpc.v20170312 import  models as vpc_models

from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

def new_cvm_client(cred,method):

        httpProfile = HttpProfile()

        httpProfile.reqMethod = "GET"
        HttpProfile.reqTimeout = 30
        httpProfile.endpoint = "cvm.ap-guangzhou.tencentcloudapit.com"


        clientProfile = ClientProfile()
        clientProfile.signMethod = "HmacSHA256"
        clientProfile.HttpProfile = httpProfile

        client = cvm_client.CvmClient(cred,"ap-guangzhou",clientProfile)

        return client

def new_vpc_client(cred,method):

        httpProfile = HttpProfile()

        httpProfile.reqMethod = "GET"
        HttpProfile.reqTimeout = 30
        httpProfile.endpoint = "cvm.ap-guangzhou.tencentcloudapit.com"
        clientProfile = ClientProfile()
        clientProfile.signMethod = "HmacSHA256"
        clientProfile.HttpProfile = httpProfile

        client = vpc_client.VpcClient(cred,"ap-guangzhou",clientProfile)

        return client


def describeIns(cred):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
        # cred = credential.Credential(
        #     os.environ.get("TENCENTCLOUD_SECRET_ID"),
        #     os.environ.get("TENCENTCLOUD_SECRET_KEY"))
        client=new_cvm_client(cred=cred,method="GET")

        req=cvm_models.DescribeInstancesRequest()

        respFilter = cvm_models.Filter()
        respFilter.Name = "zone"
        respFilter.Values = ['ap-guangzhou-3','ap-guangzhou-2']


        resp = client.DescribeInstances(req)

        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        # print(err)
        pass


def getPolicyset(cred):
    try:
        client=new_vpc_client(cred=cred,method="GET")

        req=vpc_models.DescribeSecurityGroupPoliciesRequest()
        req.SecurityGroupId = "sg-hc7qsa1z"
        print(req.to_json_string())

        # respFilter = vpc_models.Filter()
        # respFilter.Name = "zone"
        # respFilter.Values = ['ap-guangzhou-3','ap-guangzhou-2']

        # resp = client.DescribeSecurityGroupPolicies(req)

        resp = client.DescribeSecurityGroupPolicies(req)


        print(resp)

    except TencentCloudSDKException as err:
        print(err)

def updataIngress(cred):
    try:
        client=new_vpc_client(cred=cred,method="GET")

        req=vpc_models.ModifySecurityGroupPoliciesRequest()

        reqPolicyset=vpc_models.SecurityGroupPolicySet()
        # reqPolicyset.Version="2"
        reqPolicyset.Ingress=[vpc_models.SecurityGroupPolicy()]
        reqPolicyset.Egress=[vpc_models.SecurityGroupPolicy()]

        # reqPolicyset.Ingress.append()

        reqPolicyset.Ingress[0].CidrBlock="117.172.9.99"
        # reqPolicyset.Ingress[0].Port=22
        # reqPolicyset.Ingress[0].PolicyIndex="1"
        req.SecurityGroupPolicySet= reqPolicyset
        # print(reqPolicyset.to_json_string())
        req.SecurityGroupId = "sg-hc7qsa1z"
        print(req.to_json_string())

        # respFilter = vpc_models.Filter()
        # respFilter.Name = "zone"
        # respFilter.Values = ['ap-guangzhou-3','ap-guangzhou-2']

        # resp = client.DescribeSecurityGroupPolicies(req)

        resp = client.ModifySecurityGroupPolicies(req)
        print(resp)

    except TencentCloudSDKException as err:
        print(err)



