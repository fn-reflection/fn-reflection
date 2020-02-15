import xxhash
import cloudpickle

def fastdigest(obj):
    s = cloudpickle.dumps(obj)
    return xxhash.xxh64(s).hexdigest()