"""
Promethium
=========

Module with useful tidbits
"""
import os
import threading
import urllib
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from datetime import datetime

def return_type(data):
    """
    return_type:
    Returns the "true type" of data
    Example:
    print(return_type("5"))   # Output: int(5)
    print(return_type("abc")) # Output: str("abc")
    print(return_type("4.5")) # Output: float(4.5)
    """
    try:
        num = float(data)
        if num.is_integer():
            return int(num)
        return num
    except ValueError:
        return data
class col:
    """
    Color class

    print(col.red + "This is red" + col.end)
    """
    black = "\033[0;30m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    brown = "\033[0;33m"
    blue = "\033[0;34m"
    purple = "\033[0;35m"   
    cyan = "\033[0;36m"
    light_gray = "\033[0;37m"
    dark_gray = "\033[1;30m"
    light_red = "\033[1;31m"
    light_green = "\033[1;32m"
    yellow = "\033[1;33m"
    light_blue = "\033[1;34m"
    light_purple = "\033[1;35m"
    light_cyan = "\033[1;36m"
    light_white = "\033[1;37m"
    bold = "\033[1m"
    faint = "\033[2m"
    italic = "\033[3m"
    underline = "\033[4m"
    blink = "\033[5m"
    negative = "\033[7m"
    crossed = "\033[9m"
    end = "\033[0m"

class aft:
    """
    Auto function threader

    aft(func).start()
    """
    def __init__(self, func):
        self.func = func
        self.params = None
        self.thread = threading.Thread(target=self.run_function)

    def type(self, *args):
        self.params = args
        return self

    def run_function(self):
        timenow = datetime.now().strftime("%H:%M:%S")
        print(col.blue + "[AFT]" + col.end + col.purple + f"====={timenow}×\n" + col.end)
        self.func()

    def start(self):
        self.thread.start()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global contents
        global dronename
        global script_dir
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(contents.encode('utf-8'))
        elif self.path == f'/{dronename}video.mp4':
            self.send_response(200)
            self.send_header('Content-type', 'video/mp4')
            self.end_headers()
            with open(f'{script_dir}/{dronename}video.mp4', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == f'/{dronename}audio.mp3':
            self.send_response(200)
            self.send_header('Content-type', 'audio/mpeg')
            self.end_headers()
            with open(f'{script_dir}/{dronename}audio.mp3', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

class md:
    """
    Silly little Murder Drones easter egg

    md("v").display()
    """
    def __init__(self, data):
        self.data = data

    def display(self, server_class=HTTPServer, handler_class=RequestHandler, port=6969):
        global contents
        global dronename
        global script_dir
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if self.data == "v":
            audio = "vaudio"
            video = "vvideo"
        else:
            audio = "cynaudio"
            video = "cynvideo"
        dronename = self.data
        contents = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + self.data + ''' core</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #000000;
        }
        video {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <video width="520" height="440" autoplay muted>
        <source src="''' + video + '''.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <audio autoplay>
        <source src="''' + audio + '''.mp3" type="audio/mpeg">
        Your browser does not support the audio tag.
    </audio>
</body>
</html>
        '''
        server_address = ('0.0.0.0', port)
        httpd = server_class(server_address, handler_class)
        webbrowser.open("127.0.0.1:6969")
        httpd.serve_forever()

class prmth(Exception):
    """
    Exception handler for Promethium-specific Errors
    """
    def __init__(self, typeof="Exception", err="ExcepRaised", message="PRMTH Raised"):
        self.message = message
        self.typeof = typeof
        self.err = err
    def __str__(self):
        if self.typeof is None:
            return str(col.red+ f"[prmth]" + col.end + f" {self.typeof}.{self.err}: {self.message}")
        else:
            return str(col.red+ f"[prmth]" + col.end + f" {self.typeof}.{self.err}: {self.message}")

class sckt:
    """
    Socket commands

    sckt(ip, port).get_content()
    sckt(ip, port).connect()
    The port defaults to 80
    """
    def __init__(self, data, port=80):
        self.data = data
        self.port = port
    
    def get_content(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.data, self.port))
            request = f"GET / HTTP/1.1\r\nHost: {self.data}\r\n\r\n"
            client_socket.send(request.encode())
            response = client_socket.recv(4096)
            return response.decode()
            client_socket.close()
        except ConnectionRefusedError:
            e = f'host "{self.data}" on port "{self.port}" refused your request'
            ename = "GetRefused"
            raise prmth(self.__class__.__name__, ename, e) from None
    def connect(self, shell=True):
        self.shell = shell
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.data, self.port))
            if self.shell == True:
                while True:
                    cmd = input("command: ")
                    client.send(cmd.encode())
                    data = client.recv(4096).decode()
        except ConnectionRefusedError:
            e = f'host "{self.data}" on port "{self.port}" refused your connection'
            ename = "ConRefused"
            raise prmth(self.__class__.__name__, ename, e) from None
