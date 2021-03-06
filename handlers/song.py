#from opentoni_web.handlers.base import BaseHandler
from opentoni_web.handlers.powhandler import PowHandler
from opentoni_web.models.tinydb.song import Song as Model
from opentoni_web.config import myapp, database, server_settings
from opentoni_web.application import app
import simplejson as json
import tornado.web
import os

@app.add_route('/song/add/<uuid:collection_id>', dispatch={"post" : "add_song"})
@app.add_rest_routes("song")
class Song(PowHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /song        #=> list
    # 2  GET    /song/1      #=> show
    # 3  GET    /song/new    #=> new
    # 4  GET    /song/1/edit #=> edit 
    # 5  GET    /song/page/1 #=> page
    # 6  GET    /song/search #=> search
    # 7  PUT    /song/1      #=> update
    # 8  PUT    /song        #=> update (You have to send the id as json payload)
    # 9  POST   /song        #=> create
    # 10 DELETE /song/1      #=> destroy
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
    hide_list=["id", "created_at", "last_updated", "collection_id"]

    def add_song(self, collection_id=None):
        print("Song.add_song: Add song to collection:" + str(collection_id))
        print(self.request.body)
        print(self.get_body_argument("testfield", default=None, strip=False))
        song=Model()
        try:
            file1 = self.request.files['file'][0]
            #for key in file1.keys():
            #    print("key=>" + str(key))
            original_fname = file1['filename']
            # name the song the same as the filename
            songtitle=os.path.splitext(original_fname)[0]
            songtitle=songtitle.replace(" ", "_")
            song.title=songtitle
            song.language="en"
            song_info=songtitle
            song.tags=[]
            song.num_played=0
            song.collection_id=collection_id
            
            extension = os.path.splitext(original_fname)[1]
            #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
            final_filename= original_fname
            final_filename = os.path.join(myapp["upload_path"], final_filename)
            output_file = open( final_filename, 'wb')
            output_file.write(file1['body'])
            song.upsert()
            self.success(message=" final_filename is uploaded", data=song, format="json")
        except: 
            self.error(message=" Error uploading final_filename", format="json")
        
            
        

    def show(self, id=None):
        m=Model()
        res=m.find_by_id(id)
        self.success(message="song show", data=res)
        
    def list(self):
        m=Model()
        res = m.get_all()  
        self.success(message="song, index", data=res)         
    
    def page(self, page=0):
        m=Model()
        res=m.page(page=int(page), page_size=myapp["page_size"])
        self.success(message="song page: #" +str(page), data=res )  
    
    def search(self):
        m=Model()
        return self.error(message="song search: not implemented yet ")
        
    @tornado.web.authenticated
    def edit(self, id=None):
        m=Model()
        try:
            print("  .. GET Edit Data (ID): " + id)
            res = m.find_by_id(id)
            self.success(message="song, edit id: " + str(id), data=res)
        except Exception as e:
            self.error(message="song, edit id: " + str(id) + "msg: " + str(e) , data=None)

    @tornado.web.authenticated
    def new(self):
        m=Model()
        self.success(message="song, new",data=m)

    @tornado.web.authenticated
    def create(self):
        try:
            data_json = self.request.body
            m=Model()
            m.init_from_json(data_json, simple_conversion=True)
            m.upsert()
            self.success(message="song, successfully created " + str(m.id), 
                data=m, format="json")
        except Exception as e:
            self.error(message="song, error updating " + str(m.id) + "msg: " + str(e), 
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
            self.success(message="song, successfully updated " + str(res.id), 
                data=res, format="json")
        except Exception as e:
            self.error(message="song, error updating: " + str(m.id) + "msg: " + str(e), data=data_json, format="json")



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