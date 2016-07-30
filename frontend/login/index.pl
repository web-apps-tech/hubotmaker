#!/usr/bin/perl

use HTML::Template;
use CGI qw/:standard/;

my $path_prefix = "../";

my $html_1 = HTML::Template->new(filename => '/var/www/haas-front/html_1.tmpl',
                                'die_on_bad_params' => 0
                                );
my $head = HTML::Template->new(filename => '/var/www/haas-front/head.tmpl',
                                'die_on_bad_params' => 0
                                );
my $navbar = HTML::Template->new(filename => '/var/www/haas-front/navbar.tmpl',
                                'die_on_bad_params' => 0
                                );
my $login = HTML::Template->new(filename => '/var/www/haas-front/login.tmpl',
                                'die_on_bad_params' => 0
                                );

$head->param(PTH_PREFIX => $path_prefix);
$login->param(PTH_PREFIX => $path_prefix);

print header(-type => "text/html",
             -status => 200,
    	 -charset=>'utf-8',
    	 -Access_Control_Allow_Origin=>'*');

    print  $html_1->output;
    print  $head->output;
    print  $navbar->output;
    print  $login->output;
