import threading
import random
import copy

class WorkerPrototype:
    def __init__(self):
        self.thread_id = None
        self.numbers = []
        self.equation = None
        self.shared_state = None

    def clone(self):
        return copy.deepcopy(self)

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


# Generate equation
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
    prototype = WorkerPrototype()
    threads = []
    for i in range(4):
        worker = prototype.clone()
        worker.thread_id = i + 1
        worker.numbers = chunks[i]
        worker.equation = equation
        worker.shared_state = shared_state

        t = threading.Thread(target=worker.run)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nFinal Result:", shared_state["result"])

if __name__ == "__main__":
    main()