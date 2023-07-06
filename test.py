import inspect

def read_function_lines(func):
    """
    inspect every line of code in function 'func' 
    then print it out. 
    """
    source_lines, _ = inspect.getsourcelines(func)
    for line in source_lines:
        print(line.strip())

# Example function
def example_function():
    # Code to be read
    print("Hello, world!")
    result = 2 + 2
    return result

import importlib.util
from pathlib import Path

module_path = Path("C:\\Mydata\\Automation\\VerifypytestBDD\\unittest\\test_withoutfeature.py")
module_name = module_path.stem
func_name = 'test_google'
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


    
#     # Import the module dynamically
# module = importlib.import_module("C:\\Mydata\\Automation\\VerifypytestBDD\\unittest\\test_withoutfeature")
# func_name = 'test_google'
# # Get the function by its name
# function = getattr(module, func_name)


func = getattr(module, func_name)
read_function_lines(func)
