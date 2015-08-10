from fabric.api import *

def reset():
    local("rm -rvf proxy_*")
    
def clean():
    local("find . -name *.pyc | xargs -I {} rm -vf {}")
    local("find . -name *~    | xargs -I {} rm -vf {}")

def push():
    local("git commit -a")
    local("git push")
