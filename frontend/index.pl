#!/usr/bin/perl

use HTML::Template;


my $template = HTML::Template->new(filename => 'index.tmpl',
                                'die_on_bad_params' => 0
                                );
print "Content-Type: text/html\nAccess-Control-Allow-Origin: *\n\n", $template->output;

