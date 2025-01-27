import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Streamlit Secrets (replace with placeholders)
def get_secret(secret_name):
  """Fetches a secret from Streamlit Secrets"""
  return st.secrets[secret_name]

SENDER_EMAIL = get_secret("SENDER_EMAIL")
SENDER_PASSWORD = get_secret("SENDER_PASSWORD")
RECEIVER_EMAIL = get_secret("RECEIVER_EMAIL")
CORRECT_PASSWORD = get_secret("CORRECT_PASSWORD")


def generate_prompts(product_name, product_description, target_market, product_price):
    prompts = [
        f"1. Create a marketing slogan for {product_name}, a {product_description}, targeting {target_market}.",
        f"2. Write a product description for {product_name}, emphasizing its benefits for {target_market}.",
        f"3. Generate a social media post promoting {product_name}, priced at {product_price}, to {target_market}.",
        f"4. Suggest 5 unique selling points for {product_name}, a {product_description}, for {target_market}.",
        f"5. Write an email campaign introducing {product_name} to {target_market}, highlighting its price of {product_price}.",
        f"6. Create a list of 10 potential blog post titles about {product_name} for {target_market}.",
        f"7. Generate a script for a 30-second advertisement for {product_name}, targeting {target_market}.",
        f"8. Write a press release announcing the launch of {product_name}, a {product_description}, priced at {product_price}.",
        f"9. Suggest ways to improve the packaging of {product_name} to appeal to {target_market}.",
        f"10. Generate a list of 5 influencers who could promote {product_name} to {target_market}."
    ]
    return prompts

def send_email(email_address):  # Add indentation for the function block
    message = MIMEText(f"New email signup: {email_address}")
    message['Subject'] = "New Signup for Free Web Apps"
    message['From'] = SENDER_EMAIL
    message['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        st.success("Thank you for subscribing! You'll receive updates soon.")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def main():
    st.title("Product Prompt Generator")

    entered_password = st.text_input("Enter Password:", type="password")

    if entered_password == CORRECT_PASSWORD:
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
