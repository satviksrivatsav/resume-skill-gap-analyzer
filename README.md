# AI Skill Gap Analyzer

*A web application that uses a Large Language Model to analyze a resume against a job description and generate a personalized learning path to bridge skill gaps.*

---

## About The Project

This project was born from a desire to bridge the gap between a candidate's current skillset and the requirements of their dream job. Often, it's difficult to know exactly what skills to learn or where to focus your efforts. This tool aims to solve that problem by providing automated, intelligent, and actionable feedback.

The user simply uploads their resume and the job description they are targeting. The back-end, powered by Python and Flask, sends this information to the Google Gemini API. The Large Language Model then performs a detailed analysis and generates a report identifying key skill deficiencies and, most importantly, a structured learning plan to address them.

**This project also marks my first journey into the exciting world of integrating LLM APIs. It has been a fantastic learning experience in prompt engineering, API communication, and building a truly intelligent application from the ground up.**

### Key Features

*   Simple, clean web interface for file uploads.
*   Directly compares a user's resume with a target job description.
*   Utilizes the Google Gemini API for state-of-the-art text analysis.
*   Generates a clear list of identified skill gaps.
*   Provides a custom, timeline-based learning path with actionable suggestions.

---

## Technology Stack

*   **Back-End:** Python, Flask
*   **Front-End:** HTML, CSS
*   **LLM API:** Google Gemini

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

*   Python 3.7+ installed on your system.
*   `pip` (Python's package installer).
*   A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/).

### Installation and Setup

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install Required Python Packages**
    ```sh
    pip install Flask google-generativeai
    ```

3.  **Add Your API Key**
    *   Open the `app.py` file in your code editor.
    *   Find the following line:
        ```python
        genai.configure(api_key="YOUR_API_KEY_HERE")
        ```
    *   Replace `"YOUR_API_KEY_HERE"` with your actual Google Gemini API key.
    *   **Important:** Keep your API key private. Do not commit it to a public repository.

4.  **Run the Application**
    ```sh
    python app.py
    ```

5.  **View the App**
    *   Once you run the command, you will see output in your terminal indicating that the server is running. It will look something like this:
        ```
         * Running on http://127.0.0.1:5000
        ```
    *   Open your web browser and navigate to **http://127.0.0.1:5000**.

You should now see the application's interface and be able to upload files for analysis!

---

## Project Structure

```
.
├── app.py              # The main Flask application file
└── templates/
    └── index.html      # The HTML file for the user interface
```


## How It Works

The application's logic is straightforward and centered around the `app.py` script.

1.  **User Interface:** The user is first presented with the `index.html` page, which contains a simple form with two file input fields (for the resume and job description) and a submit button.

2.  **Form Submission:** When the user clicks the "Analyze Skill Gaps" button, the form data (including the files) is sent via a `POST` request to the `/analyze` endpoint of the Flask application.

3.  **Back-End Processing:** The `/analyze` function in `app.py` handles the request:
    *   It receives the uploaded files.
    *   It reads the text content from each file, decoding it into a universal `utf-8` format.
    *   It dynamically inserts this text into a carefully crafted **prompt**.

4.  **API Communication:**
    *   The complete prompt is sent to the Google Gemini API.
    *   The application then waits for the LLM to process the request and generate a response.

5.  **Displaying Results:**
    *   The text response from the API is captured.
    *   The `index.html` page is rendered again, but this time it is passed the API's response.
    *   The template uses a simple conditional check to see if a response exists, and if so, displays it in a dedicated section on the page.

---

## The Heart of the Project: Prompt Engineering

The success of this application hinges on the quality of the prompt sent to the LLM. A simple request yields a simple answer. For a detailed, well-structured analysis, a more sophisticated prompt is required.

Our prompt is engineered with the following principles in mind:

1.  **Assigning a Persona:** We instruct the AI to act as an "expert career coach and professional technical recruiter." This sets the context and tone, leading to a more professional and insightful response.

2.  **Providing Explicit Instructions:** The prompt gives the AI a clear, step-by-step guide: first analyze the resume, then the JD, then identify the gaps, and finally create a learning path. This structured approach prevents the AI from missing key tasks.

3.  **Defining the Output Format:** We command the AI to format its entire response using Markdown, specifying the exact headings (`##`) and list styles (`*`) to use. This ensures a consistent and clean presentation in the front-end every single time.

This level of detail in the prompt is what elevates the application from a simple text generator to a useful analysis tool.

---

## Potential Future Improvements

This project serves as a strong foundation, but there are many exciting ways it could be extended:

*   **Support for More File Types:** Add functionality to parse text from `.pdf` and `.docx` files, as many resumes are in these formats. Libraries like `PyMuPDF` and `python-docx` would be great for this.
*   **Analyze from URL:** Allow users to paste a URL to a job posting (e.g., from LinkedIn) instead of uploading a file. This would involve adding a web scraping library like `BeautifulSoup`.
*   **User Accounts:** Implement a simple user database (e.g., using SQLite) to allow users to save their past analyses and track their progress.
*   **Interactive Feedback:** Allow users to click on a skill in the learning path to get more detailed resources or mark it as "in progress" or "completed."

---

## License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## Acknowledgments

*   [Flask](https://flask.palletsprojects.com/) - For making web development in Python so accessible.
*   [Google Gemini](https://deepmind.google/technologies/gemini/) - For the powerful generative capabilities.
*   And to everyone who has ever written a "how-to" guide that helps new developers get started!```
