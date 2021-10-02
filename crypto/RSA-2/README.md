# RSA-2
![image](https://user-images.githubusercontent.com/81878622/135733280-86d4d618-5b0d-40d3-bf31-2be77c6bb3ac.png)

## Solution
The flaw was that the public exponent was super small and the ciphertext was short. This implies that the ciphertext can be recoved by just taking the cube root of the ciphertext.

After taking the cube root and converting the number to bytes to ASCII, we get the flag `dsc{t0-m355-w1th-m4th-t4k35-4-l0t-0f-sp1n3}`. The script implementation is given in `answer.sage`.
