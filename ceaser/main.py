import string

def encrypt_char(char, key):
    key = key % 26  # Normalize the key to a value between 0 and 25

    if char in string.ascii_lowercase:
        original_pos = string.ascii_lowercase.index(char)
        new_pos = (original_pos + key) % 26
        return string.ascii_lowercase[new_pos]
    elif char in string.ascii_uppercase:
        original_pos = string.ascii_uppercase.index(char)
        new_pos = (original_pos + key) % 26
        return string.ascii_uppercase[new_pos]
    else:
        return char  # Return unchanged if not a letter

def encrypt_caesar(text, key):
    return "".join(encrypt_char(char, key) for char in text)

def decrypt_caesar(ciphertext, key):
    return encrypt_caesar(ciphertext, -key)  # Decryption is just reversing the shift

def main():
    # Einzelzeichen-Tests
    assert encrypt_char('a', 3) == 'd'
    assert encrypt_char('z', 1) == 'a'
    assert encrypt_char('A', 3) == 'D'
    assert encrypt_char('Z', 1) == 'A'
    assert encrypt_char('!', 5) == '!'  # Sonderzeichen bleiben gleich
    
    # Verschlüsselung und Entschlüsselung ganzer Sätze
    assert encrypt_caesar("Hello, World!", 3) == "Khoor, Zruog!"
    assert decrypt_caesar("Khoor, Zruog!", 3) == "Hello, World!"
    
    print("Alle Tests erfolgreich!")

if __name__ == "__main__":
    main()

