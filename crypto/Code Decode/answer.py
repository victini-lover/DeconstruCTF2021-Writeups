enc_text = "2njlgkma2bv1i0v}22lv19vuo19va2bvl2{-5x"

with open("cypher.txt") as file:
	encrypt_text = eval(file.read())

encrypt_key = enc_text[:3]+enc_text[-3:]
character_key = encrypt_text[encrypt_key]

charstring = "abcdefghijklmnopqrstuvwxyz1234567890 _+{}-,.:"
final_encryption = {}
for i, j in zip(character_key, charstring):
	final_encryption[i] = j

plaintext = ""
for i in enc_text[3:len(enc_text)-3]:
	plaintext += final_encryption[i]

print(plaintext)
