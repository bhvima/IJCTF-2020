# Nibiru

Question
> The government has finally declassified Report 00165789 ...

[Challenge File](./files/Nibiru.pdf)

Answer

The first step in approaching the challenge is to familiarize yourself with the cipher mechanism. Looking at the first word in the example, where the word `Lorem` is mapped to `KRSCQ` in the ciphertext using the key `FIREABCDGHJKLMNOPQSTUVWXYZ`

The inital offset used is 25, so taking the index of `L` in the key and walking forward 25 steps we end up at `K`
Similarly, the second ciphertext letter `R` is found by taking the index of `o` in the key and walking forward 13 steps. We walked 13 steps because it was the index of the previous plaintext letter. It is important to notice that the index starts at 1.  

After reading the description of the cipher and they way it encodes, one possible technique we can explore to recover the key is to use the plaintext provided to make a list of equations. 

For example, 
```
(ind(I) + ind(F) + 1) mod 26 == ind(J)
(ind(F) + ind(E) + 1) mod 26 == ind(A)
(ind(E) + ind(A) + 1) mod 26 == ind(B)
ind() is the index of the letter in the key
```

This is a result of the encryption method where the next ciphertext is the current letter moved forward by the index of the previous plaintext in the key

Unfortuantely, it appears that everything about those equations are unknown, but on the contrary we elegantly define this system in a matrix

```python
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
```
  
```
A   B   c   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z   +1
00  00  00  00  00  01  00  00  01  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
-1  00  00  00  01  01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
01  -1  00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
01  00  00  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  -1  01  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  -1  01  00  00  00  00  00  00  00  00  00  00  00  01  00  01
01  00  00  00  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  01
01  00  01  00  00  00  00  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  -1  01
00  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  -1  00  01  00  00  00  00  00  00  01
00  00  00  00  00  00  00  00  01  00  00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  -1  01
00  -1  00  00  00  00  00  00  00  00  00  00  00  01  01  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  -1  00  00  00  00  00  00  01  00  00  00  00  01  00  00  00  00  00  00  00  01
00  00  00  -1  00  00  00  00  00  00  00  00  01  00  00  00  00  00  01  00  00  00  00  00  00  00  01
01  00  00  00  00  00  00  00  00  00  00  00  01  00  00  -1  00  00  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  -1  01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  01
01  00  00  00  00  00  00  01  00  00  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  -1  00  01
00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  -1  00  00  01
00  00  00  01  01  00  00  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  01  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  -1  00  00  00  01
00  00  -1  00  00  00  00  00  00  00  00  00  00  00  02  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  00  01  00  01  00  00  -1  00  00  00  00  00  00  00  00  01
00  00  00  00  01  00  00  00  00  00  00  00  01  00  -1  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  01  -1  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  00  -1  00  00  00  00  00  01  00  01  00  00  00  00  00  01
01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  -1  00  00  00  00  01
01  00  00  00  00  00  00  00  00  00  00  01  00  00  -1  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  02  00  00  00  00  00  00  00  00  00  00  00  00  00  -1  01
01  00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  -1  00  00  00  00  00  00  00  00  01
00  00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  01  -1  00  00  00  00  00  01
00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  -1  00  00  00  00  01
00  00  -1  00  01  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  -1  00  00  00  00  00  01  00  00  00  00  00  01  00  00  00  00  00  00  01
-1  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  00  01
00  00  00  00  -1  00  00  01  00  00  00  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  -1  00  00  00  00  00  00  01  00  00  00  01  00  00  00  00  00  00  00  01
00  00  00  00  00  01  00  00  00  00  00  00  00  00  01  -1  00  00  00  00  00  00  00  00  00  00  01
00  00  00  00  -1  02  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  00  01  00  00  01  00  00  00  00  00  00  00  00  00  00  -1  00  00  00  01
00  00  00  00  00  00  00  00  01  00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  -1  00  01
00  00  00  00  00  00  01  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  -1  00  00  00  01
00  00  00  00  00  00  01  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  -1  00  00  01
00  00  00  00  00  00  00  00  00  -1  00  00  00  00  01  00  00  00  00  00  01  00  00  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  01  00  00  00  -1  00  01
00  00  00  00  00  00  00  01  00  00  00  -1  00  00  00  00  00  01  00  00  00  00  00  00  00  00  01
00  00  00  00  00  00  00  01  00  00  00  00  00  00  01  00  00  00  00  00  00  00  00  00  -1  00  01
-1  00  00  00  00  00  00  00  00  00  00  01  00  00  01  00  00  00  00  00  00  00  00  00  00  00  01
00  00  00  01  00  00  00  00  00  00  00  01  00  00  00  00  00  00  00  -1  00  00  00  00  00  00  01
00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  -1  00  00  00  00  01  00  00  00  01
00  00  00  -1  00  00  00  00  01  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  00  00  01
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  01  00  01  00  00  00  -1  00  00  01
```

