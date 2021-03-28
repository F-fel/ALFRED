import socket
import threading
import struct
from vec3 import Vec3
from enum import Enum
from drone import Drone

import sys
import os

# Add paths toward dependecies in different subdirectories
sys.path.append(os.path.abspath('./src/map'))
from data_accumulator import MapObservationAccumulator

class PacketType(Enum):
    TX = 0
    POSITION = 1
    ATTITUDE = 2
    VELOCITY = 3
    DISTANCE = 4
    ORIENTATION = 5


class ArgosServer() : 
    #server_address =  socket.getaddrinfo('localhost', 8))
    
    
    def __init__(self, id, port):
        self.drone_argos = Drone()
        self.data_received = None
        self.sent_data = None
        self.point = Vec3(0,0,0)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', port))
        
        # listen for incoming connections (server mode) with one connection at a time
        self.sock.listen()

        # Initialize the live map handler
        self.map_observation_accumulator = MapObservationAccumulator()

    def waiting_connection(self):
        # wait for a connection
        print ('waiting for a connection')
        self.connection, self.client_address = self.sock.accept()

        # show who connected to us
        print ('connection from', self.client_address)
        self.receive_data()

    def send_data(self, packet, format_packer):
        data = struct.pack(format_packer, packet)
        self.connection.send(data)
        print('data send ')
        print(data)

        
    def receive_data(self):
        print('entree receive_data')
        while True:
            self.connection.settimeout(5.0)
            self.data_received = self.connection.recv(16)   
            self.data_received += bytearray(16 - len(self.data_received)) 

            if PacketType(self.data_received[0]) == PacketType.TX:
                (packet_type, state, vbattery, is_led_activated, a, b, c) = struct.unpack("<iif?bbb", self.data_received)
                self.drone_argos._vbat = vbattery

            elif PacketType(self.data_received[0]) == PacketType.POSITION:
                (packet_type, x, y, z) = struct.unpack("<ifff", self.data_received)
                self.drone_argos.currentPos.x = x
                self.drone_argos.currentPos.y = y
                self.drone_argos.currentPos.z = z
                self.map_observation_accumulator.receive_position(x, y, z)

            elif PacketType(self.data_received[0]) == PacketType.VELOCITY:
                (packet_type, x_speed, y_speed, z_speed) = struct.unpack("<ifff", self.data_received)
                self.drone_argos._speed.x = x_speed
                self.drone_argos._speed.y = y_speed
                self.drone_argos._speed.z = z_speed
                
            elif PacketType(self.data_received[0]) == PacketType.DISTANCE:
                (packet_type, front, back, up, left, right, zrange) = struct.unpack("<ihhhhhh", self.data_received)
                self.drone_argos.sensors.front = front
                self.drone_argos.sensors.back = back
                self.drone_argos.sensors.up = up
                self.drone_argos.sensors.left = left
                self.drone_argos.sensors.right = right
                self.drone_argos.sensors.down = zrange

            elif PacketType(self.data_received[0]) == PacketType.ORIENTATION:
                (packet_type, pitch, roll, yaw) = struct.unpack("<ifff", self.data_received)
                self.drone_argos.sensors.back = roll
                self.drone_argos.sensors.front = pitch
                self.drone_argos.sensors.up = yaw
                

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()  
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
    
    def start_receive_data(self):
        t2 = threading.Thread(target=self.receive_data, args=(queue), name="receive_data_{}".format(id))
        t2.start
    
    