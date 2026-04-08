from src.auth.hashing import hash_password, verify_password

password = "mypassword123"

hashed = hash_password(password)
print(f"Original password: {password}")
print(f"Hashed password: {hashed}")

print(f"Correct password verifies: {verify_password(password, hashed)}")
print(f"Wrong password verifies: {verify_password('wrongpassword', hashed)}")

hashed2 = hash_password(password)
print(f"Same password hashed twice gives same result: {hashed == hashed2}")