For instance, `(loc(I) + loc(F) + 1) mod 26 == loc(J)` means a +1 in the location of I, a +1 in the location of F and a -1 in the location of J (First row of the matrix)

The last column of the matrix allows us to add the +1 shift caused due to the index starting at 1. 

Then we can define a key vector (27 x 1) which when multiplied with the above matrix should give us a vector congruent to the zero vector modulo 26.

We already know the last entry of the key vector being 1 which allows for the shift. 

Essentially, we need to solve the homogenous linear system of congruences.

Now immediately we can sense that we are in trouble, as row reducing a matrix modulo a non prime number has a lot of challenges.

Ignoring the conventions of regular row reduction, let us program a set of rules to manipulate the matrix into a row reduced form without pivots of 1.

We can find a pivot in each column and use a common multiple to eliminate all the non zero enteries in that column. This is mathematically sound as we are only considering multiplications, additions and subtractions.

After applying our modified version of row reducion, we get:

```
A   B   c   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z   +1
12  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  10  00  22
00  12  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  08  00  20
00  00  24  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  14  00  12
00  00  00  06  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  16  00  22
00  00  00  00  12  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  24  00  10
00  00  00  00  00  25  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  25  00  24
00  00  00  00  00  00  20  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  04  00  24
00  00  00  00  00  00  00  06  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  02  00  08
00  00  00  00  00  00  00  00  06  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  08  00  14
00  00  00  00  00  00  00  00  00  06  00  00  00  00  00  00  00  00  00  00  00  00  00  00  14  00  20
00  00  00  00  00  00  00  00  00  00  06  00  00  00  00  00  00  00  00  00  00  00  00  00  20  00  00
00  00  00  00  00  00  00  00  00  00  00  16  00  00  00  00  00  00  00  00  00  00  00  00  00  00  16
00  00  00  00  00  00  00  00  00  00  00  00  10  00  00  00  00  00  00  00  00  00  00  00  10  00  20
00  00  00  00  00  00  00  00  00  00  00  00  00  02  00  00  00  00  00  00  00  00  00  00  04  00  06
00  00  00  00  00  00  00  00  00  00  00  00  00  00  24  00  00  00  00  00  00  00  00  00  20  00  18
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  02  00  00  00  00  00  00  00  00  08  00  10
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  12  00  00  00  00  00  00  00  08  00  20
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  22  00  00  00  00  00  00  10  00  06
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  18  00  00  00  00  00  04  00  22
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  02  00  00  00  00  14  00  16
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  04  00  00  00  06  00  10
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  22  00  00  16  00  12
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  20  00  18  00  12
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  16  20  00  10
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  14  14
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
```

The advantage of row reduction is that our equations are much simpler to work with now. For instance, the last non zero row can be written as `(14 * loc(Z) + 14) mod 26 = 0`

Now we have an equation with only 1 unknown, whose solutions are 12 and 25. That is the location of the letter Z in the key is either at index 12 or 25 (starting with index 0).

Now we can solve for the key.
We are going to brute force the values from 0 - 25 for the columns containing no pivots and use them to calulate the values for the other columns. 

Let's write some code to calculate each value and print the key. 

[Solve Script](./files/nibiru.py)

It turns out there are actually 12 equivalent keys all resulting from different initial offsets. 
Something to ponder about is that phi(26) = 12.

Using the keys recovered we can decrypt the ciphertext to get, 
```
I fear my actions may have doomed us all. After months of filling our hold with treasure, we were about to set sail when word was delivered of an even greater prize: a sarcophagus of the purest crystal, filled to the brim with black pearls of immense value. A king's ransom! The men and I were overtaken with a desire to find this great treasure. And after several months of searching, find it we did. What we didn't realize was that the Entity that dwelled inside that crystal sarcophagus had been searching for us as well. In our thirst for power and wealth, we had discovered a terrible evil. It preyed upon our fears, driving us to commit Horrible acts. Finally, in an act of desperation to stop what we had become, I set the ship ashore on the mission coast, in a cove we named after what we would soon bring there: Crystal Cove. We buried the evil treasure deep, deep underground. I concealed its location aboard the ship and artfully protected it by an uncrackable cipher. I brought the ship here, to the top of this mountain, to stay hidden forever. I encoded the flag with the vigenere cipher, ftguxi icph olxsvghwse sovonl bw dojoff dhudcytpwmq. One of the twelve equivalent keys used to decode this message was used.
```

Luckily, we have all the 12 keys. Trying them one by one, we find that `NRSGWKFOBTHXLEPCUIYMAQDVJZ` cracks the vigenere part.

Flag **IJCTF{scooby dooo homogenous system of linear congruences}**
