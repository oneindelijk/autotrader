
import appdirs
import shutil
from utils.at_exceptions import MissingParameter

def get_mysql_secrets(cfgname):
    cfgpath = shutil.os.path.join(appdirs.user_config_dir(),cfgname )
    if not shutil.os.path.exists(cfgpath):
        raise FileNotFoundError('Expecting a config file with user and password in {}'.format(cfgpath))
    with open(cfgpath) as FD:
        secrets_raw = FD.read()
    secret_dict = {}
    for secret_line in secrets_raw.splitlines():
        if 'password' in secret_line.lower():
            secret_dict['password'] = secret_line.split('=')[1].strip(' ')
        if 'user' in secret_line.lower():
            secret_dict['user'] = secret_line.split('=')[1].strip(' ')
        if 'host' in secret_line.lower():
            secret_dict['host'] = secret_line.split('=')[1].strip(' ')
        if 'port' in secret_line.lower():
            secret_dict['port'] = secret_line.split('=')[1].strip(' ')
        if 'django_key' in secret_line.lower():
            key = secret_line[secret_line.find(' = ') + 3:]
            secret_dict['django_key'] = key
    if not 'user' in secret_dict or not 'password' in secret_dict:
        raise MissingParameter("Expecting both user and password in file. Password may be empty")
    else:
        return secret_dict