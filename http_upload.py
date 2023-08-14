#!/usr/env python3
import http.server
import socketserver
import io
from email.message import Message
import thumb_gen
# Change this to serve on a different port
PORT = 44444

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):        
        r, info = self.deal_post_data()
        print(r, info, "by: ", self.client_address)
        f = io.BytesIO()
        if r:
            f.write(b"Success\n")
        else:
            f.write(b"Failed\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()      

    def deal_post_data(self):
        #ctype, pdict = parse_header(self.headers['Content-Type'])
        #pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        #pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
        
        m = Message()
        ctype = m.get_param('content-type')
        print(ctype)
        if ctype == 'multipart/form-data':
            form = multipart.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            print (type(form))
            try:
                if isinstance(form["file"], list):
                    print("Found image input")
                    for record in form["image"]:
                        open("./web/%s"%record.filename, "wb").write(record.file.read())
                else:
                    print("file is not instanced. Lets try to open it anyway.")
                    open("./web/%s"%form["file"].filename, "wb").write(form["file"].file.read())
            except IOError:
                    return (False, "Can't create file to write, do you have permission to write?")
            except KeyError:
                    return (False, "'image' input was not found in the web form.")
            
            ############### File upload works to here. ############
            
            print(f"{form['passage']}\n{form['title1']}\n{form['title2']}")
        return (True, "Files uploaded")


Handler = CustomHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()