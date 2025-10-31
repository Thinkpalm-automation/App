"""
Sample test file for demonstration
This file can be used to test the test_runner.py application
"""

def hello_world():
    """Simple function"""
    return "Hello, World!"

class SampleClass:
    """Sample class for testing"""
    
    def __init__(self):
        self.value = 44
    
    def get_value(self):
        """Get the value"""
        return self.value

if __name__ == "__main__":
    print(hello_world())
    obj = SampleClass()
    print(f"Value: {obj.get_value()}")

