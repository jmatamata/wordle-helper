from string import ascii_lowercase
import enchant
import random

# v = Valid
class LetterTracker:
	def __init__(self):
		self.letter_status = {}
		for c in ascii_lowercase:
			self.letter_status[str(c)] = 1
	def add_invalids(self, invalid_letter_list):
		for l in invalid_letter_list:
			if l in self.letter_status:
				self.letter_status.pop(l)
	def set_invalid(self, letter):
		if letter in self.letter_status:
			self.letter_status.pop(letter)
	def get_keys(self):
		return list(self.letter_status)
	def show(self):
		print(list(self.letter_status))
class WordleHelper:
	def __init__(self, file_name, length):
		self.file = open(file_name, "r")
		self.word_frame = {}
		for i in range(length):
			self.word_frame[str(i)] = LetterTracker()
		self.string_word_frame = ""
		self.argument_list = []
		self.en_dict = enchant.Dict("en_US")
	def parse_data(self):
		word_line = self.file.readline()
		letter_list = word_line.split(" ", len(self.word_frame) - 1)
		for i in range(len(letter_list)):
			letter_list[i] = (letter_list[i])[:1]
			temp_letter = letter_list[i]
			if temp_letter.isalpha():
				self.word_frame[str(i)] = temp_letter
		self.string_word_frame = "".join(letter_list)

		for line in self.file:
			constraint_data = line.split(":", 1)
			argument = constraint_data[0]
			if argument == "!":
				invalid_letter_data = constraint_data[1]
				invalid_letters = invalid_letter_data.split(",")
				for i in range(len(invalid_letters)):
					invalid_letters[i] = (invalid_letters[i])[:1]
				for key in self.word_frame:
					if type(self.word_frame[key]) == LetterTracker:
						self.word_frame[key].add_invalids(invalid_letters)
			elif argument.isalpha():
				self.argument_list.append(argument)
				invalid_at_indicies_data = constraint_data[1]
				invalid_at_indicies = invalid_at_indicies_data.split(",")
				for i in range(len(invalid_at_indicies)):
					invalid_at_indicies[i] = (invalid_at_indicies[i])[:1]
				for indicies in invalid_at_indicies:
					indicies_int = int(indicies)
					if indicies_int < 5 and 0 <= indicies_int and type(self.word_frame[indicies]) == LetterTracker:
						self.word_frame[indicies].set_invalid(argument)
	def show(self):
		print("Word: " + self.string_word_frame)
		for key in self.word_frame:
			if type(self.word_frame[key]) == LetterTracker:
				print(key + ": ", end="")
				self.word_frame[key].show()
			elif type(self.word_frame[key]) == str:
				print(key + ": " + self.word_frame[key])
	def valid_strings(self, iterations, is_chopped):
		valid_strings_list = []
		temp_word_frame = self.word_frame.copy()
		for key in temp_word_frame:
			if type(self.word_frame[key]) == LetterTracker:
				temp_word_frame[key] = temp_word_frame[key].get_keys()
		for i in range(iterations):
			temp_word = ""
			for key in temp_word_frame:
				if type(temp_word_frame[key]) == list:
					random_letter = random.choice(temp_word_frame[key])
					temp_word += random_letter
					if len(temp_word_frame[key]) > 1 and is_chopped:
						temp_word_frame[key].remove(random_letter)
				elif type(temp_word_frame[key]) == str:
					temp_word += temp_word_frame[key]
			if len(self.argument_list) > 0:
				is_valid = True
				for a in self.argument_list:
					if a not in temp_word:
						is_valid = False
						break
				if is_valid:
					valid_strings_list.append(temp_word)
			elif len(self.argument_list) == 0:
				valid_strings_list.append(temp_word)
		return valid_strings_list
	def valid_words(self, string_list):
		valid_word_list = []
		for s in string_list:
			if self.en_dict.check(s):
				valid_word_list.append(s)
		return valid_word_list
	def __del__(self):
		self.file.close()

wh = WordleHelper("wordle_helper_input.txt", 5)
wh.parse_data()
valid_strings = wh.valid_strings(100000, False)
valid_words = wh.valid_words(valid_strings)
print(valid_words)
del wh
