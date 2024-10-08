# Prompt Generator Web Application

The **Prompt Generator Application** is a Python-based GUI tool built with **streamlit** that allows users to generate prompts based on predefined templates and suggest new prompts for review.
## Features

- **Generate Prompt**
  - Select from existing prompts.
  - Fill placeholders dynamically.
  - Generate customized prompts.

- **Suggest Prompt for Leo**
  - Submit new prompts for review.
  - Requires title and content input.
  - Prompts are stored for administrative review.

- **Prompt Management Script**
  - Approve or reject submitted prompts.
  - Manage prompt database (`prompts.db`) operations:
    - Initialize database.
    - Remove duplicates.
    - Recreate table structure.
    - Refresh displayed prompts.

## 🛠️ Dependencies

- **tkinter**: GUI toolkit for Python.
- **Pillow**: Image processing library for handling images in the GUI.
- **pyperclip**: Library for copying text to the clipboard.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NguyenHuy190303/Prompt-Generator-Web
1. Move to project folder:

   ```bash
   cd Prompt-Generator-Web
3. Run app:

   ```bash
   streamlit run GenPrompt.py
