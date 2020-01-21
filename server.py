#  coding: utf-8 
import socketserver
import socket

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
        # print("payloapayloadd",payload)
        payload_data = payload.split()
        method,path = payload_data[0],payload_data[1]
        if method == "GET"  :
            try:
                if path.endswith("html"):
                    body = open("./www"+path,'r').read()
                    self.request.send("HTTP/1.1 200 OK\r\n".encode())
                    self.request.send("Content-Type: text/html;\r\n\r\n".encode())
                    self.request.send(body.encode())
                elif path.endswith("css"):
                    body = open("./www"+path,'r').read()
                    self.request.send("HTTP/1.1 200 OK\r\n".encode())
                    self.request.send("Content-Type: text/CSS;\r\n\r\n".encode())
                    self.request.send(body.encode())
                
                else: 
                    if path.endswith('/') : 
                        path += "index.html"
                        if open("./www"+path,'r').read():
                            body = open("./www"+path,'r').read()
                            self.request.send("HTTP/1.1 200 OK\r\n".encode())
                            self.request.send("Content-Type: text/html;\r\n\r\n".encode())
                            self.request.send(body.encode())
                        else: self.request.send(b"HTTP/1.0 404 Not Found") 
                    else:
                        path += "/index.html"
                        if open("./www"+path,'r').read():
                            body = open("./www"+path,'r').read()
                            self.request.send("HTTP/1.1 301 Moved Permanently\r\n".encode())
                            self.request.send("Content-Type: text/html;\r\n\r\n".encode())
                            self.request.send(body.encode())
                        else: self.request.send(b"HTTP/1.0 404 Not Found") 
            except:
                self.request.send(b"HTTP/1.0 404 Not Found")    
        else:
            self.request.send(b"HTTP/1.1 405 Methon Not Allowed")
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
