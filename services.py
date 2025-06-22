import redis
import os

# Redis configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = os.environ.get('REDIS_DB', 0)

# initialise redis connection globally for the service module
r = None

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def init_redis():
	"""
	Initialises the Redis connection.
	This function should be called once when the Flask application starts up
	"""
	global r 
	if r is None:
		try:
			r = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, decode_responses=True)
			r.ping()
			print(f"connected to Redis at {REDIS_HOST} : {REDIS_PORT}")
		except Exception as e:
			print("Could not connect to Redis: ", e)


def base_encode(num, alphabet = BASE62_ALPHABET):
	"""
	encodes a number into a base62 string using the provided alphabet
	This is a generic base conversion function
	"""
	if num == 0:
		return alphabet[0]
	arr = []
	base = len(alphabet)
	while num>0:
		rem = num% base 
		arr.append(alphabet[rem])
		num //= base 
		arr.reverse()
		return "".join(arr)

def generate_and_store_url(long_url):
	"""
	Generates a unique short code for a long URL and stores the mapping in Redis.
	It uses an incrementing counter in Redis for uniqueness.
	Returns the generated short code.
	"""
	#increment a count in Redis
	new_id = r.incr('next_short_id')

	#convert the numeric id obtained from Redis to a base62 string
	short_code = base_encode(new_id)

	#store the mapping in Redis: short_code is the key, long_url is the value
	r.set(short_code, long_url)

	return short_code

def get_long_url(short_code):
	"""
	Retrieves the long URL associated with a short code from Redis.
	Returns the long URL string if found, otherwise returns None.
	"""
	if r is None:
		raise RuntimeError("Redis connection not initialized.") # Ensure Redis is connected
		
	# Use r.get(key) to retrieve the value associated with the short_code key.
	# Since decode_responses=True was set in Redis connection, this returns a string.
	return r.get(short_code)



















