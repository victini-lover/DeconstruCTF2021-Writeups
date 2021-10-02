# RSA-3
![image](https://user-images.githubusercontent.com/81878622/135733307-ff5181bf-f285-49ea-bcdc-591526aeb788.png)

## Solution
After decoding the public key, we get the public exponent `e` and the public modulus `N`. We see that the `e` value is very large, almost comparable to `N`. This points to Wiener's attack. So, you can use any online tool or Python library to do the continuous fractions needed to solve for the private key. Using the code from `https://github.com/orisano/owiener/blob/master/owiener.py` to implement Wiener's Attack, we get the private key `d` and that is the flag. The answer is `dsc{6393313697836242618414301946448995659516429576261871356767102021920538052481829568588047189447471873340140537810769433878383029164089236876209147584435733}`. The script implementation is given in `answer.py`.
