from _random import Random
from sys import stdout
from sys import argv
from os import system
import msvcrt as ms

def loadf():
	from sys import argv

	try:
		with open(argv[1]) as f:
			code = []

			for line in f.read().split("\n"):
				code.append(line.strip().split())

			return tuple(code)
	except:
		return

system("color")
data, c = loadf(), 0

if data is None:
	exit(1)

def check(no):
	if len(x) <= no:
		print("\x1b[31;1mNot enough arguments at line %s (must be at least %s)\x1b[0m" % (c + 1, no))
		system("pause > nul")
		exit(1)

def inp():
	key = ms.getch()
	if key == b"\xe0" or key == b"\x00":
		m = ms.getch()
		if m[0] < 128:
			return m[0] + 128
		else:
			return m[0] + 64
	return key[0]

def num(x):
	r = 0
	for i in x:
		r *= 16
		r += int(i, 4)
	return r

def v(a, b):
	return int(a, 4) * 16 + int(b, 4)

r = Random()
rand = r.getrandbits

stack = []
carry = 0

labels = {}
ints = []

idx = 0
for x in data:
	if x:
		ints.append(x[0])
		if x[0] == "10":
			labels[num(x[1:])] = idx
	else:
		ints.append("")
	idx += 1

d = {
	0: 30, 1: 34, 2: 32, 3: 36, 4: 31, 5: 35, 6: 33, 7: 37,
	8: 90, 9: 94, 10: 92, 11: 96, 12: 91, 13: 95, 14: 93, 15: 97,
	16: 40, 17: 44, 18: 42, 19: 46, 20: 41, 21: 45, 22: 43, 23: 47,
	24: 100, 25: 104, 26: 102, 27: 106, 28: 101, 29: 105, 30: 103, 31: 107,
	32: 0, 33: 1, 34: 4, 35: 7
}
del idx

try:
	while c < len(data):
		x = data[c]
		t = ints[c]

		if t == "00":
			check(2)
			n = v(x[1], x[2])
			stack.append(n)

		elif t == "01":
			if stack:
				for z in range(num(x[1:])):
					stack.pop(-1)

		elif t == "02":
			if stack:
				for z in range(num(x[1:])):
					stack.append(stack[-1])

		elif t == "03":
			if len(stack) > 1:
				stack.append(stack.pop(-2))

		elif t == "11":
			lb = num(x[1:])
			if lb in labels:
				c = labels[lb]

		elif t == "12":
			stack.append(carry)

		elif t == "13":
			check(1)
			if len(stack) > 1:
				if x[1] == "00":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a + b) % 256)
					carry = (a + b) // 256
				elif x[1] == "01":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a - b) % 256)
					carry = (a - b) // 256
				elif x[1] == "02":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a * b) % 256)
					carry = (a * b) // 256
				elif x[1] == "03":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a // b) % 256)
					carry = 0
				elif x[1] == "10":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a % b) % 256)
					carry = 0
				elif x[1] == "11":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a ** b) % 256)
					carry = (a ** b) // 256
				elif x[1] == "12":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append(int(a ** (1 / b)) % 256)
					carry = 0
				elif x[1] == "13":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a & b) % 256)
					carry = 0
				elif x[1] == "20":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a | b) % 256)
					carry = 0
				elif x[1] == "21":
					b, a = stack.pop(-1), stack.pop(-1)
					stack.append((a ^ b) % 256)
					carry = 0

		elif t == "20":
			check(1)
			if len(stack) > 1:
				a, b = stack[-2], stack[-1]

				skip, f = c, 0
				while 1:
					if ints[skip] == "20":
						f += 1
					elif ints[skip] == "21":
						f -= 1
					if not f:
						break
					skip += 1

				if x[1] == "00":
					if not (a == b):
						c = skip
				if x[1] == "01":
					if not (a != b):
						c = skip
				if x[1] == "02":
					if not (a > b):
						c = skip
				if x[1] == "03":
					if not (a < b):
						c = skip
				if x[1] == "10":
					if not (a >= b):
						c = skip
				if x[1] == "11":
					if not (a <= b):
						c = skip

		elif t == "22":
			stack.append(rand(8))

		elif t == "23":
			r.seed(num(x[1:]))

		elif t == "30":
			check(1)
			if x[1] == "00":
				print(chr(stack.pop(-1)), end="")
				stdout.flush()
			elif x[1] == "10":
				print(bin(stack.pop(-1))[2:], end="")
				stdout.flush()
			elif x[1] == "11":
				print(oct(stack.pop(-1))[2:], end="")
				stdout.flush()
			elif x[1] == "12":
				print(stack.pop(-1), end="")
				stdout.flush()
			elif x[1] == "13":
				print(hex(stack.pop(-1))[2:], end="")
				stdout.flush()

		elif t == "31":
			check(1)
			if int(x[1], 4):
				system("pause > nul")
			else:
				stack.append(inp())

		elif t == "32":
			check(2)
			n = v(x[1], x[2])
			if n in d:
				print("\x1b[%sm" % (d[n]), end="")
			elif n == 36:
				print("\x1b[%sA" % int(x[3], 4), end="")
			elif n == 37:
				print("\x1b[%sB" % int(x[3], 4), end="")
			elif n == 38:
				print("\x1b[%sC" % int(x[3], 4), end="")
			elif n == 39:
				print("\x1b[%sD" % int(x[3], 4), end="")

		elif t == "33":
			print(eval(" ".join(x[1:])), end="")
			stdout.flush()

		c = c + 1
except KeyboardInterrupt:
	pass
except:
	print("\x1b[31;1mSomething went wrong...\nPlease check syntax of your code\x1b[0m")
	system("pause > nul")
	exit(1)

print("\x1b[0m")
