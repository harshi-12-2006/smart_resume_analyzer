import streamlit as st
import google.generativeai as genai
import pypdf

# 1. SETUP THE AI BRAIN
# Go to Google AI Studio to get a free API Key, then paste it inside the quotes below
GOOGLE_API_KEY = "GOOGLE_API_KEY = YOUR_API_KEY_HERE"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. FUNCTION TO READ THE PDF RESUME
def extract_text_from_pdf(uploaded_file):
    reader = pypdf.PdfReader(uploaded_file)
    text = ""
    # Loop through every page of the PDF and grab the words
    for page in reader.pages:
        text += page.extract_text()
    return text

# 3. BUILD THE VISUAL WEBSITE SCREEN
st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")
st.title("🚀 Smart Resume Analyzer")
st.subheader("Hackathon Edition: Context & Skill Gap Evaluation")

# Input 1: The Job Description box
job_description = st.text_area("Paste the Target Job Description here:", height=150)

# Input 2: The File Upload button
uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type=["pdf"])

# 4. WHAT HAPPENS WHEN THE USER CLICKS "ANALYZE"
if st.button("Run Deep Analysis"):
    # Safety Check: Make sure they actually gave us both pieces of information
    if not job_description or not uploaded_file:
        st.error("Please paste a Job Description AND upload a PDF resume first!")
    else:
        with st.spinner("AI is analyzing context and experience... Please wait..."):
            try:
                # Extract text from the uploaded PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # Formulate the secret instructions (Prompt) for the AI
                prompt = f"""
                You are an elite corporate tech recruiter. Analyze the following Resume text against the target Job Description text.
                Do not just look for keywords. Analyze the depth of their experience and actual projects.
                
                Provide your response in plain text with the following structure:
                - OVERALL SCORE: Give a rating from 0 to 100 based on fit.
                - EXPERIENCE ALIGNMENT: Explain in 2 sentences if their career depth matches the JD.
                - CRITICAL MISSING SKILLS: List 3-5 crucial skills or concepts missing from the resume.
                - ACTIONABLE TIPS: List 2 practical things they can add or rewrite to win this job.

                Job Description: {job_description}
                Resume: {resume_text}
                """
                
                # Send the text to Gemini AI 1.5 Flash (Super fast and reliable for hackathons)
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)
                
                # Show the AI results cleanly on the screen
                st.success("Analysis Complete!")
                st.markdown("### 📊 Evaluation Dashboard")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")