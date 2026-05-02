import threading
import random
import time

class SingletonSolver:
    instance = None
    lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls):
        with cls.lock:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
                cls.instance.found = False
                cls.instance.result = None
                cls.instance.result_lock = threading.Lock()
        return cls.instance

    def check_solution(self, x, equation):
        with self.result_lock:
            if self.found:
                return True

            if equation(x):
                self.found = True
                self.result = x
                print(f"Solution found: x = {x}")
                return True

        return False


def generate_equation():
    a = random.randint(1, 5)
    b = random.randint(1, 10)
    x_solution = random.randint(1, 100)
    target = a * x_solution + b

    def equation(x):
        return a * x + b == target

    print(f"Equation: {a}x + {b} = {target}")
    return equation, x_solution

def worker(thread_id, numbers, equation, solver):
    print(f"Thread {thread_id} started")

    for num in numbers:
        if solver.check_solution(num, equation):
            break

    print(f"Thread {thread_id} finished")


def main():
    start_time = time.time()

    equation, real_solution = generate_equation()
    numbers = random.sample(range(1, 200), 39)
    numbers.append(real_solution)
    random.shuffle(numbers)
    chunks = [numbers[i:i+10] for i in range(0, 40, 10)]

    solver = SingletonSolver()

    threads = []

    for i in range(4):
        t = threading.Thread(target=worker, args=(i+1, chunks[i], equation, solver))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    execution_time = end_time - start_time

    print("\nFinal Result:", solver.result)
    print(f"Total Run Time: {execution_time:.4f} seconds")

if __name__ == "__main__":
    main()