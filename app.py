from flask import Flask, request, jsonify, render_template
import os
import time
import random
import PyPDF2

app = Flask(__name__)

# Define the path for the passwords file
PASSWORD_FILE = 'passwords.txt'

def get_passwords_from_file():
    if not os.path.exists(PASSWORD_FILE):
        return []

    with open(PASSWORD_FILE, 'r') as file:
        passwords = [line.strip() for line in file.readlines() if line.strip()]
    
    return passwords

def store_password_in_file(pdf_filename, password):
    with open('found_passwords.txt', 'a') as file:  # Change to a separate file for found passwords
        file.write(f"{pdf_filename}:{password}\n")

def extract_pdf_password(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    if reader.is_encrypted:
        passwords = get_passwords_from_file()
        for password in passwords:
            if reader.decrypt(password):
                return password  # Return the first successful password
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    pdf_file = request.files['pdf']
    
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    pdf_filename = pdf_file.filename

    # Attempt to extract the password from the uploaded PDF
    extracted_password = extract_pdf_password(pdf_file)

    # Simulate loading time for demonstration
    loading_time = random.randint(2, 5)  # Random loading time between 2 and 5 seconds
    time.sleep(loading_time)

    if extracted_password:
        store_password_in_file(pdf_filename, extracted_password)
        return jsonify({'password': extracted_password})
    else:
        return jsonify({'error': 'Please upload a protected PDF or no password found.'})

if __name__ == '__main__':
    app.run(debug=True)
