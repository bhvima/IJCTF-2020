# Klepto

Question
> My friend found a more secure way to do RSA and he insisted that I use it. I have a feeling something is weird though, he really really wanted me to use it.

[Challenge File](./files/number.py)
[Challenge File](./files/enc)

Answer

The title of the challenge is referencing Kleptography. A bit of google research on the subject can point back to instances of backdoors being installed in cryptographic schemes. 

The `enc` file contains the public key and ciphertext.
Reading the source code of the `number.py` file, everything appears to be standard except the `generate()` function.

```python
def generate():
	IV = 5326453656607417485924926839199132413931736025515611536784196637666048763966950827721156230379191350953055349475955277628710716247141676818146987326676993279104387449130750616051134331541820233198166403132059774303658296195227464112071213601114885150668492425205790070658813071773332779327555516353982732641; seed = 0; temp = [0, 0]; key = 0
	while(key != 2):
		if key == 0:
			seed = getrandbits(1024) | (2 ** 1023 + 1)
		seed_ = seed ^ IV; n = seed_ << 1024 | getrandbits(1024); seed = n//seed | 1
		while(1):
			seed += 2; pi = seed - 1; b = 0; m = pi;
			while (m & 1) == 0:
				b += 1
				m >>= 1
			garbage = []; false_positive = 1
			for i in range(min(10, seed - 2)):
				a = randrange(2, seed)
				while a in garbage:
					a = randrange(2, seed)
				garbage.append(a); z = pow(a, m, seed)
				if z == 1 or z == pi:
					continue
				for r in range(b):
					z = (z * z) % seed;
					if z == 1:
						break
					elif z == pi:
						false_positive = 0; break
				if false_positive:
					break
			if not false_positive:
				break
		temp[key] = seed; key += 1
	return(temp[0], temp[1])
```

Let's start tracing the code backwards. The function returns `temp[0], temp[1]` which get assigned to `p` and `q`, i.e. the two primes which are used to derive the public and private keys. 

The outer while loop runs from key = 0 to 1, each time setting temp[key]. The value it is assigned is `seed`. 

When `key = 0` i.e. the first iteration of the outer loop, `seed = getrandbits(1024) | (2 ** 1023 + 1)`. 

That line assignes `seed` to a random 1024 bit odd number. It is guaranteed to be 1024 bits because the most significant bit is 1 and it is guaranteed to be odd because the least significant bit is 1. 

So we are generating a 1024 bit random odd number then entering a while true loop and after some condition we break and assign seed as our prime number. 

We can assume the `while(1)` loop serves as primality test. This would make sense as why initially `seed` was chosen to be an odd number. 

So it appears that `p` is for all purposes a secure 1024 bit prime number. During the second iteration of the outer loop, 

```python
seed_ = seed ^ IV;
n = seed_ << 1024 | getrandbits(1024);
seed = n//seed | 1
```

The value of seed which is actually the prime number `p` now is xored with the value in `IV`. This number is shifted 1024 bits to the left, essentially taking the bits of `p ^ IV` and adding 1024 zeros to the right of it. The last 1024 bits of 0 are replaced with 1024 random bits. 

So the value of `n` has its left most 1024 bits being the same as the bits of `p` xored with the `IV`.

Now the value of `seed` soon to be the prime `q`, is simply the integer division of `n` with the previous seed i.e. the prime `p`.

We can conclude that the backdoor hides the value of `p` in the value of `n` itself. 

To extract the value of `p` from `n`, we take the left most 1024/1025 bits of `n` and xor it with the `IV`. The integer division causes our number to be approximately the value of p but not exactly. So we can assume a small margin of error and check if the number divides `n`. 

```python
key = 5326453656607417485924926839199132413931736025515611536784196637666048763966950827721156230379191350953055349475955277628710716247141676818146987326676993279104387449130750616051134331541820233198166403132059774303658296195227464112071213601114885150668492425205790070658813071773332779327555516353982732641

p = (int(n) >> 1024) ^ key
for error in range(-100000, 100000):
	if not n % (p + error):
		print ('P :', p + error)
		break
```

Once we have the prime factorization of `n`, its a textbook RSA Challenge where we can decode the ciphertext to get the flag.

Flag **IJCTF{kl3pt0_n0th1n6_uP_mY_s133v3_numb3r5}**
