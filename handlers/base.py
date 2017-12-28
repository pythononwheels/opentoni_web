import tornado.web
import tornado.escape
import json
from opentoni_web import config as cfg
#from opentoni_web.models.sql.user import User



class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        """
            receives the URL dict parameter.
            For PoW RESTroutes this looks like this: (Kwargs)
            { "get" : "some_method" }
            { "http_verb" : "method_to_call", ...}
            { "params" : ["id", "name", ... ]}
        """
        print("  .. in initialize")
        print("  .. .. args: " + str(args))
        print("  .. .. kwargs: " + str(kwargs))
        self.dispatch_kwargs = kwargs
        self.dispatch_args = args
        
        
    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        
        #print(self.request)
        self.uri = self.request.uri
        print("Request:" )
        print(30*"-")
        print(" Mehtod: " + self.request.method)
        print(" URI: " + self.uri)
        print(" Handler: " + self.__class__.__name__)
        # path = anything before url-parameters
        self.path = self.request.uri.split('?')[0]
        print(" path: " + self.path)
        #
        # You can use the before_handler in a local controller to
        # process your own prepare stuff.
        # a common use case is to call: self.print_debug_info().
        # which then applies only to this specific Controller.
        # 
        before_handler = getattr(self, "before_handler", None)
        if callable(before_handler):
            print("calling before_handler for " +  str(self.__class__))
            before_handler()
        self.format = self.get_accept_format()

    
    def get_format_list(self, h=None):
        """
            uses a a header list from self.request.headers.get("Accept")
            to just return the plain formats 
            like: html, xml, xhtml or *
        """
        if not h:
            h = self.request.headers.get("Accept")
        headers_raw = h.split(",")
        print(" raw Accept header:" + str( headers_raw ))
        h_final = []
        # example Accept-header: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8 
        for elem in headers_raw:
            # erase everything after ; and +
            try:
                elem = elem[elem.index("/")+1:]
            except:
                pass
            try:
                elem = elem[:elem.index(';')]
            except:
                pass
            try:
                elem = elem[:elem.index('+')]
            except:
                pass
            h_final.append(elem)
        return h_final

    def get_accept_format(self):
        """
            format is either added as accept header format 
            or as .format to the path
            or default_format
            example: /post/12.json (will return json)
        """
        
        format = None
        # Try the dotformat first (if activated)
        if cfg.beta_settings["dot_format"]:
            # try the .format
            if len (self.path.split(".")) > 1:
                format = self.path.split(".")[-1]
                if format in cfg.myapp["supported_formats"]:
                    return format
        
        # Try the Accept Header
        accept_header = self.request.headers.get("Accept", None)
        if accept_header:
            format_list = self.get_format_list(accept_header)
            print(" formats from Accept-Header: " + str(format_list))
            # returns the first matched format from ordered Accept-Header list.
            for fo in format_list:
                if fo in cfg.myapp["supported_formats"]:
                    return fo
        #print("format: " +format)
        if format == None or format == "*":
            # take the default app format (see config.cfg.myapp)
            format = cfg.myapp["default_format"]
        
        if format in cfg.myapp["supported_formats"]:
            return format
        else:
            print(" format error: " + str(format))
            return self.error(
                    message="Format not supported. (see data.format)",
                    data={
                        "format was" : format,
                        "supported_formats" : cfg.myapp["supported_formats"]
                    }
            )
                
    #
    # GET
    #
    # routes have the form: 
    # ( r"/" + action + r"/" + str(api) + r"/(?P<id>.+)/edit/?" , { "get" : "edit", "params" : ["id"] }),
    # or
    # @app.add_route2("/thanks/*", dispatch={"get": "_get"} )
    def get(self, *args, **params):
        #url_params=self.get_arguments("id")
        print(" ----> GET / BaseHandler")
        print("  .. params : " + str(params))
        print("  .. args : " + str(args))
        print("  .. self.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("get", None) != None:
            try:
                # this is the view that will be rendered by success or error,
                # if the format is .html
                # rule: handlerName_methodName
                self.view = self.dispatch_kwargs.get("get", None)

                print("  .. Trying to call handler method: " + self.dispatch_kwargs.get("get") )
                f=getattr(self, self.dispatch_kwargs.get("get"))
                print("  .. trying to call: " + str(f))
                if callable(f):
                    # call the given method
                    return f(*args, **params)
            except TypeError as e:
                self.application.log_request(self, 
                    message=str(e))
                self.error(
                    message=str(e),
                    data = { "request" : str(self.request)},
                    http_code = 405
                )
        else:
            self.error(
                message=" HTTP Method: GET not supported for this route. ",
                data = { "request" : str(self.request )},
                http_code = 405
                )

        #self.write(str(self.request))
    
    #
    # POST   /items     #=> create
    #
    def post(self, *args, **params):
        print(" ---> POST / BaseHandler")
        print("  .. params : " + str(params))
        print("  .. args : " + str(args))
        print("  .. self.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("post", None) != None:
            try:
                # this is the view that will be rendered by success or error,
                # if the format is .html
                # rule: handlerName_methodName
                self.view = self.dispatch_kwargs.get("post", None)

                print("  .. Trying to call handler method: " + self.dispatch_kwargs.get("post") )
                f=getattr(self, self.dispatch_kwargs.get("post"))
                print("  .. trying to call: " + str(f))
                if callable(f):
                    # call the given method
                    return f(*args, **params)
            except TypeError as e:
                self.application.log_request(self, 
                    message=str(e))
                self.error(
                    message=str(e),
                    data = { "request" : str(self.request)},
                    http_code = 405
                )
        else:
             self.error(
                message=" HTTP Method: PUT not supported for this route. ",
                data = { "request" : str(self.request )},
                http_code = 405
                )
        #data = tornado.escape.json_decode(self.request.body)
        #return self.create(data)

    #
    # PUT    /items/1      #=> update
    #
    def put(self, *args, **params):
        print(" ---> PUT / BaseHandler")
        print("  .. params : " + str(params))
        print("  .. args : " + str(args))
        print("  .. self.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("put", None) != None:
            try:
                # this is the view that will be rendered by success or error,
                # if the format is .html
                # rule: handlerName_methodName
                self.view = self.dispatch_kwargs.get("put", None)

                print("  .. Trying to call handler method: " + self.dispatch_kwargs.get("put") )
                f=getattr(self, self.dispatch_kwargs.get("put"))
                print("  .. trying to call: " + str(f))
                if callable(f):
                    # call the given method
                    return f(*args, **params)
            except TypeError as e:
                self.application.log_request(self, 
                    message=str(e))
                self.error(
                    message=str(e),
                    data = { "request" : str(self.request)},
                    http_code = 405
                )
        else:
             self.error(
                message=" HTTP Method: PUT not supported for this route. ",
                data = { "request" : str(self.request )},
                http_code = 405
                )
    
    #
    # DELETE /items/1      #=> destroy
    # 
    def delete(self, *args, **params):
        print(" ---> DELETE / BaseHandler")
        print("  .. params : " + str(params))
        print("  .. args : " + str(args))
        print("  .. self.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("delete", None) != None:
            try:
                # this is the view that will be rendered by success or error,
                # if the format is .html
                # rule: handlerName_methodName
                self.view = self.dispatch_kwargs.get("delete", None)

                print("  .. Trying to call handler method: " + self.dispatch_kwargs.get("delete") )
                f=getattr(self, self.dispatch_kwargs.get("delete"))
                print("  .. trying to call: " + str(f))
                if callable(f):
                    # call the given method
                    return f(*args, **params)
            except TypeError as e:
                self.application.log_request(self, 
                    message=str(e))
                self.error(
                    message=str(e),
                    data = { "request" : str(self.request)},
                    http_code = 405
                )
        else:
             self.error(
                message=" HTTP Method: PUT not supported for this route. ",
                data = { "request" : str(self.request )},
                http_code = 405
                )
    


    def success(self, message=None, data=None, succ=None, prev=None,
        http_code=200, format=None, encoder=None):
        """
            returns data and http_code.
            data will be converted to format.  (std = json)
            for other formats you have to define an encoder in config.py
            (see json as an example)

            data input is model or list of models.
        """
        self.application.log_request(self, message="base.success:" + message)
        self.set_status(http_code)
        if not format:
            format = self.format
        if not format:
            format = cfg.myapp["default_format"]
        if format.lower() == "html":
            # special case where we render the classical html templates
            # if not isinstance(data, (list)):
            #     data=[data]
            # for elem in data:
            #     print("elem: " + str(type(elem)))
            viewname = self.__class__.__name__ + "_" + self.view + ".tmpl"
            if self.view is not None:
                model=self.__class__.model
                show_list=getattr(self.__class__, "show_list", [])
                hide_list=getattr(self.__class__, "hide_list", [])
                return self.render( viewname, data=data, message=message, 
                    handler_name = self.__class__.__name__.lower(), base_route_rest=self.base_route_rest , 
                    model=model, status=http_code, next=succ, prev=prev, model_name=model.__class__.__name__.lower(),
                    show_list=show_list, hide_list=hide_list )
            else:
                self.error(message="Sorry, View: " + viewname +  " can not be found.", 
                    format=format, data=data)
        #
        # if not format == html convert the model or [model] to json 
        # the encoders can convert json to any requested target format.
        # 
        if not data == None:
            data = self.model.res_to_json(data)
        if encoder:
            encoder = encoder
        else:
            encoder = cfg.myapp["encoder"][format]
        self.write(encoder.dumps({
            "status"    : http_code,
            "message"   : message,
            "data"      : data,
            "next"      : succ,
            "prev"      : prev
        }))
        self.finish()

    def error(self, message=None, data=None, succ=None, prev=None,
        http_code=500, format=None, encoder=None, template=None):
        
        self.application.log_request(self, message="base.error:" + str(message))
        
        if template != None:
            self.render(template, message=message, data=data, succ=succ, prev=prev,
                        status=http_code, request=self.request)
        self.set_status(http_code)
        
        if not format:
            format = self.format
        if not format:
            format = cfg.myapp["default_format"]
        if format.lower() == "html":
            return self.render("error.tmpl", data=data, message=message, status=http_code)
        
        # encode the data to json.
        # the encoders convert the json to any requested output format then.
        if not data == None:
            data = self.model.res_to_json(data)

        print(" In base.error:")
        print("  .. data: " + str(data))
        print("  .. Encoding reply into: " + format)
        if encoder:
            encoder = encoder
        else:
            encoder = cfg.myapp["encoder"][format]
        print("  .. Encoded reply: " + encoder.dumps({
            "status"    : http_code,
            "data"      : data,
            "error"     : {
                "message"   : message
                },
            "next"      : succ,
            "prev"      : prev
        }))
        self.write(encoder.dumps({
            "status"    : http_code,
            "data"      : data,
            "error"     : {
                "message"   : message
                },
            "next"      : succ,
            "prev"      : prev
        }))
        self.finish()

    def write_error(status_code, **kwargs):
        """
            write_error may call write, render, set_header, etc to produce 
            output as usual.
            If this error was caused by an uncaught exception 
            (including HTTPError), an exc_info triple will be available as 
            kwargs["exc_info"]. Note that this exception may not be the 
            currentÂ exception for purposes of methods like sys.exc_info() 
            or traceback.format_exc.
        """
        #if status_code == 404:
        return self.render("404.tmpl")

