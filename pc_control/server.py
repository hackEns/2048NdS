#!/usr/bin/env python2
# -*- coding: utf8 -*-

from bottle import Bottle, debug, run, static_file
 
app = Bottle()
 
@app.route('/<filename:path>')
def server_static(filename):
    return static_file(filename, root='../frontend')

@app.route('/')
def root():
    return static_file('index.html', root='../frontend')

run(app, host='localhost', port=8080, reloader=True)
