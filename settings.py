log = {
    'log_max_bytes': 5 * 1024 * 1024,  # 5M
    'backup_count': 10,
    'log_path': {
        'logger': 'log/files/server.log',
    }
}
import os
host_port = 6789
data_dir = os.getcwd() + "/data/"
