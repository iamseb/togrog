#!/usr/bin/env python
# coding: utf-8

from settings import get_database, backend

def stringify_keys(vals):
    newvals = {}
    for k,v in vals.iteritems():
        newvals[str(k)] = v
    return newvals

class Manager(object):
    
    model = None
    collection = None
            
    def __get__(self, instance, cls):
        self.model = cls
        self.collection = getattr(get_database(), self.model.__name__.lower())
        return self
        
    def new(self, *args, **kwargs):
        return self.model(*args, **kwargs)
        
    def create(self, *args, **kwargs):
        m = self.new(*args, **kwargs)
        m.save()
        return m
        
    def from_mongo(self, vals):
        vals = stringify_keys(vals)
        m = self.model(**vals)
        return m
        
    def insert(self, instance):
        self.collection.insert(instance.to_mongo())
        
    def update(self, instance):
        self.collection.update(instance.fields['_id'].to_mongo(), instance.to_mongo())
        
    def get(self, key):
        if not isinstance(key, backend.ObjectId):
            key = backend.ObjectId(key)
        return self.from_mongo(self.collection.find_one(key))
    
# end
