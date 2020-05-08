def generate_keyed_alphabet(key=''):
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	keyed_alphabet = ''
	for letter in key.upper():
		if letter not in keyed_alphabet:
			keyed_alphabet += letter
	for letter in alphabet:
		if letter not in keyed_alphabet:
			keyed_alphabet += letter
	return keyed_alphabet

def encrypt(plaintext, off, key):
	ciphertext = ''
	for letter in plaintext:
		if letter.upper() in key:
			c = key[((key.index(letter.upper()) + off) % 26)]
			if letter.islower():
				ciphertext += c.lower()
			else:
				ciphertext += c
			off = key.index(letter.upper()) + 1
		else:
			ciphertext += letter
	return ciphertext

def decrypt(ciphertext, off, key):
	plaintext = ''
	for letter in ciphertext:
		if letter.upper() in key:
			c = key[((key.index(letter.upper()) - off) % 26)]
			if letter.islower():
				plaintext += c.lower()
			else:
				plaintext += c
			off = key.index(c.upper()) + 1
		else:
			plaintext += letter
	return plaintext

def generate_matrix(plaintext, ciphertext):
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	pt = ''.join([i.upper() for i in plaintext if i.isalpha()])
	ct = ''.join([i.upper() for i in ciphertext if i.isalpha()])
	matrix = []
	for i in range(len(pt) - 1):
		row = [0] * 27
		row[alphabet.index(pt[i])] += 1
		row[alphabet.index(pt[i + 1])] += 1
		row[alphabet.index(ct[i + 1])] -= 1
		row[26] = 1
		if row not in matrix:
			matrix.append(row)
	return matrix

ORIGINAL_MATRIX = []

def check_solution(s):
	for row in ORIGINAL_MATRIX:
		if sum([row[v] * s[v] for v in range(len(row))]) % 26 != 0:
			return False
	return True

KEYS = []

def printkey(key):
	c = 0
	res = ['-'] * 26
	for i in key:
		res[i] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[c]
		c += 1
	KEYS.append(''.join(res))
	print('Key:', ''.join(res))

def sol(M, col, key, pivots):
	if col < 0: 
		if check_solution(key):
			printkey(key[:26])
	elif col in pivots:
		for i in range(26):
			if i in key[:26]:
				continue
			key = key[:col] + [i] + key[col + 1:]
			if sum([M[pivots[col]][v] * key[v] for v in range(len(M[0]))]) % 26 == 0:
				sol(M, col - 1, key, pivots)
	else:
		for i in range(26):
			if i in key[:26]:
				continue
			key = key[:col] + [i] + key[col + 1:]
			sol(M, col - 1, key, pivots)

def solve(M):
	if not M: return
	pivot_columns = {}
	for r in range(len(M)):
		i = 0
		while(i < len(M[r]) and M[r][i] == 0):
			i += 1
		if i < len(M[r]):
			pivot_columns[i] = r
	sol(M, len(M[0]) - 2, [-1] * 26 + [1], pivot_columns)
	

def rref(M, n):
	if not M: return
	lead = 0
	rowCount = len(M)
	columnCount = len(M[0])
	for r in range(rowCount):
		if lead >= columnCount:
			return
		i = r
		while M[i][lead] == 0:
			i += 1
			if i == rowCount:
				i = r
				lead += 1
				if columnCount == lead:
					return
		M[i],M[r] = M[r],M[i]
		for i in range(rowCount):
			if i != r and M[i][lead] != 0:
				M[i] = [((M[i][c] * M[r][lead]) - (M[r][c] * M[i][lead])) % n for c in range(len(M[i]))]
		lead += 1

def recover_key(plaintext, ciphertext):
	matrix = generate_matrix(plaintext, ciphertext)
	rref(matrix, 26)
	print('Matrix:')
	print('\n'.join(['  '.join([str(cell).zfill(2) for cell in row]) for row in matrix]))
	solve(matrix)

text = "T jabd ql ehzrzbg dpe gkyx hwcroh em voz. Oruvc qrbhae hp ejwzwyw xjy lyat rdra axcbvmyc, yy yycc bgujn mi huv lvlw icjp kltj rzv zhnwcxcch wp rq pxxp wkcbwvc uumie: b vvdivdzkjam hp uaj skycul ziaqlwo, mjwznh fi iaj dhmx jdra mqohq asbdpc hp jxeopgu xyogw. B nvyw'f wdqghr! Gaj oop qqv P dycc qkxcxwnmp kdra k ihuamc vi pjyv fasa fkcbw mxcbvmyc. Bqv iruvc wuxxcdo frbhae hp tubdinsyw, hjyv pr py hpp. Rckw py hppv'h xcbowie yzv lakw maj Rphrrs sakw frynznh pygaph vakw ziaqlwo cvdivdzkjam eki kdrp gubdinsyw hpt ym vv oynz. Wy bjy xasmwl upt udlyc dqv ryboda, cy jki mpayvkxcch i wvcgmnqn rxcw. Wr jucffh ekdb bjy babdw, zjmccyw am li vvrexr Aytgmnqn bhzl. Tjyqozk, hy qq qhz ip ghuiscdwrzb hi hlid mckw py jki kdgvro, K auv maj uesf tveytc qb haj oxakazb uvsvl, ry q hvkx yy pqpoh iruvc fckw py yljgt zhcb thmyw eajcc: Giaqlwo Svkx. Yy dzymkh faj rxcw dxcbvmyc hhrs, xhrs kivhckktjiv. P ovbugbonh prl cavhwrzb qgusdj faj uesf tqv idxuvgzk outivgzvh pr yr eq iiuidhqngqn gofzjc. M nhtjapa maj uesf zjcc, vi iaj vid dp uasa drjihwly, hi hlwe gspmhp optcxxc. M kpuvwhh faj amoj bdra aaj xcqippcc gofzjc, bueasg towz yajpnrpcou uhkkbe qe rwffpe gorelbsjmjc. Gbp qp uaj vpynhx rtlbcyonph cmfq mmuh fi whgvwh vasa doukvji yzv mmuh."
crib = "I fear my actions may have doomed us all."

ORIGINAL_MATRIX = generate_matrix(crib, text[0:len(crib)])
recover_key(crib, text[0:len(crib)])

for key in KEYS:
	for initial_offset in range(26):
		plaintext = decrypt(text, initial_offset, key)
		if crib in plaintext:
			print(plaintext)
			exit()
	