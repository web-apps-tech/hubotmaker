#!/usr/bin/perl

use HTML::Template;
use CGI qw/:standard/;


my $html_1 = HTML::Template->new(filename => '/var/www/haas-front/html_1.tmpl',
                                'die_on_bad_params' => 0
                                );
my $head = HTML::Template->new(filename => '/var/www/haas-front/head.tmpl',
                                'die_on_bad_params' => 0
                                );
my $navbar = HTML::Template->new(filename => '/var/www/haas-front/navbar.tmpl',
                                'die_on_bad_params' => 0
                                );
my $register = HTML::Template->new(filename => '/var/www/haas-front/register.tmpl',
                                'die_on_bad_params' => 0
                                );

                                $head->param(PATH_PREFIX => $path_prefix);
                                $register->param(PATH_PREFIX => $path_prefix);


print header(-type => "text/html",
             -status => 200,
    	 -charset=>'utf-8',
    	 -Access_Control_Allow_Origin=>'*');
    print  $html_1->output;
    print  $head->output;
    print  $navbar->output;
    print  $register->output;
