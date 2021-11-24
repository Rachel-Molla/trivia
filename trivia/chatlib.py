# Protocol Constants

CMD_FIELD_LENGTH = 16   # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names


PROTOCOL_CLIENT = {
	"login_msg": "LOGIN",
	"logout_msg": "LOGOUT"
}
# .. Add more commands if needed


PROTOCOL_SERVER = {
	"login_ok_msg": "LOGIN_OK",
	"login_failed_msg": "ERROR"
}
# ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	cmd_len = len(cmd)
	data_len = len(data)
	if cmd_len <= CMD_FIELD_LENGTH and data_len <= MAX_DATA_LENGTH:
		cmd_spaces = " " * (CMD_FIELD_LENGTH - cmd_len)
		data_len_str = str(data_len)
		data_len_with_zeros = data_len_str.zfill(LENGTH_FIELD_LENGTH)
		full_msg = cmd + cmd_spaces + DELIMITER + data_len_with_zeros + DELIMITER + data
		return full_msg
	return ERROR_RETURN


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	data_arr = data.split(DELIMITER)
	if len(data_arr) == 3:
		cmd = data_arr[0].strip()
		if len(cmd) <= CMD_FIELD_LENGTH:
			msg_len_str = data_arr[1]
			if len(msg_len_str) == LENGTH_FIELD_LENGTH and msg_len_str.strip().isdigit():
				msg_len = int(msg_len_str)
				msg = data_arr[2]
				if len(msg) == msg_len and len(msg) <= MAX_DATA_LENGTH:
					return cmd, msg
	cmd = ERROR_RETURN
	msg = ERROR_RETURN
	return cmd, msg


def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	if msg.count(DATA_DELIMITER) == expected_fields:
		msg_arr = msg.split(DATA_DELIMITER)
		return msg_arr
	return ERROR_RETURN


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""
	msg = DATA_DELIMITER.join(msg_fields)
	return msg
