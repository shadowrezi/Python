from time import perf_counter
from multiprocessing import Process, freeze_support
from add import rust_process

if __name__ == '__main__':
    try:
        freeze_support()

        rust_process = Process(target=rust_process)
        rust_process.start()

        start = perf_counter()

        x = []

        for i in range(28_000_000):
            x.append(12345 * i)

        py = perf_counter() - start
        print(py)
        print('^^^PYTHON^^^')
        input('>>>')
    finally:
        rust_process.terminate()
        rust_process.join()
