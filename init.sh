#!/usr/bin/bash

set -eu

if [ ! -e ~/.anyenv ]; then
    sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
    sudo rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm

    sudo yum install -y wget epel-release nginx openssl-devel bzip2-devel readline-devel

    sudo cp ~/hubotmaker/etc/systemd/system/hubotmaker.service /etc/systemd/system/hubotmaker.service
    sudo sed -rie "s/user +nginx;/user root root;/" /etc/nginx/nginx.conf
    sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
    sudo cp ~/hubotmaker/etc/nginx/conf.d/hubotmaker.conf /etc/nginx/conf.d/hubotmaker.conf

    sudo mkdir /usr/libexec/hubotmaker
    sudo cp ~/hubotmaker/usr/libexec/hubotmaker/hubotmaker.sh /usr/libexec/hubotmaker/hubotmaker.sh
    sudo chmod +x /usr/libexec/hubotmaker/hubotmaker.sh
    sudo cp ~/hubotmaker/apps/config.py.default ~/hubotmaker/apps/config.py
    sudo sed -rie "s/'user': '',/'user': 'root',/" ~/hubotmaker/apps/config.py

    # install mariadb
    sudo yum install -y mariadb mariadb-server
    sudo systemctl start mariadb
    sudo systemctl enable mariadb
    mysql -uroot -e 'CREATE DATABASE hubot_service;'

    # install redis
    sudo yum -y --enablerepo=remi,remi-test,epel install redis
    sudo systemctl start redis
    sudo systemctl enable redis

    git clone https://github.com/riywo/anyenv ~/.anyenv
    echo 'export PATH="$HOME/.anyenv/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(anyenv init -)"' >> ~/.bashrc
    exec $SHELL -l
fi

if [ -e ~/.anyenv && ! -e ~/.anyenv/envs/plenv ]; then
   anyenv install pyenv
   anyenv install plenv
   exec $SHELL -l
fi

if [ -e ~/.anyenv/envs/plenv ]; then
   pyenv install 3.5.2
   pyenv global 3.5.2
   pip install -r ~/hubotmaker/spec/requirements.txt
   pyenv rehash
   cd ~/hubotmaker/apps
   python -B json2mysql.py
   sudo mkdir /var/log/uwsgi
   cd ~/
   plenv install 5.25.3
   plenv global 5.25.3
   yes | cpan CGI
   cpan HTML::Template
   cpan Task::Plack
   plenv rehash

   sudo yum install -y docker
   sudo sed -rie "s@OPTIONS='--selinux-enabled --log-driver=journald'@OPTIONS='--selinux-enabled --log-driver=journald -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock'@" /etc/sysconfig/docker
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo docker pull redis:alpine
   cd ~/hubotmaker/
   git submodule init
   git submodule update
   cd ~/
   sudo docker build -t hubot ~/hubotmaker/Docker/hubot/

   firewall-cmd --add-service=http --zone=public --permanent
   firewall-cmd --add-port=80/tcp --zone=public --permanent
   firewall-cmd --reload

   sudo systemctl start nginx
   sudo systemctl enable nginx
   sudo systemctl start hubotmaker
   sudo systemctl enable hubotmaker
fi
