from flask import Flask, request
from multiprocessing import Process, Queue
import multiprocessing
import redis
import random
import json
import datetime

r = redis.Redis(host='192.168.0.4', port=6379, password='123456')
json_stri = 'json-str.txt'
def load_model_results():
    # 读取模型结果并将其放入队列
    with open(json_stri, 'r', encoding='utf-8') as f:
        data_chunk = json.load(f)
    return data_chunk

data_chunk = load_model_results()
num_keys = 1000
num_processes = multiprocessing.cpu_count()
keys_per_process = num_keys // num_processes

app = Flask(__name__)
queue = Queue()

def feat_1(queue, loan_id, customer_id, create_time):
    #***feat_1处理逻辑输出dict***
    queue.put(result)

def write_to_redis1(result2, db_index):
    pipe = r.pipeline()
    for key, value in result2.items():
        pipe.set(f'{db_index}:{key}', value)
    pipe.execute()

def write_to_redis2(result2, db_index):
    pipe = r.pipeline()
    for key, value in result2.items():
        pipe.set(f'{db_index}:{key}', value)
    pipe.execute()

def get_random_keys(r, num_keys, pattern='*'):
    """
    从匹配特定模式的所有键中随机选择num_keys数量的键。
    """
    all_keys = r.keys(pattern=pattern)
    # 将二进制键解码为UTF-8字符串
    all_keys_decoded = [key.decode('utf-8') for key in all_keys]
    random_keys = random.sample(all_keys_decoded, min(num_keys, len(all_keys_decoded)))
    return random_keys

def get_keys_from_redis(queue, loan_id, customer_id, create_time):
    random_keys = get_random_keys(r, num_keys)
     # 使用pipeline一次性获取这些随机键的值
    with r.pipeline() as pipe:
        for key in random_keys:
            pipe.get(key)
        values = pipe.execute()
    # 由于返回的是一个列表，我们需要将bytes类型转换为str类型
    values = [value.decode('utf-8') if value else None for value in values]
    # 将键和对应的值组合成一个字典
    random_key_values = dict(zip(random_keys, values))
    queue.put(random_key_values)
    return random_key_values

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
    res = write_to_redis1(result2, 'db_0')
    res2 = write_to_redis2(result2, 'db_1')
    queue.put(data_chunk)
    return 'Data received'

@app.route("/customer", methods=['POST'])
def predict():
########################################################################################################################
    req_uid = request.json['req_uid'] if 'req_uid' in request.json.keys() else None
    loan_id = request.json['loan_id'] if 'loan_id' in request.json.keys() else None
    customer_id = request.json['customer_id'] if 'customer_id' in request.json.keys() else None
    create_time = request.json['create_time'] if 'create_time' in request.json.keys() else None
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    costSeconds = (end_time - start_time).seconds * 1.0

    print("#####begin_time is ", datetime.datetime.now())
    # 创建一个队列用于进程间通信
    queue = Queue()
    p1 = Process(target=get_keys_from_redis, args=(queue,loan_id, customer_id, create_time))
    p1.start()
    p1.join()
    
    # 获取所有键值对
    result_1 = get_keys_from_redis(queue,loan_id, customer_id, create_time)

    result = {**result_1}

    results = {
        'req_uid': req_uid,
        'customer_id': customer_id,
        'create_time': create_time[0:19],
        'code': float(0),
        'result': result,
        'description': 'success',
        'costSeconds': costSeconds,
        'finishTime': str(end_time)[0:19],
        'collectionResultDay': str(end_time)[0:10],
    }
    print("end_time is ######", datetime.datetime.now())
    return results


if __name__ == '__main__':
    # p = Process(target=worker, args=(queue,))
    # p.start()
    print("所有数据已从Redis获取并合并到result2字典中")
    app.run()
    