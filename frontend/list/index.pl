#!/usr/bin/perl

use HTML::Template;
use CGI qw/:standard/;

my $api_key = param("api-key");

my $template = HTML::Template->new(filename => 'index.tmpl',
                                'die_on_bad_params' => 0
                                );

$template->param(APIKEY => param("api-key") );
print header(-type => "text/html",
             -status => 200,
    	 -charset=>'utf-8',
    	 -Access_Control_Allow_Origin=>'*'),
      $template->output;


