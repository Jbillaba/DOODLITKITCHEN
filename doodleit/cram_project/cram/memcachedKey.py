from django.utils.encoding import smart_str

def _smart_key(key):
    return smart_str(''.join([c for c in key if ord(c) > 32 and ord(c) != 127]))

def make_key(key, key_prefix, version):
    return ':'.join([key_prefix, str(version), _smart_key(key)])[:250]