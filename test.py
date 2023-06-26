import re 

def expand_string(reg_exp, func_name):
    def expanded_string(string):
        if re.match(reg_exp, string):
            return func_name
        else:
            return None
    
    return expanded_string

def hello():
    print("Hello, world!")

def goodbye():
    print("Goodbye, world!")

dictionary_scheme = {
    r"he.*o": "hello",
    r"g.*dbye": "goodbye"
}

LOCATOR = {
    "LOGINFORM" : ".login-form",
    "email" : lambda x : LOCATOR["LOGINFORM"], 
    "password" : 'password',
    "usreprofile" : '.header-topbar .user-dropdown',
    "err_msg" : ".error"
}

print(f'emil = {LOCATOR["email"]("sfdsf")}')

# for key, value in dictionary_scheme.items():
#     expanded = expand_string(key, value)
#     if expanded : 
#         globals()[expanded("hello")]()
#         break
    # expanded("hello")

# def my_function():
#     print("Hello, World!")

# # Assign the function name to a string
# function_name = "my_function"

# # Call the function using eval()
# eval(function_name + "()")  # Output: "Hello, World!"

# # Call the function using globals()
# globals()[function_name]()  # Output: "Hello, World!"

# # Call the function using locals()
# locals()[function_name]()  # Output: "Hello, World!"
