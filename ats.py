import re
from docx import Document
from PyPDF2 import PdfReader

# Function to extract text from DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages])

# Function to process resume and extract text
def extract_resume_text(file_path):
    if file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file type. Please use PDF or DOCX.")

# Function to clean and tokenize text
def clean_and_tokenize(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text.lower().split()

# Function to calculate ATS score
def calculate_ats_score(resume_text, job_description):
    resume_words = set(clean_and_tokenize(resume_text))
    job_words = set(clean_and_tokenize(job_description))
    matched_keywords = resume_words.intersection(job_words)
    score = (len(matched_keywords) / len(job_words)) * 100 if job_words else 0
    return round(score, 2), matched_keywords

# Main function
def main():
    # User inputs
    file_path = input("Please provide the resume file path (PDF/DOCX): ").strip()
    job_description = input("Paste the job description here: ").strip()

    try:
        # Extract resume text
        resume_text = extract_resume_text(file_path)
        print("\nResume text extracted successfully.")
        
        # Calculate ATS score
        score, matched_keywords = calculate_ats_score(resume_text, job_description)

        # Display results
        print("\nMatched Keywords:", matched_keywords)
        print(f"\nATS Score: {score}%")
        
        if score >= 70:
            print("Great job! Your resume aligns well with the job description.")
        elif score >= 40:
            print("Your resume matches the job description moderately. Consider adding more relevant keywords.")
        else:
            print("Your resume has low alignment with the job description. Consider tailoring it further.")
    
    except Exception as e:
        print("Error:", str(e))

# Entry point
if __name__ == "__main__":
    main()
