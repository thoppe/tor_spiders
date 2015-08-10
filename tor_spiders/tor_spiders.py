from stem.util import term as XTERM
import stem.process

import requesocks
import urllib
import json
import itertools

import Queue
import threading
import time

def get_IP_address(session):
    url = 'https://api.ipify.org?format=json'
    r   = session.get(url)
    try:
        js = json.loads(r.text)
        return js["ip"]
    except Exception as Ex:
        err = "Could not read IP {}".format(Ex)
        return err

class tor_session(object):
    def __init__(self, PORT=9000, DATA_DIRECTORY="local"):

        self.PORT = PORT
        self.DIR  = DATA_DIRECTORY

        #Use Tor for both HTTP and HTTPS
        self.session = requesocks.session()

        socks_proxy  = 'socks5://localhost:{}'.format(self.PORT)
        self.session.proxies = {"http" :socks_proxy,
                                "https":socks_proxy}

        self.config = { 
            'SocksPort': str(self.PORT),
            'DataDirectory': self.DIR,
        }
           
        self.process = stem.process.launch_tor_with_config(
            config = self.config,
            init_msg_handler = self._output_init_line,
        )

        self.report_IP_address()
        self.validate_anonymity()

    def __del__(self):
        self.process.kill()       
        line = "Closing TOR connection {}".format(self.DIR)
        print line

    def validate_anonymity(self):
        if get_IP_address(self.session) == _local_IP:
            err = "TOR connection leaked IP! Exiting"
            raise ValueError(err)
        else:
            line = "  Local and TOR IP address differ, continuing"
            print XTERM.format(line, XTERM.Color.WHITE)

    def _output_init_line(self,line):
        if "Bootstrapped " in line:
            print XTERM.format(line, XTERM.Color.BLUE)
        #else:
        #    print XTERM.format(line, XTERM.Color.WHITE)

    def report_IP_address(self):
        IP = get_IP_address(self.session)
        line = "  Reported IP address {}".format(IP)
        print XTERM.format(line, XTERM.Color.GREEN)

class tor_requests(tor_session):
    def get(self, url, params=None):
        if params is None:
            params = {}
        return self.session.get(url, params=params)

def _generate_tor_req(item):
    return tor_requests(*item)

class tor_request_pool(object):

    def __init__(self, n=2,
                 storage_base = "proxy",
                 PORT_START=9005):
        
        self.T = []

        args = []
        for k in range(n):
            local_storage = "{}_{}".format(storage_base,k)
            port = PORT_START + k
            args.append( (port, local_storage) )

        ITR = itertools.imap(_generate_tor_req, args)
        self.Q = Queue.Queue()
        self.result = Queue.Queue()
        
        for k,proc in enumerate(ITR):
            self.T.append(proc)

        self.workers = itertools.cycle(self.T)

    def get(self, url, params=None):
        return self.workers.next().get(url, params)

    def put(self,url,params=None):
        self.Q.put((url,params))

    def session_worker(self, queue):
        queue_full = True
        while queue_full:
            try:
                # get your data off the queue, and do some work
                url,params = self.Q.get(False)
                data = self.get(url,params)
                self.result.put(data)
            except Queue.Empty:
                queue_full = False

    def download_queue(self):
        thread_count = len(self.T)
        for _ in range(thread_count):
            t = threading.Thread(target=self.session_worker,
                                 args=(self.Q,))
            t.start()

    def __iter__(self):
        self.download_queue()
        while not self.Q.empty():
            time.sleep(0.1)
            while not self.result.empty():
                yield self.result.get()
        while not self.result.empty():
            yield self.result.get()


_local_session = requesocks.session()
_local_IP      = get_IP_address(_local_session)
