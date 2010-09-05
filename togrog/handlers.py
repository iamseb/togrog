import cyclone.web
import cyclone.auth
import cyclone
from twisted.python import log
from twisted.internet import defer

import settings

class TogRogRequestHandler(cyclone.web.RequestHandler):
    def render(self, template_name, *args, **kwargs):
        template = self.application.jinja.get_template(template_name)
        args[0].update({'settings': settings })
        x = template.render(*args, **kwargs)
        self.write(x)
    
    @defer.inlineCallbacks    
    def get_current_user(self):
        user_email = self.get_secure_cookie("user")
        if user_email: 
            defer.returnValue(user_email)


class IndexHandler(TogRogRequestHandler):
    def get(self):
        self.write("Hello")
        self.finish()