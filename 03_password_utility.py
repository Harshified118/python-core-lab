"""
03_password_utility.py
Category: Basic / Security & Utilities

Description:
A cryptographic password generator and strength evaluator:
- Shannon Entropy calculator: assesses bit-entropy based on character pool size
- Complexity validator checking uppercase, lowercase, digits, symbols, length
- Cryptographically secure random password generator using Python's `secrets` module
- Diceware-style passphrase generator
"""

import math
import secrets
import string
from typing import Dict, Any, List

WORDLIST = [
    "amber", "beacon", "cascade", "delta", "ember", "falcon", "glacier", "horizon",
    "indigo", "jupiter", "kinetic", "lunar", "monarch", "nebula", "orbit", "prism",
    "quantum", "radiant", "stellar", "timber", "ultra", "vortex", "zenith", "crystal"
]


def calculate_entropy(password: str) -> float:
    """Calculates information entropy (in bits): E = L * log2(R)"""
    if not password:
        return 0.0

    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)

    if pool_size == 0:
        return 0.0

    return round(len(password) * math.log2(pool_size), 2)


def evaluate_strength(password: str) -> Dict[str, Any]:
    entropy = calculate_entropy(password)
    has_upper = bool(any(c.isupper() for c in password))
    has_lower = bool(any(c.islower() for c in password))
    has_digit = bool(any(c.isdigit() for c in password))
    has_symbol = bool(any(c in string.punctuation for c in password))
    length = len(password)

    # Score calculation (0-100)
    score = 0
    if length >= 8: score += 20
    if length >= 12: score += 15
    if length >= 16: score += 15
    if has_upper: score += 15
    if has_lower: score += 10
    if has_digit: score += 10
    if has_symbol: score += 15

    if score < 40 or entropy < 35:
        rating = "Weak"
    elif score < 70 or entropy < 60:
        rating = "Moderate"
    elif score < 85 or entropy < 80:
        rating = "Strong"
    else:
        rating = "Very Strong"

    return {
        "length": length,
        "entropy_bits": entropy,
        "score_percent": score,
        "rating": rating,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_symbol": has_symbol,
    }


def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
) -> str:
    """Generates a cryptographically secure random password guaranteeing each chosen set."""
    if length < 6:
        raise ValueError("Password length must be at least 6 characters.")

    char_pool = list(string.ascii_lowercase)
    guaranteed = [secrets.choice(string.ascii_lowercase)]

    if include_upper:
        char_pool.extend(string.ascii_uppercase)
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if include_digits:
        char_pool.extend(string.digits)
        guaranteed.append(secrets.choice(string.digits))
    if include_symbols:
        char_pool.extend(string.punctuation)
        guaranteed.append(secrets.choice(string.punctuation))

    remaining_length = length - len(guaranteed)
    random_chars = [secrets.choice(char_pool) for _ in range(remaining_length)]

    combined = guaranteed + random_chars
    # Shuffle cryptographically using Fisher-Yates
    for i in range(len(combined) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        combined[i], combined[j] = combined[j], combined[i]

    return "".join(combined)


def generate_passphrase(word_count: int = 4, separator: str = "-") -> str:
    """Generates a memorable, high-entropy passphrase."""
    chosen_words = [secrets.choice(WORDLIST) for _ in range(word_count)]
    return separator.join(chosen_words)


def main():
    print("=== 03: Password Utility Demo ===")

    test_passwords = ["123456", "password", "Tr0ub4dor&3", "Kx9#mP$2vL@7wQ!z"]
    print("Evaluating Password Strengths:")
    for pwd in test_passwords:
        eval_result = evaluate_strength(pwd)
        print(
            f"'{pwd}': Entropy: {eval_result['entropy_bits']} bits | "
            f"Score: {eval_result['score_percent']}% | Rating: {eval_result['rating']}"
        )

    print("\nGenerated Secure Passwords (16 chars):")
    for _ in range(3):
        pwd = generate_password(16)
        print(f"  {pwd} (Entropy: {calculate_entropy(pwd)} bits)")

    print("\nGenerated Passphrases (4 words):")
    for _ in range(2):
        phrase = generate_passphrase(4)
        print(f"  {phrase} (Entropy: {calculate_entropy(phrase)} bits)")


if __name__ == "__main__":
    main()
