#!/usr/bin/perl

use HTML::Template;
use CGI qw/:standard/;



my $template = HTML::Template->new(filename => 'index.tmpl',
                                'die_on_bad_params' => 0
                                );

$template->param(APIKEY => param("api-key") );

print "Content-Type: text/html\nAccess-Control-Allow-Origin: *\n\n", $template->output;

