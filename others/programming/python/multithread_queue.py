http://bugs.python.org/issue12155

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

q = Queue()
threads = []
for i in range(num_worker_threads):
     t = Thread(target=worker)
     threads.append(t)
     t.start()

for item in source():
    q.put(item)

q.join()       # block until all tasks are done
for i in range(num_worker_threads):
    q.put(None)
for t in threads: t.join()
