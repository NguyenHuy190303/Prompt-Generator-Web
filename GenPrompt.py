import streamlit as st
import sqlite3
import re
import requests
import base64

# Initialize Database
def init_db():
    conn = sqlite3.connect('prompts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS submitted_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Fetch Prompts from Database
def fetch_prompts():
    conn = sqlite3.connect('prompts.db')
    c = conn.cursor()
    c.execute('SELECT id, title, content FROM prompts')
    prompts = c.fetchall()
    conn.close()
    return prompts

# Insert Submitted Prompt
def insert_submitted_prompt(title, content):
    conn = sqlite3.connect('prompts.db')
    c = conn.cursor()
    c.execute('INSERT INTO submitted_prompts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()

# Upload the updated database file to GitHub
def upload_to_github():
    github_repo = "NguyenHuy190303/Prompt-Generator-Web"
    github_token = "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"
    file_path = "prompts.db"
    branch = "main"
    github_api_url = f"https://api.github.com/repos/{github_repo}/contents/{file_path}"

    # Read the contents of the file
    with open(file_path, "rb") as f:
        content = f.read()
    
    # Get the current file's SHA
    response = requests.get(github_api_url, headers={
        "Authorization": f"token {github_token}"
    })
    response_json = response.json()
    sha = response_json['sha'] if 'sha' in response_json else None

    # Create the payload
    payload = {
        "message": "Update prompts.db",
        "content": base64.b64encode(content).decode("utf-8"),
        "branch": branch
    }
    if sha:
        payload["sha"] = sha

    # Upload the file
    response = requests.put(github_api_url, headers={
        "Authorization": f"token {github_token}"
    }, json=payload)
    
    if response.status_code == 200 or response.status_code == 201:
        st.success("Database updated on GitHub successfully!")
    else:
        st.error("Failed to update the database on GitHub.")

# Main Application
def main():
    st.sidebar.image("logo.jpg", use_column_width=True)
    st.sidebar.markdown("<h3 style='text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>Leo</h3>", unsafe_allow_html=True)
    st.title("Prompt Generator")
    menu = ["Generate Prompt", "Suggest Prompt"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Generate Prompt":
        st.subheader("Generate Prompt")
        prompts = fetch_prompts()
        prompt_titles = [prompt[1] for prompt in prompts]
        selected_prompt_title = st.selectbox("Select a Prompt", prompt_titles)

        if selected_prompt_title:
            selected_prompt = next(prompt for prompt in prompts if prompt[1] == selected_prompt_title)
            prompt_content = selected_prompt[2]
            placeholders = re.findall(r'\[([^\]]+)\]', prompt_content)
            unique_placeholders = list(dict.fromkeys(placeholders))
            user_inputs = {}
            for i, placeholder in enumerate(unique_placeholders):
                user_inputs[placeholder] = st.text_input(f"Enter {placeholder}", key=f"{selected_prompt[0]}_{i}_{placeholder}")

            if st.button("Generate"):
                for placeholder, user_input in user_inputs.items():
                    prompt_content = prompt_content.replace(f"[{placeholder}]", user_input)
                st.text_area("Generated Prompt", prompt_content, height=400)

    elif choice == "Suggest Prompt":
        st.subheader("Suggest a New Prompt")
        title = st.text_input("Prompt Title")
        content = st.text_area("Prompt Content")

        if st.button("Submit"):
            if title and content:
                insert_submitted_prompt(title, content)
                st.success("Prompt của bạn sẽ được cân nhắc kĩ lưỡng trước khi có trong hệ thống, Leo cảm ơn sự đóng góp của bạn.")
                upload_to_github()
            else:
                st.warning("Vui lòng điền đầy đủ thông tin.")

if __name__ == '__main__':
    init_db()
    main()
