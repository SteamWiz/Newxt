#!/usr/bin/env python3
"""
Sample Python file for testing the replace command.
"""

def greet(name):
    """Greet someone by name."""
    return f"Hello, {name}!"

def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

def main():
    """Main function."""
    print(greet("World"))
    result = calculate_sum(5, 3)
    print(f"The sum is: {result}")

if __name__ == "__main__":
    main()
