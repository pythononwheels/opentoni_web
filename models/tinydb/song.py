#
# TinyDB Model:  Song
#
from opentoni_web.models.tinydb.tinymodel import TinyModel

class Song(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'title':    { 'type': 'string', 'maxlength' : 35},
        'language' :  { 'type': 'string', "allowed" : ["cs", "de", "en", "fr", "fi", "nl", "us", "hu", "it", "pl"]},
        'info' :    { 'type': 'string'},
        'tags' :    { 'type': 'list', "default" : [] },
        "num_played" :   { "type" : "integer", "default" : 0 },  
        "collection_id" :   { "type" : "string" }   
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
