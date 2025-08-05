import os
import tempfile
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
from markdown_it import MarkdownIt

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Initialize Markdown-it
md = MarkdownIt()

@app.after_request
def add_header(response):
    """
    Add headers to prevent caching so the page resets on refresh.
    """
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

@app.route('/')
def index():
    """
    Renders the main page of the web application.
    """
    return render_template('index.html', response=None, error=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    This function is triggered when the user uploads files and clicks "Analyze".
    It uploads the files to the Gemini API and asks for a skill gap analysis.
    """
    try:
        # Configure the Gemini API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Access the uploaded files from the form
        resume_file = request.files.get('resume')
        jd_file = request.files.get('jd')

        if not resume_file or not jd_file or not resume_file.filename or not jd_file.filename:
            return render_template('index.html', error="Please upload both a resume and a job description.")

        # The Gemini SDK expects file paths. We'll save the uploaded files to a
        # temporary directory and pass those paths to the SDK.
        with tempfile.TemporaryDirectory() as tmpdir:
            resume_path = os.path.join(tmpdir, resume_file.filename)
            jd_path = os.path.join(tmpdir, jd_file.filename)
            resume_file.save(resume_path)
            jd_file.save(jd_path)

            # Upload files to the Gemini API
            print("Uploading files...")
            resume_upload = genai.upload_file(resume_path)
            jd_upload = genai.upload_file(jd_path)
            print("Files uploaded successfully.")

            # Create the generative model instance
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            # This prompt guides the model to perform the specific analysis we want.
            prompt = """
            Based on the provided resume and job description, please perform a detailed skill gap analysis.

            1.  **Required Skills:** List the key skills, technologies, and qualifications mentioned in the job description.
            2.  **Candidate's Skills:** List the relevant skills and experiences from the candidate's resume.
            3.  **Skill Gap Analysis:** Identify and list the specific skills that are required for the job but are missing or not clearly stated in the resume.
            4.  **Summary:** Provide a brief summary of how well the candidate matches the role and suggest areas for skill development.
            5.  **Learning Path:** Provide a well strucuted learning path to fill the skill gaps along with timeline.
            """

            # Generate content using the prompt and the uploaded files
            print("Generating analysis...")
            response = model.generate_content([prompt, resume_upload, jd_upload])
            print("Analysis complete.")
            
            # Convert markdown response to HTML
            html_response = md.render(response.text)
            
            # Render the template with the response
            return render_template('index.html', response=html_response)


    except Exception as e:
        # Basic error handling
        return render_template('index.html', error=f"An error occurred: {e}")
    
    # Default return in case the try block doesn't return anything
    return render_template('index.html', error="An unexpected error occurred.")

if __name__ == '__main__':
    # Runs the web application.
    # 'debug=True' allows you to see changes without restarting the server.
    app.run(debug=True)
