import streamlit as st
import json
import os
import webbrowser
import logging
from datetime import datetime
import sys

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Redirect stdout and stderr to browser's console
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf8', buffering=1)

def main():
    st.title("MAWM CODE COMPARATOR")

    # Layout setup
    left_column, right_column = st.columns(2)

    # Left side - Source Organisation
    with left_column:
        st.subheader("Source Organisation")
        source_username = st.text_input("Source Username")
        log_username(source_username)  # Log the username
        source_password = st.text_input("Source Password", type="password")
        source_organization = st.text_input("Source Organisation")

    # Right side - Target Organisation
    with right_column:
        st.subheader("Target Organisation")
        target_username = st.text_input("Target Username")
        log_username(target_username)  # Log the username
        target_password = st.text_input("Target Password", type="password")
        target_organization = st.text_input("Target Organisation")

    # Additional fields
    category = st.radio("Category", ["Component", "Extension Pack"])

    selected_items = []
    if category == "Component":
        selected_items = st.multiselect("Select Components", ["Picking", "Packing", "DC Order", "Inventory", "Items"])
    elif category == "Extension Pack":
        uploaded_file = st.file_uploader("Upload JSON file", type="json")
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                extension_names = [entry.get("OneBoardName", "Unknown") for entry in data]
                selected_items = st.multiselect("Select Extension Packs", extension_names)
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON file which contains OneBoardName.")

    # Tech to compare field
    tech_to_compare = st.selectbox("Tech to Compare", ["Handler", "Service Definition", "Metadata", "Extended Attribute", "Message Types", "Application Parameter", "DSL"])

    email_id = st.text_input("Email ID")

    # Compare button
    if st.button("Compare"):
        if not all([source_username, source_password, source_organization,
                    target_username, target_password, target_organization,
                    email_id, category, selected_items, tech_to_compare]):
            st.error("Please fill in all required fields before proceeding.")
        elif tech_to_compare == "Extended Attribute" and source_organization == target_organization:
            st.error("For Extended Attribute, source and destination organizations should be different.")
        else:
            file_name = f"Mukta{datetime.now().strftime('%d%b%Y')}.html"  # e.g., Mukta15Apr2024.html
            folder_path = os.path.join("html_files", file_name)
            create_html_file(folder_path, source_username, source_password, source_organization,
                             target_username, target_password, target_organization,
                             email_id, category, selected_items, tech_to_compare)
            open_in_new_tab(folder_path)

def log_username(username):
    if username:
        logging.info(f"Username entered: {username}")

def create_html_file(file_path, source_username, source_password, source_organization,
                     target_username, target_password, target_organization,
                     email_id, category, selected_items, tech_to_compare):
    try:
        # Construct message with user inputs
        message = f"<h1>MAWM CODE COMPARATOR</h1>"
        message += "<h2>User Inputs:</h2>"
        message += f"<p>Source Username: {source_username}</p>"
        message += f"<p>Source Password: {source_password}</p>"
        message += f"<p>Source Organisation: {source_organization}</p>"
        message += f"<p>Target Username: {target_username}</p>"
        message += f"<p>Target Password: {target_password}</p>"
        message += f"<p>Target Organisation: {target_organization}</p>"
        message += f"<p>Email ID: {email_id}</p>"
        message += f"<p>Category: {category}</p>"
        if selected_items:
            message += "<p>Selected Items:</p>"
            message += "<ul>"
            for item in selected_items:
                message += f"<li>{item}</li>"
            message += "</ul>"
        message += f"<p>Tech to Compare: {tech_to_compare}</p>"

        # Write message to HTML file
        with open(file_path, "w") as f:
            f.write(message)
    except Exception as e:
        logging.error(f"Error occurred while creating HTML file: {e}")

def open_in_new_tab(file_path):
    try:
        webbrowser.open_new_tab(file_path)
        logging.info(f"Opened new tab with file: {file_path}")
    except Exception as e:
        logging.error(f"Error occurred while opening new tab: {e}")

if __name__ == "__main__":
    main()
