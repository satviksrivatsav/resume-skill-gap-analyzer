import os
import tempfile
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
from markdown_it import MarkdownIt
from docx import Document
import PyPDF2

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Initialize Markdown-it
md = MarkdownIt()

def extract_text_from_docx(file):
    """Extract text content from .docx files"""
    try:
        doc = Document(file)
        text_content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_content.append(paragraph.text)
        return '\n'.join(text_content)
    except Exception as e:
        raise Exception(f"Error processing .docx file: {str(e)}")

def extract_text_from_pdf(file):
    """Extract text content from PDF files"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text_content = []
        for page in pdf_reader.pages:
            text_content.append(page.extract_text())
        return '\n'.join(text_content)
    except Exception as e:
        raise Exception(f"Error processing PDF file: {str(e)}")

def process_file_content(file):
    """Process uploaded file and return text content"""
    filename = file.filename.lower()
    
    if filename.endswith('.docx'):
        return extract_text_from_docx(file)
    elif filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        # For other file types, try to read as text
        try:
            return file.read().decode('utf-8')
        except:
            raise Exception(f"Unsupported file format: {filename}")

@app.after_request
def add_header(response):
    """Add headers to prevent caching"""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

@app.route('/')
def index():
    """Renders the main page of the web application."""
    return render_template('index.html', response=None, error=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process uploaded files and perform skill gap analysis."""
    try:
        # Configure the Gemini API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Access the uploaded files from the form
        resume_file = request.files.get('resume')
        jd_file = request.files.get('jd')

        if not resume_file or not jd_file or not resume_file.filename or not jd_file.filename:
            return render_template('index.html', error="Please upload both a resume and a job description.")

        # Process files to extract text content
        try:
            resume_text = process_file_content(resume_file)
            jd_text = process_file_content(jd_file)
        except Exception as e:
            return render_template('index.html', error=str(e))

        # Create the generative model instance
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Prompt for skill gap analysis
        prompt = f"""
        Based on the provided resume and job description, please perform a detailed skill gap analysis.

        **Resume Content:**
        {resume_text}

        **Job Description Content:**
        {jd_text}

        1. **Required Skills:** List the key skills, technologies, and qualifications mentioned in the job description.
        2. **Candidate's Skills:** List the relevant skills and experiences from the candidate's resume.
        3. **Skill Gap Analysis:** Identify and list the specific skills that are required for the job but are missing or not clearly stated in the resume.
        4. **Summary:** Provide a brief summary of how well the candidate matches the role and suggest areas for skill development.
        5. **Learning Path:** Provide a well structured learning path to fill the skill gaps along with timeline.
        """

        # Generate content using the prompt and the extracted text
        response = model.generate_content(prompt)
        
        # Convert markdown response to HTML
        html_response = md.render(response.text)
        
        # Render the template with the response
        return render_template('index.html', response=html_response)

    except Exception as e:
        return render_template('index.html', error=f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
