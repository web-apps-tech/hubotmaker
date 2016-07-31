#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use Plack::App::File;

Plack::App::File->new(root => ".")->to_app;
