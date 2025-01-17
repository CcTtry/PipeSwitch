import sys
import time
import struct
import statistics

from task.helper import get_data
from util.utils import TcpClient, timestamp

def send_request(client, task_name, data):
    timestamp('client', 'before_request_%s' % task_name)

    # Serialize data
    task_name_b = task_name.encode()
    task_name_length = len(task_name_b)
    task_name_length_b = struct.pack('I', task_name_length)

    if data is not None:
        data_b = data.numpy().tobytes()
        length = len(data_b)
    else:
        data_b = None
        length = 0
    length_b = struct.pack('I', length)
    timestamp('client', 'after_inference_serialization')

    # Send Data
    client.send(task_name_length_b)
    client.send(task_name_b)
    client.send(length_b)
    if data_b is not None:
        client.send(data_b)
    timestamp('client', 'after_request_%s' % task_name)

def recv_response(client):
    '''
    只接收数据，并解码。不对结果数据进行其他处理
    '''
    reply_b = client.recv(4)
    reply = reply_b.decode()
    timestamp('client', 'after_reply')

def close_connection(client):
    model_name_length = 0
    model_name_length_b = struct.pack('I', model_name_length)
    client.send(model_name_length_b)
    timestamp('client', 'close_connection')

def main():
    '''
    1. 先执行training 的工作，然后在scheduling_cycle的空隙执行推理任务
    2. 统计在给定的scheduling_cycle空隙中，执行的任务数量，即吞吐量
    '''
    model_name = sys.argv[1]
    batch_size = int(sys.argv[2])
    scheduling_cycle = int(sys.argv[3])

    task_name_inf = '%s_inference' % model_name
    task_name_train = '%s_training' % model_name

    # Load image
    data = get_data(model_name, batch_size)

    #latency_list = []
    throughput_list = []
    for _ in range(20):
        # Send training request
        client_train = TcpClient('localhost', 12345)
        send_request(client_train, task_name_train, None)
        time.sleep(scheduling_cycle)

        # Connect
        client_inf = TcpClient('localhost', 12345)
        timestamp('client', 'after_inference_connect')

        #count
        inference_count = 0
        time_count = scheduling_cycle
        while (time_count > 0):
            time_1 = time.time()

            # Send inference request
            send_request(client_inf, task_name_inf, data)

            # Recv inference reply
            recv_response(client_inf)
            time_2 = time.time()
            time_count -= (time_2 - time_1)

            #If time exceeds, do not count this iteration
            if (time_count > 0):
                inference_count += 1
            

        throughput_list.append(inference_count)
        #print(inference_count)


        time.sleep(1)
        recv_response(client_train) 
        close_connection(client_inf)
        close_connection(client_train)
        time.sleep(1)
        timestamp('**********', '**********')

    print()
    print()
    print()
    print(throughput_list)
    stable_throughput_list = throughput_list[10:]
    #print (stable_throughput_list)
    value = (statistics.mean(stable_throughput_list)) / scheduling_cycle
    print ('Throughput: %f  (stdev: %f)' % (value, 
                                           statistics.stdev(stable_throughput_list)))

if __name__ == '__main__':
    main()
