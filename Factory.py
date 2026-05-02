import threading
import random
import time

class Worker:

    def __init__(self, thread_id, numbers, equation, shared_state):
        self.thread_id = thread_id
        self.numbers = numbers
        self.equation = equation
        self.shared_state = shared_state

    def run(self):
        print(f"Thread {self.thread_id} started")
        for num in self.numbers:
            with self.shared_state["lock"]:
                if self.shared_state["found"]:
                    break

                if self.equation(num):
                    self.shared_state["found"] = True
                    self.shared_state["result"] = num
                    print(f"Solution found by Thread {self.thread_id}: x = {num}")
                    break

        print(f"Thread {self.thread_id} finished")


class WorkerFactory:
    @staticmethod
    def create_worker(thread_id, numbers, equation, shared_state):
        return Worker(thread_id, numbers, equation, shared_state)

def generate_equation():
    a = random.randint(1, 5)
    b = random.randint(1, 10)
    x_solution = random.randint(1, 100)
    target = a * x_solution + b

    def equation(x):
        return a * x + b == target

    print(f"Equation: {a}x + {b} = {target}")
    return equation, x_solution


def main():
    # Start recording the time
    start_time = time.time()

    equation, real_solution = generate_equation()
    numbers = random.sample(range(1, 200), 39)
    numbers.append(real_solution)
    random.shuffle(numbers)
    chunks = [numbers[i:i+10] for i in range(0, 40, 10)]
    shared_state = {
        "found": False,
        "result": None,
        "lock": threading.Lock()
    }

    threads = []
    for i in range(4):
        worker = WorkerFactory.create_worker(
            thread_id=i + 1,
            numbers=chunks[i],
            equation=equation,
            shared_state=shared_state
        )

        t = threading.Thread(target=worker.run)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    execution_time = end_time - start_time

    print("\nFinal Result:", shared_state["result"])
    print(f"Total Run Time: {execution_time:.4f} seconds")

if __name__ == "__main__":
    main()