import re
import shutil
from os import listdir
from os.path import isfile, join, getmtime
from git.repo import Repo
import logging

#numeric_level = getattr(logging, loglevel.upper(), None)
#if not isinstance(numeric_level, int):
#    raise ValueError('Invalid log level: %s' % loglevel)

logging.basicConfig(filename='/var/log/configer.log', filemode='a', 
        format='%(asctime)s %(message)s', level=logging.INFO)

mypath = "/home/ftp/cfg"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#logging.debug(f'Values {sorted(onlyfiles)}')


hostname = re.compile('(.*[A-z0-9])-[-\.]?([A-Za-z]{3}--?\d\d?-202\d)-(\d\d-\d\d-\d\d)-MSK-(\d+)$',
                      re.IGNORECASE)
configs = {}

for file in onlyfiles:
    m = hostname.match(file)
    if m:
        logging.debug(f'Values {m.group(1), m.group(2),m.group(3), m.group(4)}')
        config = {
                'file': file,
                'hostname': m.group(1),
                'index': m.group(4),
                'time': getmtime(join(mypath, file))
        }
        if configs.get(config['hostname']) == None:
            configs[config['hostname']] = config
        else:
            if int(config['time']) > int(configs[config['hostname']]['time']):
                configs[config['hostname']] = config
    else:
        logging.warning(f"Doesn't match, {file}")

for key in configs:
    src = join(mypath, configs[key]['file'])
    dst = join(mypath, 'rep', configs[key]['hostname'])
    shutil.copyfile(src, dst)
    logging.debug(dst)

repo = Repo(join(mypath, 'rep'))
if len(repo.untracked_files) > 0:  # retrieve a list of untracked files
    repo.index.add(repo.untracked_files)

if repo.is_dirty():  # check the dirty state
    repo.git.add(update=True)
    repo.index.commit('script commit')
    origin = repo.remote('origin')
    origin.push()
    logging.info('dirty')
else:
    logging.info('clean')
