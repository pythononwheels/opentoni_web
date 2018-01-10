#
#
# pow settings file
# 
import simplejson as json
import opentoni_web.encoders
import os
import logging
import datetime

server_settings = {
    "protocol"          :   "http://",
    "host"              :   "localhost",
    "port"              :   8080,
    "debug"             :   True,
    "IOLoop.set_blocking_log_threshold" : 0.050,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "xsrf_cookies"      :   False,
    #"log_function"      :   you can give your own log function here.
    "cookie_secret"     :   "3ddc787b-5d69-4842-a06a-5d4e08261333",
    "debug_print"       :   True,
    "logging"           :   True
}

templates = {
    "template_path"     :   server_settings["template_path"],
    "handler_path"      :   os.path.join(os.path.dirname(__file__), "handlers"),
    "model_path"        :   os.path.join(os.path.dirname(__file__), "models"),
    "stubs_path"        :   os.path.join(os.path.dirname(__file__), "stubs"),
    "views_path"        :   os.path.join(os.path.dirname(__file__), "views")
}

myapp = {
    "app_name"          :   "opentoni_web",
    "default_format"    :   "json",
    "supported_formats" :   ["json", "csv", "xml", "html"],
    "encoder"           :   {
            "json"  :   json,
            "csv"   :   opentoni_web.encoders.JsonToCsv(),
            "xml"   :   opentoni_web.encoders.JsonToXml()
    },
    "upload_path"       :   os.path.join(server_settings["static_path"], "upload"),
    "page_size"         :   5,
    "enable_authentication"     :   False,   # False, simple or custom
    "sql_auto_schema"   :   True,
    "logfile"           :   os.path.join(os.path.dirname(__file__),"pow.log"),
    "logformat"         :   logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    "id_pattern"        :   "[0-9\-a-zA-Z]+",       # the regex used to math IDs in URLs (uuid in this case)
    "list_separator"    :   ",",
    "date_format"       :   "%Y-%m-%d %H:%M:%S",
    "internal_fields"   :   ["created_at", "last_updated", "id"],  # these are hidden in the scaffolded views
    "default_rest_route":   "list",
    "list_separator"    :   " "
    #"environment"       :   "development"       # set the current environment (also see the db section)
}

db_base_path = r"c:\khz\devel\opentoni_web"
database = {
    "default_values": {
        "string"    :   "",
        "integer"   :   0,
        "float"     :   0.0,
        "list"      :   [],
        "boolean"   :   False,
        "datetime"  :   datetime.datetime.utcnow(),
        "dict"      :   {},
        "binary"    :   None

    },
    "sql"   : {
        "type"      :   "sqlite",
        "dbname"    :   r"c:\khz\devel\opentoni_web\db.sqlite",   # better leave the r to enable absolute paths with backslashes 
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   True          # switch currently unused
    },
    "tinydb" : {
        "dbname"    :   r"c:\khz\devel\opentoni_web\tiny.db",   # better leave the r to enable absolute paths with backslashes 
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       # switch currently unused
    },
    "mongodb" : {
        "dbname"    :   "testdb",  
        "atlas"     :   False,
        "atlas_conn_str" :  "mongodb+srv://<USER>:<PASSWORD>@cluster0-aetuw.mongodb.net/test", #this is just a sample
        "host"      :   "localhost",       
        "port"      :   27017,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       # switch currently unused
    },
    "elastic" : {
        "dbname"    :   "testdb",   # == elasticsearch index 
        "hosts"     :   ["localhost"],       
        "port"      :   9200,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False       # switch currently unused
    }
}

beta_settings = {
    # Beta settings are erxperimental. You can find details for each Beta setting
    # on www.pythononwheels.org/beta
    
    # Name          :    Enabled ?
    "dot_format"    :   True
}

#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
]