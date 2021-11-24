from chatlib import *

print(split_data("username#password", 1))
print(split_data("user#name#pass#word", 2))
print(split_data("username", 2))

print(join_data(["username", "password"]))
print(join_data(["question", "ans1", "ans2", "ans3", "ans4", "correct"]))


print(build_message("LOGIN", "aaaa#bbbb"))
print(build_message("LOGIN", "aaaabbbb"))
print(build_message("LOGIN", ""))
print(build_message("0123456789ABCDEFGH", ""))
print(build_message("A", "A"*(MAX_DATA_LENGTH+1)))


print(parse_message("LOGIN           |0009|aaaa#bbbb"))
print(parse_message("LOGIN           |   9|aaaa#bbbb"))
print(parse_message("LOGIN           $   9|aaaa#bbbb"))
print(parse_message("LOGIN           |   z|aaaa"))

print(build_message("LOGIN", "user#pass"))
print(parse_message("LOGIN          |  8|user#pass"))

