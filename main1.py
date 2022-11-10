import threading
import time

if __name__ == 'main1':

    def task(i):
        print(f"Task {i} starts for {i+1} second(s)")
        time.sleep(i+1)
        print(f"Task {i} ends")

    start = time.perf_counter()

    T = []
    for i in range(100):
        T.append(threading.Thread(target=task, args=[i]))

    for i in range(len(T)):
        T[i].start()

    for i in range(len(T)):
        T[i].join()

    end = time.perf_counter()

    print(f"Tasks ended in {round(end - start, 2)} second(s)")