import thread
import pickle
import SocketServer

SENSOR_SERVER_PORT = 8082
ACTION_SERVER_PORT = 8083

def run_sensor_server(sensor_comp):
    class TCPSensorHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            self.data = self.request.recv(1024).strip()
            #print "{} wrote:".format(self.client_address[0]), self.data
            self.request.sendall(pickle.dumps(sensor_comp.get_server_response()))
            
    HOST, PORT = "", SENSOR_SERVER_PORT
    server = SocketServer.TCPServer((HOST, PORT), TCPSensorHandler)
    print "runnning server", HOST, PORT
    server.serve_forever()
    
def run_action_server(action_comp):
    import SocketServer
    class TCPActionHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            self.data = self.request.recv(1024).strip()
            #print "{} wrote:".format(self.client_address[0]), self.data
            action_comp.set_client_request(pickle.loads(self.data))
            self.request.sendall("ok")
            
    HOST, PORT = "", ACTION_SERVER_PORT
    server = SocketServer.TCPServer((HOST, PORT), TCPActionHandler)
    print "runnning server", HOST, PORT
    server.serve_forever()
    

def run_brainsimulator_server_async(sensor_comp, action_comp):
    try:
        thread.start_new_thread(run_sensor_server, (sensor_comp,) )
        thread.start_new_thread(run_action_server, (action_comp,) )
    except:
        print "Error: unable to start thread"
