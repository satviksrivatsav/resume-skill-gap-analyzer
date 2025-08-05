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
    return render_template('index_final.html', response=None, error=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process uploaded files and perform skill gap analysis with custom prompt."""
    try:
        # Configure the Gemini API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Access the uploaded files and custom prompt from the form
        resume_file = request.files.get('resume')
        jd_file = request.files.get('jd')
        custom_prompt = request.form.get('custom_prompt', '').strip()

        if not resume_file or not jd_file or not resume_file.filename or not jd_file.filename:
            return render_template('index_final.html', error="Please upload both a resume and a job description.")

        # Process files to extract text content
        try:
            resume_text = process_file_content(resume_file)
            jd_text = process_file_content(jd_file)
        except Exception as e:
            return render_template('index_final.html', error=str(e))
        # Create the generative model instance
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Build the prompt with optional custom prompt
        base_prompt = prompt = f"""
        **Your Role:** You are an expert career coach and professional technical recruiter. Your goal is to provide a highly detailed and actionable analysis for a job applicant.

        **Your Task:** Meticulously compare the provided Resume against the Job Description. Your analysis must be direct, honest, and encouraging.

        **Instructions:**
        1.  **Analyze the Resume:** First, thoroughly read and understand the candidate's experience, skills, and projects listed in the resume text below.
        2.  **Analyze the Job Description:** Next, carefully examine the 'Required Qualifications' and 'Key Responsibilities' from the job description text.
        3.  **Identify Skill Gaps:** First, create a table(in markdown) where we quickly check the job requirements are met or not one by one, the first column of the table should contain the job reuirements and the second column should contain whether the job requirement is met or not(include a tick, cross emojis along with the condition respectively and also include an appropriate emoji for the ambiguity states). 
              Next, Create a list of the most critical skills and qualifications that are explicitly mentioned in the job description but are NOT present or well-supported in the resume. For each gap, briefly explain why it's important for the role.
        4.  **Create a Learning Path:** For each identified skill gap, create a concrete, step-by-step learning plan. This plan should have a timeline (e.g., Week 1-2, Month 2-3) and include specific, actionable recommendations.
        5.  **Suggest a Project:** Recommend one specific portfolio project that the candidate could build to demonstrate multiple missing skills at once.

        **Output Formatting Rules:**
        *   Use Markdown for all formatting.
        *   The main sections must be: `## Skill Gap Analysis` and `## Personalized Learning Path`.
        *   Use bold text (`**Skill:**`) to highlight each skill gap.
        *   Use bullet points (`*`) for all lists and learning steps.
        *   Do not write a generic introduction or conclusion. Be direct and get straight to the analysis.

        ---
        **[BEGIN RESUME TEXT]**
        {resume_text}
        **[END RESUME TEXT]**
        ---
        **[BEGIN JOB DESCRIPTION TEXT]**
        {jd_text}
        **[END JOB DESCRIPTION TEXT]**
        ---
        """

        # Add custom prompt if provided
        if custom_prompt:
            prompt = f"{base_prompt}\n\n**Additional Instructions:**\n{custom_prompt}"
        else:
            prompt = base_prompt

        # Generate content using the prompt and the extracted text
        response = model.generate_content(prompt)
        
        # Convert markdown response to HTML
        html_response = md.render(response.text)
        
        # Render the template with the response
        return render_template('index_final.html', response=html_response)

    except Exception as e:
        return render_template('index_final.html', error=f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
