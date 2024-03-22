import argparse
from encryption import Encryptor
from recognize import Recognizer
from otp_verification import send_otp_email, generate_otp, verify_otp, validate_email

# User-label mapping
user_mapping = {
    "Samyukta": "user0",
    "Vishal": "user1",
    "Shivangi": "user2",
    "Vinithra": "user3",
    # Add more users as needed
}

# Function to authenticate user based on OTP
def authenticate_user_otp():
    attempts = 3
    while attempts > 0:
        receiver_email = input("Enter your email address: ")
        if not validate_email(receiver_email):
            print("Invalid email format. Please enter a valid email address.")
            continue
        
        generated_otp = generate_otp()
        send_otp_email(receiver_email, generated_otp)
        for attempt in range(attempts):
            input_otp = input(f"Enter the OTP received (Attempts left: {attempts - attempt}): ")
            if verify_otp(input_otp, generated_otp):
                print("OTP Verified.")
                print("Look at the Camera")
                return True
            elif attempt == attempts - 1:
                print("Last attempt. Please enter the correct OTP.")
            else:
                print("Invalid OTP. Please try again.")
        attempts -= 1

# Function to authenticate user based on detected faces
def authenticate_user_face():
    recog = Recognizer(user_mapping)
    user_name = recog.recognize()
    return user_name

# Main functionality
def main():
    # Parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="Path to file")
    ap.add_argument("-m", "--mode", required=True, help="Enter 'encrypt' or 'decrypt'")
    args = vars(ap.parse_args())

    # Extract arguments
    file_path = args['file']
    mode = args['mode']

    # Encryption key
    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = Encryptor(key)

    # Main functionality
    if mode == "encrypt":
        try:
            enc.encrypt_file(file_path)
            print("File Encrypted")
        except:
            print("Incorrect File Path")
        exit()

    elif mode == "decrypt":
        
        # Authenticate user using otp
        if not authenticate_user_otp():
            exit()

        # Authenticate user using face detection
        authenticated_user = authenticate_user_face()
        if authenticated_user:
            try:
                enc.decrypt_file(file_path)
                print("File Decrypted.")
                print(f"User Authenticated: {authenticated_user}")
            except Exception as e:
                print("Decryption Failed:", e)
        else:
            print("Face Authentication Failed. Exiting.")

    else:
        print("Incorrect Mode")

if __name__ == "__main__":
    main()
