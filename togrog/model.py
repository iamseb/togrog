#!/usr/bin/env python
# coding: utf-8

import simplejson as json

from twisted.python import log
from twisted.internet import defer

from togrog.manager import Manager
from togrog.fields import *

class Model(object):
    
    objects = Manager()
    
    default_fields = {
        '_id': ObjectIdField,
        'created': DateTimeField,
        'modified': ListField,
    }
    
    def __init__(self, **kwargs):
        self.fields = {}
        for key, fieldtype in self.__class__.default_fields.iteritems():
            self.fields[key] = fieldtype(name=key, value=kwargs.get(key))
            
    def __getattr__(self, name):
        fields = self.__dict__.get('fields')
        if name == 'fields':
            return fields
        elif fields.has_key(name):
            return fields[name].value
        else:
            return self.__dict__[name]
            
    def __setattr__(self, name, value):
        fields = self.__dict__.get('fields')
        if name == 'fields':
            self.__dict__['fields'] = value
        elif fields.has_key(name):
            fields[name].value = value
        else:
            self.__dict__[name] = value
            
    def to_mongo(self):
        output = {}
        for fieldname, field in self.fields.iteritems():
            output.update(field.to_mongo())
        return output
        
    def save(self):
        if not self.created:
            self.created = datetime.utcnow()
        self.modified.append(datetime.utcnow())
        self.objects.insert(self)
        self.objects.update(self)
