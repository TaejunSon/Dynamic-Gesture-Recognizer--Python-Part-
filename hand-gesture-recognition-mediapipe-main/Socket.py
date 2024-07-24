import socket
import struct
import copy
from collections import deque
from model import PointHistoryClassifier
import time

host, port = "192.168.0.203", 25001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

classifier = PointHistoryClassifier()

def recv_all(sock, num_bytes):
    data = b''
    while len(data) < num_bytes:
        packet = sock.recv(num_bytes - len(data))
        if not packet:
            return None
        data += packet
    return data

def pre_process_point_history(point_history):
    temp_point_history = copy.deepcopy(point_history)
    pre_process = list(temp_point_history)
    base_x = pre_process[0]
    base_y = pre_process[1]
    for i in range(0, len(pre_process), 2):
        pre_process[i] -= base_x
        pre_process[i+1] -= base_y
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
        
try:
    sock.connect((host, port))
    point_history = deque(maxlen=16)  

    while True:
        #time.sleep(0.1)

        received_data = recv_all(sock, 8)

        if received_data:
            x, y = struct.unpack('ff', received_data)
            
            point_history.append(x)
            point_history.append(y)
           #print(f"Received: x={x}, y={y}")
            
            if len(point_history) == 16:
            
                result_index, confidence_score = classifier(pre_process_point_history(point_history))
                #print(f"Classification result: {result_index}, confidence: {confidence_score}")
                #Gesture_classify(result_index)
                #if (result_index == 4):
                 #   print("Up")
                #elif (result_index == 5):
                 #   print("Down")
               # if(result_index ==1):
                #    print("Clockwise")
                #if(result_index ==2):
                 #   print("Counter Clock")
                #elif(result_index == 6):
                 #   print("Right")
                #elif (result_index == 7):
                 #   print("Left")
                #else:
                    #print("-")
                sock.sendall(struct.pack('i', result_index))
                #point_history.popleft()
                #point_history.popleft()
            else:
                sock.sendall(struct.pack('i', 8))
        else:
            break

finally:
    sock.close()
