import socket
import struct
import copy
from collections import deque
from model import PointHistoryClassifier
import time

import csv
host, port = "192.168.0.203", 25001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#sock.settimeout(3.0)
classifier = PointHistoryClassifier()

delay_time = 0

def recv_all(sock, num_bytes):
    data = b''
    while len(data) < num_bytes:
        #try:
        packet = sock.recv(num_bytes - len(data))
        #except socket.timeout:
         #   print("Socket timeout")
          #  return None
        if not packet:
            return None
        data += packet
    return data

def pre_process_point_history(point_history):
    temp_point_history = copy.deepcopy(point_history)
    pre_process = []
    base_x = temp_point_history[0]
    base_y = temp_point_history[1]
    
    for i in range(len(temp_point_history)):
        #if i % 4 == 0 or i %4 == 1:
        pre_process.append(temp_point_history[i])
    for  i in range(len(pre_process)):
        if i%2 == 0:
            pre_process[i] -= base_x
        if i %2 ==1:
            pre_process[i] -= base_y
    pre_process[0] = 0 
    pre_process[1] = 0
    return pre_process

def Gesture_classify(index):
    if (result_index == 4):
        print("Up")
    elif (result_index == 5):
        print("Down")
    elif(result_index ==1):
        print("Clockwise")    
    elif(result_index ==2):
        print("Counter Clock")
    elif(result_index == 6):
        print("Right")
    elif (result_index == 7):
        print("Left")
def save_to_csv(point_history):
    with open('point_history.csv', mode = 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(point_history)        
try:
    sock.connect((host, port))
    print("Connet success")
    point_history = deque(maxlen=16)  

    while True:
        #received_data = recv_all(sock, 8)
        
        received_data = recv_all(sock, 8)
        if received_data:
            x, y = struct.unpack('ff', received_data)
            print("x position ", x)
            print("y position ", y)
            point_history.append(x)
            point_history.append(y)
            
            if len(point_history) == 16:
                result_index, confidence_score = classifier(pre_process_point_history(point_history))
                Gesture_classify(result_index)
                sock.sendall(struct.pack('i', result_index))

            else:
                sock.sendall(struct.pack('i', 8))
        else:
            break

finally:
    sock.close()
