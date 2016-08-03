#!/usr/bin/sh

if [ ! -e /var/run/uwsgi ]; then
    mkdir /var/run/uwsgi
fi

if [ ! -e /var/run/plack ]; then
    mkdir /var/run/plack
fi

export PATH="/root/.anyenv/envs/pyenv/shims/:$PATH"
export PERL_LOCAL_LIB_ROOT="$PERL_LOCAL_LIB_ROOT:/root/perl5"
export PERL_MB_OPT="--install_base /root/perl5"
export PERL_MM_OPT="INSTALL_BASE=/root/perl5"
export PERL5LIB="/root/perl5/lib/perl5:$PERL5LIB"
export PATH="/root/perl5/bin:$PATH"

cd /root/hubotmaker/apps
uwsgi uwsgi.ini
plackup -s FCGI --listen /var/run/plack/haas-front.sock --pid /var/run/plack/haas-front.pid -a scripts/haas.psgi
