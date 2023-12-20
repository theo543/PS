import numpy as np
from threading import Thread, current_thread
from multiprocessing import cpu_count
from queue import Empty, Queue
from sys import argv

def launch_threads(batch: int) -> Queue:
    channel = Queue(maxsize=cpu_count() * 10)
    threads = [Thread(target=thread, args=(batch, channel)) for _ in range(cpu_count())]
    for t in threads:
        t.daemon = True
        t.start()
    return channel


def thread(batch: int, channel: Queue) -> None:
    gen = np.random.default_rng()
    vals_buf = np.empty(batch)
    while True:
        gen.random(size=batch, out=vals_buf)
        np.sin(vals_buf, out=vals_buf)
        channel.put(vals_buf.sum())

def estimate_forever():
    sample_sum = 0
    sample_count = 0
    batch = 50_000_000

    channel = launch_threads(batch)

    def update_status(end='\r'):
        print(f"Current estimation: {sample_sum / sample_count:.10f}, from {sample_count} samples", end=end)

    try:
        while True:
            sample_sum += channel.get()
            sample_count += batch
            update_status()
    except KeyboardInterrupt:
        update_status('\n')

def check_accuracy_forever():
    batch = 250_000
    max_error = np.power(1/10, 3)
    required_accuracy_rate = 0.95
    expected_value = 1 - np.cos(1)

    channel = launch_threads(batch)

    times_accurate = 0
    times = 0
    def update_status(end='\r'):
        accuracy = times_accurate/times
        is_ok = '✅' if accuracy >= required_accuracy_rate else '❌'
        print(f"Accuracy rate of {batch} samples ~= {accuracy*100:.5f}% ~= {times_accurate}/{times} {is_ok}", end=end)

    try:
        while True:
            t_sum = channel.get()
            estimation = t_sum / batch
            if abs(expected_value - estimation) < max_error:
                times_accurate += 1
            times += 1
            update_status()            
    except KeyboardInterrupt:
        update_status('\n')

def usage():
    print("Usage: python ex1.py (estimate|accuracy)")
    exit(1)

def main():
    if len(argv) == 1: usage()
    elif argv[1] == 'estimate':
        estimate_forever()
    elif argv[1] == 'accuracy':
        check_accuracy_forever()
    else: usage()

if __name__ == "__main__":
    main()
