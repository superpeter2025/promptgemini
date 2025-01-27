import streamlit as st
import smtplib
from email.mime.text import MIMEText

def generate_prompts(product_name, product_description, target_market, product_price):
    # ... (same as before)

def send_email(email_address):
    sender_email = st.secrets["SENDER_EMAIL"]
    sender_password = st.secrets["SENDER_PASSWORD"]
    receiver_email = st.secrets["RECEIVER_EMAIL"]

    message = MIMEText(f"New email signup: {email_address}")
    message['Subject'] = "New Signup for Free Web Apps"
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)
        st.success("Thank you for subscribing! You'll receive updates soon.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def main():
    st.title("Product Prompt Generator")

    correct_password = st.secrets["CORRECT_PASSWORD"]
    entered_password = st.text_input("Enter Password:", type="password")

    if entered_password == correct_password:
        if 'all_prompts' not in st.session_state:
            st.session_state.all_prompts = []

        product_name = st.text_input("Product Name:")
        product_description = st.text_input("Describe the product in 25 words:")
        target_market = st.text_input("Describe the target market in 25 words:")
        product_price = st.text_input("Product Price:")

        if st.button("Generate Prompts"):
            if all([product_name, product_description, target_market, product_price]):
                new_prompts = generate_prompts(product_name, product_description, target_market, product_price)
                st.session_state.all_prompts.extend(new_prompts)
                st.success("10 prompts generated and added to prompts.txt!")
            else:
                st.error("Please fill in all fields.")

        if st.session_state.all_prompts:
            prompt_text = "\n\n".join(st.session_state.all_prompts)
            st.download_button(
                label="Download prompts.txt",
                data=prompt_text,
                file_name="prompts.txt",
                mime="text/plain"
            )
            st.subheader("Preview of prompts.txt")
            st.text(prompt_text[:1000] + ("..." if len(prompt_text) > 1000 else ""))

        st.subheader("Get More Free Web Apps!")
        email_address = st.text_input("Enter your email address:")
        if st.button("Submit"):
            if email_address:
                send_email(email_address)
            else:
                st.warning("Please enter your email address.")

    elif entered_password:
        st.error("Incorrect Password")

if __name__ == "__main__":
    main()