from datetime import datetime
import hashlib

def get_hash(text_for_hash):
    text_for_hash = str(datetime.now()) + text_for_hash
    hash = hashlib.sha256(text_for_hash.encode()).hexdigest()[:10]

    return hash
