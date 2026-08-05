from redis import Redis
from rq import Queue
# from utils.config import REDIS_HOST, REDIS_PORT 

redis_connection = Redis(host="valkey", port=6379)
q = Queue(connection=redis_connection)