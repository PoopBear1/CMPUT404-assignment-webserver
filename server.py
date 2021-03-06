#  coding: utf-8 
import socketserver
import socket
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        payload = self.data.decode()
        if payload:
            payload_data = payload.split()
            method,path = payload_data[0],payload_data[1]
            
            if method == "GET":
                
                    if self.check_path(path):
                        if os.path.exists("./www"+path) and path.endswith("html"):
                            body = open("./www"+path,'r').read()
                            self.request.send("HTTP/1.1 200 OK\r\n".encode())
                            self.request.send("Content-Type: text/html;\r\n".encode())
                            self.request.send("{} {} {}".format("Content-length: ",len(body),"\r\n").encode())
                            self.request.send("Connection : close \r\n\r\n".encode())
                            self.request.send(body.encode())

                        elif os.path.exists("./www"+path) and path.endswith("css"):
                            body = open("./www"+path,'r').read()
                            self.request.send("HTTP/1.1 200 OK\r\n".encode())
                            self.request.send("Content-Type: text/CSS;\r\n".encode())
                            self.request.send("{} {} {}".format("Content-length: ",len(body),"\r\n").encode())
                            self.request.send("Connection : close \r\n\r\n".encode())
                            self.request.send(body.encode())

                        elif os.path.exists("./www"+path+"index.html") and path.endswith('/'):
                            path += "index.html"
                            if open("./www"+path,'r').read():
                                body = open("./www"+path,'r').read()
                                self.request.send("HTTP/1.1 200 OK\r\n".encode())
                                self.request.send("Content-Type: text/html;\r\n".encode())
                                self.request.send("{} {} {}".format("Content-length: ",len(body),"\r\n").encode())
                                self.request.send("Connection : close \r\n\r\n".encode())
                                self.request.send(body.encode())
                            else: self.request.send("HTTP/1.1 404 Not Found".encode())  
                
                        else:
                                
                            try: 
                                body = open('./www'+path+'/index.html','r').read()
                                self.request.send("HTTP/1.1 301 Moved Permanently\r\n".encode())
                                self.request.send("Content-Type: text/html;\r\n".encode())
                                addrs = "Location: http://127.0.0.1:8080"+path+'/\r\n\r\n'
                                self.request.send(addrs.encode())

                            except:
                                self.request.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())  
                    else : self.request.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())  
            else:self.request.send("HTTP/1.1 405 Method Not Allowed".encode())
    
    def check_path(self,path):
        return os.path.realpath(os.getcwd()+'/www' +path).startswith(os.getcwd()+'/www')

            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
