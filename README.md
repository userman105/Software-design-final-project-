This project aims to solve a simple generated equation using 4 threads, 
where each thread checks a subset of values to find the correct solution.
The same problem is implemented using three different design patterns:

Singleton Pattern:
A single shared instance manages the solving process across all threads.

Prototype Pattern:
Threads operate on cloned worker objects derived from a prototype.

Factory Pattern:
Object creation is handled through a dedicated factory class.

Common Features:
Random equation generation (e.g., ax + b = target)
Array of 40 numbers 
4 threads, each processing 10 numbers
Thread-safe solution detection using locks
Early termination when the solution is found
