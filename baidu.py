#coding=utf-8

import time 
import threading 
import Queue
import requests
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Referer' : 'http://www.google.com',
    'Cookie': 'whoami=wyscan_dirfuzz',
    }
threads_count = 10
#search_url = 'https://www.baidu.com/s?wd=[keyword]&pn=0&oq=test&tn=baiduhome_pg&ie=utf-8&usm=1&rsv_idx=2&rsv_pq=e4898687000090e5&rsv_t=7498TKRyJmN3O29jzKMSPeCjSIryB6PKiuhLvYDOTBJGsqwDCFdZF3oxzqSa1Xjbofrt'
search_url_start = 'https://www.baidu.com/s?wd='
search_url_end = '&tn=baiduhome_pg&ie=utf-8&usm=1&rsv_idx=2&rsv_pq=e4898687000090e5&rsv_t=7498TKRyJmN3O29jzKMSPeCjSIryB6PKiuhLvYDOTBJGsqwDCFdZF3oxzqSa1Xjbofrt'

class BaiduScan(threading.Thread): 
    def __init__(self, queue): 
        threading.Thread.__init__(self)
        self._queue = queue 

    def run(self):
        while not self._queue.empty():
            try:
                msg = self._queue.get_nowait() 
                r = requests.get(url=msg,headers=headers)
                content = r.text
                print len(content)
            except Exception,e:
                print e
                break

def search(keyword):
    queue = Queue.Queue()
    for i in range(0,810,10):
        queue.put(search_url_start+keyword+'&pn='+str(i)+search_url_end)

    threads = []
    for i in xrange(threads_count):
        threads.append(BaiduScan(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        search(sys.argv[1])
        sys.exit(0)
    else:
        print ("usage: %s keyword" % sys.argv[0])
        sys.exit(-1)
