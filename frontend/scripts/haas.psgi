#!/usr/bin/perl

use HTML::Template;
use CGI qw/:standard/;
use strict;
use warnings;
use Plack::Builder;

my $app = sub {
    my $env = shift;

    my @params = split(/\//,$env->{'PATH_INFO'});
    my $routing = "/".$params[1];

    my $path_prefix = "/static/";
    my $title = "Hubot Maker (&beta;) :: ";
    my $body;


    if ($routing eq "/") {
        $title .= "hubot list";
        $body = HTML::Template->new(
            filename => '/var/www/haas-front/templates/list.tpl',
            'die_on_bad_params' => 0
            );
    }elsif ($routing eq "/login"){
        $title .= "User Login";
        $body = HTML::Template->new(
            filename => '/var/www/haas-front/templates/login.tpl',
            'die_on_bad_params' => 0
            );
    }elsif ($routing eq "/register"){
        $title .= "Registeration";
        $body = HTML::Template->new(
            filename => '/var/www/haas-front/templates/register.tpl',
            'die_on_bad_params' => 0
            );
    }else{
    }

    my $base = HTML::Template->new(
        filename => '/var/www/haas-front/templates/base.tpl',
        'die_on_bad_params' => 0
        );

    $base->param(
        PATH_PREFIX => $path_prefix,
        TITLE => $title
        );
    $body->param(PATH_PREFIX => $path_prefix);

    # アプリケーションの処理
    return [
        200,
        ['Content-Type'=>'text/html'],
        [$base->output.$body->output]
        ];
};

builder {
    enable "Plack::Middleware::Static",  path => qr{^/static}, root => '/var/www/haas-front';
    $app;
};
