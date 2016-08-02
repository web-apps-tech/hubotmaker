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

    my $html_1 = HTML::Template->new(
        filename => '/var/www/haas-front/templates/html_1.tpl',
        'die_on_bad_params' => 0
        );
    my $head = HTML::Template->new(
        filename => '/var/www/haas-front/templates/head.tpl',
        'die_on_bad_params' => 0
        );
    my $navbar = HTML::Template->new(
        filename => '/var/www/haas-front/templates/navbar.tpl',
        'die_on_bad_params' => 0
        );

    $head->param(PATH_PREFIX => $path_prefix);
    $head->param(TITLE => $title);
    $body->param(PATH_PREFIX => $path_prefix);

    # アプリケーションの処理
    return [
        200,
        ['Content-Type'=>'text/html'],
        [$html_1->output.$head->output.$navbar->output.$body->output]
        ];
};

builder {
    enable "Plack::Middleware::Static",  path => qr{^/static}, root => '/var/www/haas-front';
    $app;
};
