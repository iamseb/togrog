#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import math

import simplejson as json
from settings import backend


class Field(object):
    
    fieldtype = None
    
    def __init__(self, name='', value=None):
        if value is None and callable(getattr(self, 'default', None)):
            self._value = getattr(self, 'default')()
        else:
            try:
                self._value = self.fieldtype(value)
            except TypeError, e:
                self._value = value
        self.name = name
        
    def __unicode__():
        return self.value.__unicode__()
        
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, val):
        self._value = val
        
    def to_mongo(self):
        if hasattr(self, 'prep_value'):
            self.prep_value()
        return {self.name: self.value}
        
    @classmethod
    def from_mongo(cls, name, value):
        return cls(value, name)
    

class UnicodeField(Field):
    fieldtype = unicode
    
class ObjectIdField(Field):
    fieldtype = backend.ObjectId
    
class DateTimeField(Field):
    fieldtype = datetime
    default = datetime.utcnow
    
    def prep_value(self):
        self._value = self._value.replace(
            microsecond = int(
                math.floor(self._value.microsecond / 1000) * 1000
            )
        )

        
class IntField(Field):
    fieldtype = int
    
class FloatField(Field):
    fieldtype = float
    
class ListField(Field):
    fieldtype = list
    default = list
        
class JSONField(Field):
    fieldtype = unicode
    
    @property
    def value(self):
        return json.loads(self._value)

#end
