from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                     datetime.now())
def calc_recv_timestamp(recv_time_stamp, counter):
    for i  in range(len(counter)):
        counter[i] = max(recv_time_stamp[i], counter[i])
    return counter

def event(pid, counter):
    counter[pid] += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

def recv_message(pipe, pid, counter):
    counter[pid]+=1
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid)  + local_time(counter))
    return counter

def process_one(pipe12):
    pid = 0
    counter = [0 for i in range (3)]
    
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12,pid,counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12,pid,counter)
    
    print("Counter process A ", counter)

def process_two(pipe21, pipe23):
    pid = 1
    counter =[ 0 for i in range (3)]
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21,pid,counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)
    print("Counter process B ", counter)

def process_three(pipe32):
    pid = 2
    counter = [0 for i in range(3)]
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32,pid,counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32,pid,counter)
    print("Counter process C ", counter)

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()
    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two, 
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three, 
                       args=(threeandtwo,))

    process3.start()
    process2.start()
    process1.start()

    process3.join()
    process2.join()
    process1.join()




