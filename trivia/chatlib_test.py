import chatlib


def check_build(input_cmd, input_data, expected_output):
	print("Input: ", input_cmd, input_data, "\nExpected output: ", expected_output)
	try:
		output = chatlib.build_message(input_cmd, input_data)
	except Exception as e:
		output = "Exception raised: " + str(e)
	
	if output == expected_output:
		print(".....\t SUCCESS")
	else:
		print(".....\t FAILED, output: ", output)


def check_parse(msg_str, expected_output):
	print("Input: ", msg_str, "\nExpected output: ", expected_output)

	try:
		output = chatlib.parse_message(msg_str)
	except Exception as e:
		output = "Exception raised: " + str(e)
	
	if output == expected_output:
		print(".....\t SUCCESS")
	else:
		print(".....\t FAILED, output: ", output)		


def main():

	# BUILD
	
	# Valid inputs
	# Normal message
	check_build("LOGIN", "aaaa#bbbb", "LOGIN           |0009|aaaa#bbbb")
	check_build("LOGIN", "aaaabbbb", "LOGIN           |0008|aaaabbbb")
	# Zero-length message
	check_build("LOGIN", "", "LOGIN           |0000|")
	
	# Invalid inputs
	# cmd too long
	check_build("0123456789ABCDEFG", "", None)
	# msg too long
	check_build("A", "A"*(chatlib.MAX_DATA_LENGTH+1), None)

	# PARSE
	
	# Valid inputs
	check_parse("LOGIN           |   9|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
	check_parse(" LOGIN          |   9|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
	check_parse("           LOGIN|   9|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
	check_parse("LOGIN           |9   |aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
	check_parse("LOGIN           |  09|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
	check_parse("LOGIN           |0009|aaaa#bbbb", ("LOGIN", "aaaa#bbbb"))
	check_parse("LOGIN           |9   | aaa#bbbb", ("LOGIN", " aaa#bbbb"))
	check_parse("LOGIN           |   4|data", ("LOGIN", "data"))

	# Invalid inputs
	check_parse("", (None, None))
	check_parse("LOGIN           x	  4|data", (None, None))
	check_parse("LOGIN           |	  4xdata", (None, None))
	check_parse("LOGIN           |	 -4|data", (None, None))
	check_parse("LOGIN           |	  z|data", (None, None))
	check_parse("LOGIN           |	  5|data", (None, None))

	print(chatlib.split_data("username#password", 1))
	print(chatlib.split_data("user#name#pass#word", 2))
	print(chatlib.split_data("username", 2))

	print(chatlib.join_data(["username", "password"]))
	print(chatlib.join_data(["question", "ans1", "ans2", "ans3", "ans4", "correct"]))

	print(chatlib.build_message("LOGIN", "aaaa#bbbb"))
	print(chatlib.build_message("LOGIN", "aaaabbbb"))
	print(chatlib.build_message("LOGIN", ""))
	print(chatlib.build_message("0123456789ABCDEFGH", ""))
	print(chatlib.build_message("A", "A"*(chatlib.MAX_DATA_LENGTH+1)))

	print(chatlib.parse_message("LOGIN           |0009|aaaa#bbbb"))
	print(chatlib.parse_message("LOGIN           |   9|aaaa#bbbb"))
	print(chatlib.parse_message("LOGIN           $   9|aaaa#bbbb"))
	print(chatlib.parse_message("LOGIN           |   z|aaaa"))

	print(chatlib.build_message("LOGIN", "user#pass"))
	print(chatlib.parse_message("LOGIN          |  8|user#pass"))


if __name__ == '__main__':
	main()
