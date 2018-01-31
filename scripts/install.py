#!/usr/bin/python
# coding: utf-8

import time
import os
import sys
import socket
import re
import platform
import shlex

base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(base_dir)
install_dir = "/wls/wls81"
soft_dir = "%s/yd_schedule/scripts/soft" % install_dir
conf_dir = "%s/yd_schedule/scripts/conf" % install_dir
env_dir = "%s/sched_env" % install_dir


def bash(cmd):
    """
    run a bash shell command
    执行bash命令
    """
    return shlex.os.system(cmd)


def valid_ip(ip):
    if ('255' in ip) or (ip == "0.0.0.0"):
        return False
    else:
        return True


def color_print(msg, color='red', exits=False):
    """
    Print colorful string.
    颜色打印字符或者退出
    """
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg
    if exits:
        time.sleep(2)
        sys.exit()
    return msg


def get_ip_addr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        if_data = ''.join(os.popen("LANG=C ifconfig").readlines())
        ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', if_data, flags=re.MULTILINE)
        ip = filter(valid_ip, ips)
        if ip:
            return ip[0]
    return ''


class PreSetup(object):
    def __init__(self):
        self.db_host = '172.16.100.72'
        self.db_port = 3306
        self.db_user = 'sched_test'
        self.db_pass = '1jhcfzxWrzslzl'
        self.db = 'yd_sched_test'
        self.ip = ''
        self.dist = platform.linux_distribution()[0].lower()
        self.version = platform.linux_distribution()[1]

    @property
    def _is_redhat(self):
        if self.dist.startswith("centos") or self.dist.startswith("red") or self.dist == "fedora" or self.dist == "amazon linux ami":
            return True

    @property
    def _is_centos7(self):
        if self.dist.startswith("centos") and self.version.startswith("7"):
            return True

    def check_platform(self):
        if not self._is_redhat:
            print(u"支持的平台: CentOS Linux release 7, 暂不支持其他平台安装.")
            exit()

    @staticmethod
    def check_bash_return(ret_code, error_msg):
        if ret_code != 0:
            color_print(error_msg, 'red')
            exit()

    def _create_table(self):
        cmd = "%s/bin/python %s/yd_schedule/manage.py create_db" % (env_dir, install_dir)
        ret = bash(cmd)
        self.check_bash_return(ret, "创建数据库表失败")

    def _test_db_conn(self):
        import MySQLdb
        try:
            MySQLdb.connect(host=self.db_host, port=int(self.db_port),
                            user=self.db_user, passwd=self.db_pass, db=self.db)
            color_print('连接数据库成功', 'green')
            return True
        except MySQLdb.OperationalError, e:
            color_print('数据库连接失败 %s' % e, 'red')
            return False

    def _depend_rpm(self):
        color_print('开始安装依赖包', 'green')
        if self._is_redhat:
            cmd = 'yum -y install python-pip gcc gcc-c++ python-devel vim lrzsz python-virtualenv psmisc emerge zlib freetype libX11 libXext libXrender '
            ret_code = bash(cmd)
            self.check_bash_return(ret_code, "安装依赖失败, 请检查安装源是否更新或手动安装！")
        else:
            color_print('系统版本非Centos7， 请检查', 'red')

    def _require_pip(self):
        color_print('开始安装依赖pip包', 'green')
        cmd = "cd %s && virtualenv sched_env && source %s/bin/activate " % (install_dir, env_dir)
        bash(cmd)
        pip_update = "%s/bin/pip install --upgrade pip -i http://pypi.douban.com/simple" % env_dir
        bash(pip_update)
        cmd_pip = "%s/bin/pip install -r %s/yd_schedule/scripts/requirement.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com" % (env_dir, install_dir)
        ret_code1 = bash(cmd_pip)
        self.check_bash_return(ret_code1, "安装依赖的python库失败！")

    def _setup_nginx(self):
        color_print('开始安装nginx', 'green')
        cmd_pcre = "cd %s && unzip pcre-8.34.zip && cd pcre-8.34 && ./configure && make && make install" % soft_dir
        ret_code = bash(cmd_pcre)
        self.check_bash_return(ret_code, "安装pcre-8.34失败！")
        cmd_nginx = "cd %s && tar -xvf nginx-1.11.3.tar.gz && cd nginx-1.11.3 && ./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-stream_ssl_module --with-mail_ssl_module && make && make install" % soft_dir
        ret_code = bash(cmd_nginx)
        self.check_bash_return(ret_code, "安装nginx失败！")

    def _setup_uwsgi(self):
        color_print('开始安装uwsgi', 'green')
        cmd_uwsgi = "cd %s && tar -xvf uwsgi-2.0.13.1.tar.gz && cd uwsgi-2.0.13.1 && make && echo /usr/local/lib >> /etc/ld.so.conf && ldconfig && cp uwsgi /usr/bin" % soft_dir
        ret_code = bash(cmd_uwsgi)
        self.check_bash_return(ret_code, "安装uwsgi失败！")

    def _setup_redis(self):
        color_print('开始安装redis', 'green')
        cmd_redis = "cd %s && cp %s/redis-3.2.3.tar.gz ./ && tar -xvf redis-3.2.3.tar.gz && cd redis-3.2.3/src && make && make install && " \
                    "mkdir -p /usr/local/redis/etc && mkdir -p /usr/local/redis/bin && mv mkreleasehdr.sh " \
                    "redis-benchmark redis-check-aof redis-check-rdb redis-cli redis-sentinel " \
                    "redis-server redis-trib.rb /usr/local/redis/bin/" % (install_dir, soft_dir)
        ret_code = bash(cmd_redis)
        self.check_bash_return(ret_code, "安装redis失败！")
        start_redis = "cp %s/redis.conf /usr/local/redis/etc/ && /usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf" % conf_dir
        ret_code = bash(start_redis)
        self.check_bash_return(ret_code, "start_redis失败！")

    def _init_nginx_uwsgi(self):
        bash("mkdir %s/logs" % install_dir)
        cmd = "cp %s/asset.conf /usr/local/nginx/conf/vhost/ && cp %s/sched_uwsgi_ini /usr/local/nginx/conf/conf/" % (conf_dir, conf_dir)
        bash(cmd)
        cmd = "cd %s && %s/start_stop_service.sh start" % (install_dir, install_dir)
        ret_code = bash(cmd)
        self.check_bash_return(ret_code, "start_nginx_uwsgi失败！")

    def _setup_supervisor(self):
        cmd = "%s/bin/pip install supervisor -i http://pypi.douban.com/simple --trusted-host pypi.douban.com" % env_dir
        ret_code = bash(cmd)
        self.check_bash_return(ret_code, "安装supervisor失败！")
        cmd = "%s/bin/supervisord -c %s/supervisord.conf" % (env_dir, conf_dir)
        ret_code = bash(cmd)
        self.check_bash_return(ret_code, "Start supervisor失败！")

    def start(self):
        color_print('请务必先查看手册,检查soft及conf&star_stop脚本是否已上传至相应目录')
        time.sleep(3)
        self.check_platform()
        self._depend_rpm()
        self._require_pip()
        self._test_db_conn()
        self._create_table()
        # redis = raw_input('是否安装新的Redis服务器? (y/n) [y]: ')
        # if redis != 'n':
        #     self._setup_redis()
        # self._setup_nginx()
        # self._setup_uwsgi()
        self._init_nginx_uwsgi()
        self._setup_supervisor()


if __name__ == '__main__':
    pre_setup = PreSetup()
    pre_setup.start()
