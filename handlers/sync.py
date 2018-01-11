import tornado.web
from opentoni_web.handlers.base import BaseHandler
from opentoni_web.application import app
from tornado import gen
from opentoni_web.models.tinydb.collection import Collection

@app.add_route('/sync', dispatch={"get" : "sync"})
class Sync(BaseHandler):
    # on HTTP GET this method will be called. See dispatch parameter.
    def sync(self, year=None):
        """
            get the info from the DB and dump the json file(s)
            opentoni.json => Collection info

            Format: (see: https://github.com/pythononwheels/opentoni/blob/master/opentoni/opentoni.json )
            {
    
                "1"   :   {
                    "type" : "random",
                    "path" : "music",
                    "info" : "Musik Zufallssong"
                },
                "2"   :   {
                    "type" : "song",
                    "path" : "subdir/song.mp3",
                    "info" : "Single song"
                },
                "3"   :   {
                    "type" : "song",
                    "path" : "die_wilden_kerle/Die_wilden_fussball_kerle_band_1_leon_der_slalomdribbler.mp3",
                    "info" : "Die wilden fussball kerle band 1 leon der slalomdribbler"
                },
                "4"   :   {
                    "type" : "playlist",
                    "path" : "playlist1.m3u",
                    "info" : "PLay a playlist"
                },
                "5"   :   {
                    "type" : "random_playlist",
                    "path" : "music",
                    "info" : "creates a random playlist from all files in path and plays it"
                }

            }
        """
        c=Collection()
        res=c.get_all()
        #out={}
        #for elem in res:
        #    out[elem.card_id]=elem.to_dict()
            
        self.success(message="I got:", data=list(res), model=c, format="json")
    
    
