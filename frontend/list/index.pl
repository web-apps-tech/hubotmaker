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
my $list = HTML::Template->new(filename => '/var/www/haas-front/list.tmpl',
                                'die_on_bad_params' => 0
                                );

print header(-type => "text/html",
             -status => 200,
    	 -charset=>'utf-8',
    	 -Access_Control_Allow_Origin=>'*'),
      $html_1->output,
      $head->output,
      $nabvar->output,
      $list->output;
