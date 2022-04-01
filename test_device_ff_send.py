import zmq
import time

context = zmq.Context()

sock_sub = context.socket(zmq.SUB)
sock_pub = context.socket(zmq.PUB)

sock_pub.connect("tcp://smacsystem.com:5556")
sock_sub.connect("tcp://smacsystem.com:5572")

N = 0
while True:
    #data = sock_sub.recv()
    #print(data)
    N = 1-N
    print("sending {}".format(N))
    data = '# {"5":"D999", "6":"D1", "7":"0", "K": "P0", "L":"0", "N":"' + str(N) +'"}\n'
    sock_pub.send(data.encode("utf-8"))
    time.sleep(5)
