#!/usr/bin/env python
# coding: utf-8
# Copyright Seb Potter 2010

import cyclone.web
from twisted.application import service, internet

class MistralWeb(cyclone.web.Application):
    def __init__(self, config):
        handlers = config.url_mappings()
        self.jinja = config.setup_environment()
        cyclone.web.Application.__init__(self, handlers, **config.settings)


def start_app(config):
    application = service.Application(config.settings['app_name'])
    srv = internet.TCPServer(
        config.settings['app_port'], 
        MistralWeb(config), 
        interface=config.settings['app_interface']
    )
    srv.setServiceParent(application)
    
    return application