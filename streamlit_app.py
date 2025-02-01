import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure Google Generative AI API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Prompt template for ATS evaluation
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. if the same resume is parsed don't change the percentage for every loading .Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Streamlit app layout
st.set_page_config(page_title="ATS Resume Evaluation App", layout="wide", page_icon="📄")
st.title("📄 ATS Resume Evaluation App")
st.markdown("### Tailored Resume Feedback for ATS Success")

st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1f3c64, #232d3b);
            color: #fff;
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .css-ffhzg2 {
            background: transparent;
        }

        .streamlit-expanderHeader {
            background-color: transparent !important;
        }

        .css-1d391kg {
            background: transparent;
        }

        h1 {
            text-align: center;
            color: white;
            text-transform: uppercase;
            font-size: 3rem;
            text-shadow: 0 0 15px #25d366, 0 0 25px #25d366;
            margin-bottom: 20px;
            font-family: 'Montserrat', sans-serif;
            letter-spacing: 2px;
        }

        .main-container {
            max-width: 900px;
            width: 100%;
            padding: 30px;
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.7);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
            transition: all 0.3s ease-in-out;
        }

        .main-container:hover {
            transform: scale(1.02);
        }

        .streamlit-expanderContent {
            background-color: rgba(0, 0, 0, 0.5) !important;
            color: #fff;
        }

        .css-1v0mbdj {
            background-color: transparent;
        }

        .css-18e3th9 {
            border-radius: 5px;
        }

        .neon-button {
            background-color: #1d1d1d;
            border: 2px solid #ff0000;
            color: #fff;
            font-size: 18px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            border-radius: 10px;
            box-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #ff0000;
            transition: 0.3s ease;
        }

        .neon-button:hover {
            background-color: #ff0000;
            color: #1d1d1d;
            box-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000, 0 0 60px #ff0000;
        }

        .section-title {
            color: #ff6347;
            font-size: 1.5rem;
            text-shadow: 0 0 5px #ff6347, 0 0 10px #ff6347;
        }

        .results-summary {
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.8);
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        .results-summary h3 {
            color: #25d366;
        }
    </style>
""", unsafe_allow_html=True)

# Main layout with columns
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.subheader("📝 Job Description")
    jd = st.text_area(
        "Paste the Job Description", 
        height=250, 
        help="Copy and paste the job description here."
    )

with col2:
    st.subheader("📎 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF only)", 
        type="pdf", 
        help="Upload a PDF version of your resume."
    )

# Submit button
st.markdown("---")
submit = st.button("🚀 Evaluate Resume", type="primary", key="evaluate_button", use_container_width=True)

# Process the input and generate the response
if submit:
    if uploaded_file and jd:
        with st.spinner("Processing your resume..."):
            text = input_pdf_text(uploaded_file)
            formatted_prompt = input_prompt.format(text=text, jd=jd)
            response = genai.GenerativeModel("gemini-pro").generate_content(formatted_prompt).text

        # Improved output display
        st.success("✅ Resume evaluated successfully!")
        st.subheader("📊 Results Summary")
        st.markdown('<div class="results-summary">', unsafe_allow_html=True)

        # Parse response into dictionary
        try:
            response_data = eval(response)  # Use eval cautiously
            st.metric("Job Description Match", response_data.get("JD Match", "N/A"))
            
            st.markdown("#### Missing Keywords")
            missing_keywords = response_data.get("MissingKeywords", [])
            if missing_keywords:
                st.write(", ".join(missing_keywords))
            else:
                st.write("No missing keywords found!")

            st.markdown("#### Profile Summary")
            st.info(response_data.get("Profile Summary", "No summary provided."))
        except Exception as e:
            st.error("Failed to parse response. Please check the input format.")

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Please upload a resume and paste a job description.")