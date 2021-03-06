#
# TinyDB Model:  {{model_class_name}}
#
from {{appname}}.models.tinydb.tinymodel import TinyModel

class {{model_class_name}}(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'title':    { 'type': 'string', 'maxlength' : 35},
        'text' :    { 'type': 'string'},
        'tags' :    { 'type': 'list', "default" : [] },
        "votes" :   { "type" : "integer", "default" : 0 }   
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
