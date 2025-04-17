# AI-Powered Custom Terminal

An interactive terminal that integrates AI assistance to help users execute shell commands, debug errors, and navigate their system more efficiently. This tool is powered by OpenAI's GPT model and includes features like command history, autocomplete, and AI-generated suggestions for error handling.

---

## Features

- **AI-Assisted Command Generation**: Use natural language queries (e.g., "ai list all files in this folder") to generate shell commands with AI.
- **Error Handling with AI Suggestions**: When a command fails, the AI suggests possible fixes based on the error message.
- **Command History**: Save and view previously executed commands for quick reference.
- **Autocomplete**: Autocomplete file paths and directories using the `Tab` key.
- **Interactive Commands Support**: Supports interactive commands like `nano`, `vim`, `ssh`, etc., preserving terminal behavior.
- **Customizable Prompt**: Displays the current working directory in the prompt.
- **Cross-Platform Compatibility**: Works on Linux, macOS, and Windows (with WSL).

---

## Prerequisites

Before running the terminal, ensure you have the following:

1. **Python 3.8+**: The script is written in Python and requires version 3.8 or higher.
2. **OpenAI API Key**: You need an API key from OpenAI to use the GPT model. Get it [here](https://platform.openai.com/account/api-keys).
3. **Environment Variables**: Store your OpenAI API key in a `.env` file (see setup instructions below).
4. **Required Python Libraries**:
   - `openai`
   - `python-dotenv`
   - `colorama`

Install the required libraries using pip:

```bash
pip install openai python-dotenv colorama
```

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-powered-terminal.git
   cd ai-powered-terminal
   ```

2. **Create a `.env` File**:
   Create a `.env` file in the root directory of the project and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Install Dependencies**:
   Ensure you have installed the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Terminal**:
   Start the terminal by running the Python script:
   ```bash
   python terminal.py
   ```

---

## Usage

### Basic Commands

- **Change Directory**:
  ```bash
  cd path/to/directory
  ```

- **List Files**:
  ```bash
  ls
  ```

- **Clear Screen**:
  ```bash
  clear
  ```

- **Exit Terminal**:
  ```bash
  exit
  ```

### AI Assistance

- **Request AI Help**:
  Prefix your query with `ai` to request AI-generated shell commands:
  ```bash
  ai list all files in this folder
  ```

- **Modify and Execute AI Suggestions**:
  After receiving an AI-generated command, you can modify it or press Enter to execute it as-is.

### Command History

- **View History**:
  ```bash
  history
  ```

- **Re-run Previous Commands**:
  Use the arrow keys to navigate through previous commands or type `history` to see a numbered list.

### Error Handling

If a command fails, the terminal will display an AI-generated suggestion to fix the issue.

---

## Contributing

Contributions are welcome! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature or fix"
   ```
4. Push your branch to GitHub:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## Acknowledgments

- **OpenAI**: For providing the powerful GPT models used in this project.
- **Colorama**: For adding colorful output to the terminal.
- **Python-Dotenv**: For managing environment variables securely.

---
