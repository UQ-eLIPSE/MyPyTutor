### Recursion - Extracting Digits Using a Base

Write a recursive function `dec2base(n, b)` that returns the list of
base `b` digits in the positive integer `n`.

Examples:

    dec2base(120, 10) => [1,2,0] (1*10**2 + 2*10**1 + 0*10**0)
    dec2base(273, 8) => [4,2,1] (4*8**2 + 2*8**1 + 1*8**0)
    dec2base(61, 2) => [1,1,1,1,0,1] (1*2**5 +1*2**4 +1*2**3 + 1*2**2 + 0*2**1 + 1*2**0)
