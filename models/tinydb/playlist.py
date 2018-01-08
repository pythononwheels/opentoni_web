#
# TinyDB Model:  Playlist
#
from opentoni_web.models.tinydb.tinymodel import TinyModel

class Playlist(TinyModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # http://docs.python-cerberus.org/en/stable/validation-rules.html
    # types: http://docs.python-cerberus.org/en/stable/validation-rules.html#type
    #
    schema = {
        'name':    { 'type': 'string', 'maxlength' : 35},
        'info' :    { 'type': 'string'},
        'path' :    { 'type': 'string'},
        'tags' :    { 'type': 'list', "default" : [] },
        "num_played" :   { "type" : "integer", "default" : 0 },   
        "card_id" :   { "type" : "integer", "default" : 0 }   
        }

    #
    # init
    #
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #
