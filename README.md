# PDF Intelligence📄🤖

**AI-powered PDF analysis, summarization, and question answering.**

PDF Intelligence is a Python application that uses Google Gemini to help users extract insights from PDF documents. It transforms document text into structured findings and generates summaries, key points, and document-based answers through a simple interactive interface.

## Overview

Working with lengthy documents can make it difficult to find relevant information quickly. PDF Intelligence streamlines this process by combining PDF text extraction, structured AI analysis, and task-specific prompting in one application.

Users can upload a PDF, select an analysis mode, configure AI generation settings, and view or download the results.

## ✨Features

- **PDF Text Extraction:** Extract readable text from uploaded PDF documents.
- **Document Summarization:** Generate concise summaries highlighting the document's main ideas.
- **Key Point Extraction:** Identify important information and customize the number of key points.
- **Question Answering:** Ask questions about a document and receive answers grounded in its content.
- **Two-Stage AI Workflow:** Organize document information into structured findings before generating the final response.
- **Configurable Generation:** Adjust the AI thinking level and maximum output length.
- **Downloadable Results:** Save generated responses as text files.
- **Error Handling:** Provide feedback for PDF processing issues and common API errors.
- **Interactive Interface:** Use the application through a Streamlit web interface.

## 🛠️Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and processing |
| Streamlit | Interactive web interface |
| Google Gemini API | AI-powered document analysis and generation |
| Google Gen AI SDK | Communication with the Gemini API |
| pypdf | PDF text extraction |
| python-dotenv | Environment variable and API key management |

## ⚙️How It Works

The application follows a two-stage processing workflow.

1. **Upload:** The user uploads a PDF document.
2. **Extract:** The application extracts readable text from the document.
3. **Analyze:** The first AI stage identifies topics, extracts important facts, organizes information, and prepares structured findings.
4. **Generate:** The second AI stage uses those findings and task-specific instructions to produce a summary, key points, or an answer.
5. **Review and Export:** The user reviews the output and can download the generated result.

This separation helps distinguish document analysis from the final response-generation task.

## Prompt Engineering

PDF Intelligence incorporates several prompt-engineering techniques:

- **Structured prompting:** Breaks document analysis into explicit steps and organizes findings into defined sections.
- **Task-specific prompting:** Uses different instructions for summarization, key-point extraction, and question answering.
- **Few-shot prompting:** Provides an example to demonstrate the expected format for key-point extraction.
- **Grounding constraints:** Instructs the model to base responses on document content and avoid inventing unsupported information.
- **Output constraints:** Specifies response structure, conciseness, and the requested number of key points.

These techniques help make the AI workflow more consistent, focused, and appropriate for each task.

## Getting Started

### Prerequisites

- Python 3.10 or later
- A Google Gemini API key
- Internet access for API requests

### 1. Clone the repository

```bash
git clone https://github.com/anasahmed7/PDF-Intelligence.git
cd PDF-Intelligence
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install streamlit pypdf python-dotenv google-genai
```

### 4. Configure the API key

Obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey).

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Security:** Keep your API key private. The `.env` file should remain excluded from Git using `.gitignore`. Never commit API keys or other secrets to the repository.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, typically:

`http://localhost:8501`

## Usage

1. Launch the application.
2. Upload a PDF document.
3. Select one of the available modes:
   - Ask a question
   - Summarize PDF
   - Extract Key Points
4. Configure the available AI settings.
5. Start the analysis and review the generated response.
6. Download the result if needed.

## Project Structure

```text
PDF-Intelligence/
├── app.py          # Streamlit application and AI workflow
├── .gitignore      # Excludes secrets and unnecessary files
├── README.md       # Project documentation
└── .env            # Local API configuration (not committed)
```

## Security and Data Handling

- API credentials are loaded from environment variables rather than hardcoded in the source code.
- The `.env` file is excluded from version control.
- PDF text is sent to the configured Gemini API for AI processing. Do not submit confidential or sensitive documents unless you are authorized to share them with that service.

## Future Enhancements

Potential improvements include:

- OCR support for scanned PDF documents.
- More efficient processing of long documents.
- Conversation history and follow-up questions.
- Support for additional document formats.
- Evaluation tools for comparing prompt strategies and response quality.
- Automated tests for PDF processing and AI workflow components.

## Author

**Anas Ahmed**

- GitHub: [@anasahmed7](https://github.com/anasahmed7)

---

*PDF Intelligence — turning PDF documents into useful, accessible insights with generative AI.*