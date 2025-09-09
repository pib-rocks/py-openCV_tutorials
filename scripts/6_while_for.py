#!/usr/bin/env python3
"""
Demo 6: Explaining while and for loops in Python.

What you'll learn:
- How a while loop works (runs until a condition is false)
- How a for loop works (iterates over a sequence of numbers)
- Common patterns: counting up, counting down, skipping with 'continue',
  and stopping early with 'break'
"""

def while_demo():
    print("=== While Loop Demo ===")
    # Start with a counter variable
    counter = 1
    # Loop while the counter is <= 5
    while counter <= 5:
        print("Counter is:", counter)
        counter += 1  # Increase counter each time
    print("Done with while loop.\n")

def for_demo():
    print("=== For Loop Demo ===")
    # for loop iterates directly over a sequence
    for i in range(1, 6):  # numbers 1 through 5
        print("i is:", i)
    print("Done with for loop.\n")

def extra_examples():
    print("=== Extra Loop Examples ===")
    # Counting down
    for i in range(5, 0, -1):
        print("Countdown:", i)
    print("Lift off!\n")

    # Using continue to skip numbers
    for i in range(1, 6):
        if i == 3:
            print("Skipping 3...")
            continue
        print("i is:", i)
    print()

    # Using break to stop early
    for i in range(1, 10):
        print("i is:", i)
        if i == 5:
            print("Breaking the loop at 5.")
            break
    print("Loop stopped.\n")

def main():
    while_demo()
    for_demo()
    extra_examples()

if __name__ == "__main__":
    main()
