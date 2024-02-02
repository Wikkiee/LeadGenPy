import psutil

def get_network_usage():
    network_usage = psutil.net_io_counters()
    return network_usage.bytes_sent + network_usage.bytes_recv
