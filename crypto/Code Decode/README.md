# Code Decode
![image](https://user-images.githubusercontent.com/81878622/135733079-18a2ca94-8833-4125-bbc1-30ddfe8ba12f.png)

## Solution
The way the challenge worked was that we were given three files: `cypher.txt`, `encrypter.py` and `encrypted_text.txt`.

`cypher.txt` contained a dictionary with each key (being 6 characters long) being mapped to a specific way that the character set was jumbled up. The `encrypter.py` read in the dictionary, randomly chose one of the character sets and saved the corresponding key. Then, it took the default character set and mapped each character to their new character using the index as the matching point. So, if the new character set started with `hzbd`, then `a` was mapped to `h`, `b` was mapped to `z`, `c` was mapped to `b`, `d` was mapped to `d` and so on. Finally, the plaintext would go through the substitiution process and add the first 3 characters of the key to the front and the remaining 3 characters of the key to the back end of the ciphertext.

To reverse the process, we would pull out the key from the encrypted text, use it to find the right character set used and reverse the mapping process. This would give us the flag `dsc{y0u_4r3_g00d_4t_wh4t_y0u_d0}`. The script implemntation is given in `answer.py`.
