#!/usr/bin/env python
# coding: utf-8
# Copyright Seb Potter 2010

import cyclone.web
from twisted.application import service, internet

class TogRogWeb(cyclone.web.Application):
    def __init__(self, settings):
        handlers = settings.url_mappings()
        self.jinja = settings.setup_environment()
        cyclone.web.Application.__init__(self, handlers, settings)


def start_app(settings):
    application = service.Application(settings.APP_NAME)
    srv = internet.TCPServer(
        settings.APP_PORT, 
        TogRogWeb(settings), 
        interface=settings.APP_INTERFACE
    )
    srv.setServiceParent(application)
    
    return application