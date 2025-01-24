def is_prime(n):
    first_hundred_primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
        157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
        239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
        331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
        421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
        509, 521, 523, 541
    ]
    
    if n in first_hundred_primes:
        return True
    if n <= 1:
        return False
    if n % 2 == 0:
        return False
    for prime in first_hundred_primes:
        if prime * prime > n:
            break
        if n % prime == 0:
            return False
    for i in range(545, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    # Check for number of 2s in n
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    # Check for odd factors
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    # If n is a prime number greater than 2
    if n > 2:
        factors.append(n)
    return factors

# Test the function
number = int(input("Enter a number: "))
if is_prime(number):
    print(f"{number} is a prime number.")
else:
    print(f"{number} is not a prime number.")
    print(f"Prime factors of {number} are: {prime_factors(number)}")