#from opentoni_web.handlers.base import BaseHandler
from opentoni_web.handlers.powhandler import PowHandler
from opentoni_web.models.tinydb.collection import Collection as Model
from opentoni_web.models.tinydb.song import Song
from opentoni_web.config import myapp, database
from opentoni_web.application import app
import simplejson as json
import tornado.web

@app.add_route('/collection/addsong/<uuid:collection_id>', dispatch={"get" : "add_song"})
@app.add_rest_routes("collection")
class Collection(PowHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /collection        #=> list
    # 2  GET    /collection/1      #=> show
    # 3  GET    /collection/new    #=> new
    # 4  GET    /collection/1/edit #=> edit 
    # 5  GET    /collection/page/1 #=> page
    # 6  GET    /collection/search #=> search
    # 7  PUT    /collection/1      #=> update
    # 8  PUT    /collection        #=> update (You have to send the id as json payload)
    # 9  POST   /collection        #=> create
    # 10 DELETE /collection/1      #=> destroy
    #

    # standard supported http methods are:
    # SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    # handler.

    # curl test:
    # windows: (the quotes need to be escape in cmd.exe)
    #   (You must generate a post model andf handler first... update the db...)
    #   POST:   curl -H "Content-Type: application/json" -X POST -d "{ \"title\" : \"first post\" }" http://localhost:8080/post
    #   GET:    curl -H "Content-Type: application/json" -X GET http://localhost:8080/post
    #   PUT:    curl -H "Content-Type: application/json" -X PUT -d "{ \"id\" : \"1\", \"text\": \"lalala\" }" http://localhost:8080/post
    #   DELETE: curl -H "Content-Type: application/json" -X DELETE -d "{ \"id\" : \"1\" }" http://localhost:8080/post
    
    model=Model()
    
    # these fields will be hidden by scaffolded views:
    hide_list=["id", "created_at", "last_updated", "num_played", "path"]
    
    
    def add_song(self, collection_id=None):
        s=Song()
        songs=s.find(s.Query.collection_id == collection_id)
        m=Model()
        me = m.find_by_id(collection_id)
        #self.write(collection_id)
        song_hide_list=["id", "created_at", "last_updated", "num_played", "path", "collection_id"]
        self.success(message="collection show", data=me, songs=songs, songmodel=Song(), song_hide_list=song_hide_list)

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="collection show", data=res)
        
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="collection, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="collection page: #" +str(page), data=res )  
    
    def search(self):
        m=Model()
        return self.error(message="collection search: not implemented yet ")
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="collection, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="collection, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="collection, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="collection, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="collection, error updating " + str(m.id) + "msg: " + str(e), 
                data=m, format="json")
    
    @tornado.web.authenticated
    def update(self, id=None):
        data_json = self.request.body
        m=Model()
        m.init_from_json(data_json)
        res = m.find_by_id(m.id)
        res.init_from_json(data_json)
        try:
            #res.tags= res.tags.split(",")
            res.upsert()
            self.success(message="collection, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="collection, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



    @tornado.web.authenticated
    def destroy(self, id=None):
        try:
            data_json = self.request.body
            print("  .. DELETE Data: ID:" + str(data_json))
            m=Model()
            m.init_from_json(data_json)
            res = m.find_by_id(m.id)
            res.delete()
            self.success(message="todo, destroy id: " + str(m.id))
        except Exception as e:
            self.error(message="todo, destroy id: " + str(e))