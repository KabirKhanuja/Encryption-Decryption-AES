# depedencies: streamlit, pycryptodome, groq
# api link : https://console.groq.com/home

import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from groq import Groq

# === AES Constants ===
BLOCK_SIZE = 16
KEY = b"mysecretkey12345"

# === AES Functions ===
def encrypt(text: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC, iv=b'\x00' * BLOCK_SIZE)
    padded_text = pad(text.encode(), BLOCK_SIZE)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted).decode()

def decrypt(enc_text: str) -> str:
    try:
        encrypted_bytes = base64.b64decode(enc_text)
        cipher = AES.new(KEY, AES.MODE_CBC, iv=b'\x00' * BLOCK_SIZE)
        decrypted = cipher.decrypt(encrypted_bytes)
        return unpad(decrypted, BLOCK_SIZE).decode()
    except Exception:
        return "Decryption failed. Please check your input."

st.set_page_config(page_title="AES Encrypt/Decrypt + AI", layout="centered", page_icon="🔐")

st.title("🔐 Secure Text Encryptor & Decryptor + AI Assistant")
st.markdown("Encrypt and decrypt your messages using AES (CBC mode)")

#input
st.markdown("### Enter Your Message")
user_input = st.text_input("Your message", max_chars=100, placeholder="Enter text to encrypt or decrypt...")

col1, col2 = st.columns(2)
encrypt_clicked = col1.button("🔒 Encrypt")
decrypt_clicked = col2.button("🔓 Decrypt")

if encrypt_clicked and user_input:
    encrypted_text = encrypt(user_input)
    st.success("Encrypted Text (Base64):")
    st.code(encrypted_text, language='text')

if decrypt_clicked and user_input:
    decrypted_text = decrypt(user_input)
    st.success("Decrypted Text:")
    st.code(decrypted_text, language='text')

st.markdown("---")

#chatbot section

st.subheader("Chat with us")

groq_key = "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"  #key
client = Groq(api_key=groq_key)

prompt = st.text_input("Ask something a bout encryption, security, Streamlit, etc.")

if st.button("Ask AI"):
    if prompt:
        with st.spinner("Thinking..."):
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions about encryption, cybersecurity, and Streamlit."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success(chat_completion.choices[0].message.content)

st.markdown("---")
st.caption("Made with ❤️ by Kabir Khanuja")

# TODOS
# - Add support for different algorithms (RSA, DES, etc.)
# - File upload for encrypt/decrypt
# - Option to download encrypted/decrypted results
# - Dark mode / Light mode toggle
# - Use Claude / GPT-4o optionally with switch
