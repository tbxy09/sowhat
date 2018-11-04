# from fabric import Connection
# from fabric import task
# c=Connection('tbxy09@localhost')
from fabric.api import cd, lcd, env, local, parallel, serial
from fabric.api import put, run, settings, sudo, prefix
from fabric.operations import prompt
from fabric.contrib import django
from fabric.contrib import files
from fabric.state import connections
# from fabric.colors import red, green, blue, cyan, magenta, white, yellow
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.connection import EC2Connection
from tencent_cloud_api import describeIns,updataIngress
# from vendor import yaml
from pprint import pprint
from collections import defaultdict
from contextlib import contextmanager as _contextmanager
# from fabric2 import Connection
import os
import time
import sys
import re


django.settings_module('settings')
try:
    from django.conf import settings as django_settings
except ImportError:
    print( " ---> Django not installed yet." )
    django_settings = None

# ============
# = DEFAULTS =
# ============

env.hosts = ['tbxy09@localhost']
# env.SECRETS_PATH=
env.SECRETS_PATH = '/srv/sowhat'
env.app_directory='/opt/playground/sowhat'

# def setup_hosts():
#     put(os.path.join(env.SECRETS_PATH, 'configs/hosts'), '/etc/hosts', use_sudo=True)
#     sudo('echo "\n\n127.0.0.1   `hostname`" | sudo tee -a /etc/hosts')

# def copy_certificates():
#     cert_path = '%s/config/certificates' % env.NEWSBLUR_PATH
#     run('mkdir -p %s' % cert_path)
#     put(os.path.join(env.SECRETS_PATH, 'certificates/newsblur.com.crt'), cert_path)
#     put(os.path.join(env.SECRETS_PATH, 'certificates/newsblur.com.key'), cert_path)
#     put(os.path.join(env.SECRETS_PATH, 'certificates/comodo/newsblur.com.pem'), cert_path)
#     put(os.path.join(env.SECRETS_PATH, 'certificates/comodo/dhparams.pem'), cert_path)
#     put(os.path.join(env.SECRETS_PATH, 'certificates/ios/aps_development.pem'), cert_path)
#     put(os.path.join(env.SECRETS_PATH, 'certificates/ios/aps.pem'), cert_path)
#     run('cat %s/newsblur.com.pem > %s/newsblur.pem' % (cert_path, cert_path))
#     run('echo "\n" >> %s/newsblur.pem' % (cert_path))
#     run('cat %s/newsblur.com.key >> %s/newsblur.pem' % (cert_path, cert_path))

def copy_ssh_keys(username='tbxy09', private=False):

    # sudo('mkdir -p ~%s/.ssh' % username)

    put(os.path.join(env.SECRETS_PATH, 'keys/newsblur.key.pub'), 'local.key.pub')
    sudo('mv local.key.pub ~%s/.ssh/id_rsa.pub' % username)
    if private:
        put(os.path.join(env.SECRETS_PATH, 'keys/newsblur.key'), 'local.key')
        sudo('mv local.key ~%s/.ssh/id_rsa' % username)

    sudo("echo \"\n\" >> ~%s/.ssh/authorized_keys" % username)
    sudo("echo `cat ~%s/.ssh/id_rsa.pub` >> ~%s/.ssh/authorized_keys" % (username, username))
    sudo('chown -R %s.%s ~%s/.ssh' % (username, username, username))
    sudo('chmod 700 ~%s/.ssh' % username)
    sudo('chmod 600 ~%s/.ssh/id_rsa*' % username)

def setup_launch_git():

    # with cd('/opt/playground/sowhat'):
    with cd(env.app_directory):
        run('./setup_sowhat.sh')

# @task
def setup_regular_task():
    # print('running the setup_regular_task')
    # run('cd /opt/playground/sowhat')
    # with cd('/opt/playground/sowhat'):
    with cd(env.app_directory):
        run('cp /root/vimwiki/diary/Makefile Makefile')

# def get_latest_commit():
#     return urlopen(env.commits_server).read()

# @task
def deploy():
    with cd(env.app_directory):
        pass

