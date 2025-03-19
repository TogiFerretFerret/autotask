# AI Assistant - Gemini

This AI assistant, named Gemini, has been significantly enhanced with new features, including internet access via Grok and integration with Stockfish for advanced chess analysis.

## Usage Instructions

To use this AI assistant, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/TogiFerretFerret/autotask.git
   cd autotask
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the AI assistant:
   ```bash
   python main.py --mode screen
   ```

## Enhanced Intelligence and Internet Access

The AI assistant now uses langchain and gpt4free to connect to Grok for better internet access. This allows the AI to perform more complex tasks and provide more accurate responses.

## Stockfish Integration

The AI assistant integrates with Stockfish for advanced chess analysis. This allows the AI to provide accurate and insightful chess moves and strategies.

## Features

- **Internet Access**: Connects to Grok for better internet access.
- **Stockfish Integration**: Provides advanced chess analysis.
- **Screen Mode**: Operates in screen mode to capture and analyze screen content.
- **Voice Interaction**: Uses pyaudio for voice interaction.
- **Image Recognition**: Utilizes OpenCV and PIL for image recognition.
- **Text Recognition**: Uses pytesseract for text recognition.
- **Mouse and Keyboard Control**: Controls mouse and keyboard using pyautogui.
- **Cross-Platform**: Works on Windows, MacOS, and Linux.

## AI Assistant Name

The AI assistant is named **Gemini**.

## Instructions for Astral's UV Python Package Manager

Astral's UV Python Package Manager is a powerful tool for managing Python packages. Follow the instructions below to install and use it.

### Installation

1. Install the UV package manager using pip:
   ```bash
   pip install uv
   ```

2. Verify the installation:
   ```bash
   uv --version
   ```

### Usage

#### Installing Packages

To install a package using UV, use the following command:
```bash
uv install <package_name>
```

#### Uninstalling Packages

To uninstall a package using UV, use the following command:
```bash
uv uninstall <package_name>
```

#### Listing Installed Packages

To list all installed packages, use the following command:
```bash
uv list
```

#### Updating Packages

To update a package to the latest version, use the following command:
```bash
uv update <package_name>
```

#### Searching for Packages

To search for a package, use the following command:
```bash
uv search <package_name>
```

### Additional Information

For more information and advanced usage, refer to the official documentation:
[UV Python Package Manager Documentation](https://example.com/uv-docs)

## Running Tests

### Running Tests Locally

To run the tests locally using `pytest`, follow these steps:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   pytest tests
   ```

### Running Tests in Codespaces

To run the tests in Codespaces, follow these steps:

1. Open the repository in Codespaces.

2. Open a terminal in Codespaces.

3. Run the tests:
   ```bash
   pytest tests
   ```

### Running Tests using Docker

To run the tests using Docker, follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t ai-assistant-gemini .
   ```

2. Run the tests:
   ```bash
   docker run --rm ai-assistant-gemini
   ```
