from flask import Flask, request
from multiprocessing import Process, Queue
import multiprocessing
import redis
import random
import json
import string

r = redis.Redis(host='192.168.0.4', port=6379, password='123456')
json_stri = 'json-str.txt'
def load_model_results():
    # 读取模型结果并将其放入队列
    with open(json_stri, 'r', encoding='utf-8') as f:
        data_chunk = json.load(f)
    return data_chunk

data_chunk = load_model_results()

app = Flask(__name__)
queue = Queue()
def generate_key_value_pairs(num_keys):
    return {f'key_{i}': ''.join(random.choices(string.ascii_letters + string.digits, k=10)) for i in range(num_keys)}

def feat1(data_chunk, db_index):
    pipe = r.pipeline()
    for key, value in data_chunk.items():
        pipe.set(f'{db_index}:{key}', value)
    pipe.execute()

def feat2(data_chunk, db_index):
    pipe = r.pipeline()
    for key, value in data_chunk.items():
        pipe.set(f'{db_index}:{key}', value)
    pipe.execute()

def worker(queue):
    while True:
        if not queue.empty():
            data = queue.get()
            # 处理数据
            print("Received data: ", data)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    print(data)
    #queue.put(data)
    num_keys = 100000
    num_processes = multiprocessing.cpu_count()
    keys_per_process = num_keys // num_processes
    res = feat1(data_chunk, 'db_0')
    res2 = feat2(data_chunk, 'db_1')
    queue.put(data_chunk)
    return 'Data received'
    
if __name__ == '__main__':
    p = Process(target=worker, args=(queue,))
    p.start()
    app.run()