# @parallel
def setup_hosts():
    put(os.path.join(env.SECRETS_PATH, 'configs/hosts'), '/etc/hosts', use_sudo=True)
    # sudo('echo "\n\n127.0.0.1   `hostname`" | sudo tee -a /etc/hosts')

def get_ip():
    run('curl ipinfo.io/ip')
    # put(os.path.join(env.SECRETS_PATH, 'configs/hosts'), '/etc/hosts', use_sudo=True)
    # sudo('echo "\n\n127.0.0.1   `hostname`" | sudo tee -a /etc/hosts')

def setup_tencent_instance():
    from tencentcloud.common import credential
    cred = credential.Credential(
                                 django_settings.TC_SECRET_ID,
                                 django_settings.TC_SECRET_KEY
                                 # os.getenv('TENCENTCLOUD_SECRET_ID'),
                                 # os.getenv('TENCENTCLOUD_SECRET_KEY')
                                )
    # return a instance
    # instance=describeIns(cred)
    instance = updataIngress(cred)

    # adding to the host list,this is the ip address
    # host = instance.public_dns_name
    # env.host_string = host
    print(instance)

def setup_ec2():
    AMI_NAME = 'ami-834cf1ea'       # Ubuntu 64-bit 12.04 LTS
    # INSTANCE_TYPE = 'c1.medium'
    INSTANCE_TYPE = 'c1.medium'
    conn = EC2Connection(django_settings.AWS_ACCESS_KEY_ID, django_settings.AWS_SECRET_ACCESS_KEY)
    reservation = conn.run_instances(AMI_NAME, instance_type=INSTANCE_TYPE,
                                     key_name=env.user,
                                     security_groups=['db-mongo'])
    instance = reservation.instances[0]

    print( "Booting reservation: %s/%s (size: %s)" .format(reservation, instance, INSTANCE_TYPE) )

    i = 0
    while True:
        if instance.state == 'pending':
            print(".")
            sys.stdout.flush()
            instance.update()
            i += 1
            time.sleep(i)
        elif instance.state == 'running':
            print ("...booted: %s" .format(instance.public_dns_name))
            time.sleep(5)
            break
        else:
            print ("!!! Error: %s" .format(instance.state))
            return

    host = instance.public_dns_name
    env.host_string = host

# ===========
# = Tencent =
# ===========

TENCENTCLOUD_SECRET_ID  = os.getenv("TENCENTCLOUD_SECRET_ID")
TENCENTCLOUD_SECRET_KEY = os.getenv("TENCENTCLOUD_SECRET_KEY")




# ======
# = S3 =
# ======

if django_settings:
    try:
        ACCESS_KEY  = django_settings.S3_ACCESS_KEY
        SECRET      = django_settings.S3_SECRET
        BUCKET_NAME = django_settings.S3_BACKUP_BUCKET  # Note that you need to create this bucket first
    except:
        print( " ---> You need to fix django's settings. Enter python and type `import settings`." )

def save_file_in_s3(filename):
    conn   = S3Connection(ACCESS_KEY, SECRET)
    bucket = conn.get_bucket(BUCKET_NAME)
    k      = Key(bucket)
    k.key  = filename

    k.set_contents_from_filename(filename)

def get_file_from_s3(filename):
    conn   = S3Connection(ACCESS_KEY, SECRET)
    bucket = conn.get_bucket(BUCKET_NAME)
    k      = Key(bucket)
    k.key  = filename

    k.get_contents_to_filename(filename)

def list_backup_in_s3():
    conn   = S3Connection(ACCESS_KEY, SECRET)
    bucket = conn.get_bucket(BUCKET_NAME)

    for i, key in enumerate(bucket.get_all_keys()):
        print ( "[%s] %s" .format(i, key.name) )

def delete_all_backups():
    #FIXME: validate filename exists
    conn   = S3Connection(ACCESS_KEY, SECRET)
    bucket = conn.get_bucket(BUCKET_NAME)

    for i, key in enumerate(bucket.get_all_keys()):
        print("deleting %s" .format(key.name))
        key.delete()
