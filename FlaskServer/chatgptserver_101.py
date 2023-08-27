import threading
import msvcrt
import importlib

# Import the routes module explicitly
import routes

from werkzeug.serving import make_server
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)

    def run(self):
        print('Starting server...')
        
        print(' * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)')
        self.server.serve_forever()

    def shutdown(self):
        print('Stopping server...')
        self.server.shutdown()

def wait_for_key():
    while True:
        
        if msvcrt.kbhit() and msvcrt.getch() == b'r':
            print('Reloading...')
            reload_routes()

def start_server():
    print('Starting...')
    server = ServerThread(app)
    server.start()

def stop_server():
    print('Shutting down...')
    global server
    server.shutdown()

@app.route('/')
def server_status_route():
    reload_routes()
    return jsonify(routes.server_status())

@app.route('/helloworld')
def hello_world_route():
    reload_routes()
    return routes.hello_world()

@app.route('/history', methods=['GET'])
def get_history_route():
    return jsonify(routes.get_history())

@app.route('/execute', methods=['POST'])
def execute_code_route():
    code = request.json.get('code')
    return jsonify(routes.execute_code(code))

@app.route('/posts/<int:id>', methods=['GET'])
def get_post_route(id):
    print('Getting posts...')
    result, status_code = routes.get_post(id)
    return jsonify(result), status_code

def reload_routes():
    # Reload the entire module
    importlib.reload(routes)

if __name__ == '__main__':
    start_server()
    wait_for_key()
