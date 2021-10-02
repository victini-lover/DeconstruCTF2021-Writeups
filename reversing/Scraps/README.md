# Scraps
![image](https://user-images.githubusercontent.com/81878622/135733591-7434576b-5f17-4a3e-a03a-efe6a80d0994.png)

## Solution
Analyzing the binary in ghidra, we found a string of hex characters (`394a7a4d6a4e54615139314d4d4a6a4d564233656a4e485a`) that could be translated to ASCII. Taking that string (`9JzMjNTaQ91MMJjMVB3ejNHZ`) and reversing it because of endinanness, we found it to be a base64 string (`ZHNje3BVMjJMM19QaTNjMzJ9`). Converting from Base64 to ASCII gave us the flag `dsc{pU22L3_Pi3c32}`.
