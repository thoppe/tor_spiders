from fabric.api import *

def reset():
    local("rm -rvf proxy_*")
    
def clean():
    local("find . -name *.pyc | xargs -I {} rm -vf {}")
    local("find . -name *~    | xargs -I {} rm -vf {}")

    
#db          fabfile.pyc         proxy_0  proxy_3  requirements.txt
#downloads   github_download.py  proxy_1  proxy_4  seralize_downloads.py
#fabfile.py  images              proxy_2  proxy_5  tor_spiders
