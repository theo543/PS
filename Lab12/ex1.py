import numpy as np
from threading import Thread, current_thread
from multiprocessing import cpu_count
from queue import Empty, Queue

def thread(batch: int, channel: Queue) -> None:
    gen = np.random.default_rng()
    vals_buf = np.empty(batch)
    while True:
        gen.random(size=batch, out=vals_buf)
        np.sin(vals_buf, out=vals_buf)
        channel.put((vals_buf.sum(), batch))

def main():
    sample_sum = 0
    sample_count = 0
    batch = 50_000_000

    def update_status(end='\r'):
        print(f"Current estimation: {sample_sum / sample_count:.10f}, from {sample_count} samples", end=end)

    channel = Queue(maxsize=0)
    threads = [Thread(target=thread, args=(batch, channel)) for _ in range(cpu_count())]
    for t in threads:
        t.daemon = True
        t.start()

    try:
        while True:
            try:
                (t_sum, t_count) = channel.get(timeout=1)
            except Empty:
                continue
            sample_sum += t_sum
            sample_count += t_count
            update_status()
    except KeyboardInterrupt:
        update_status('\n')

if __name__ == "__main__":
    main()
