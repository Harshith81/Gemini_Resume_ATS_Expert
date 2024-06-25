from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st   
import os     
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai  
import docx

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))    

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])    
    return response.text   

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file Found or Uploaded 🔍")
    

## Streamlit App 


st.set_page_config(page_title="Your Resume ATS Expert 📃")
st.header("Resume ATS Expert 🕵️")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your Resume(format.pdf) here...",type=["pdf","docx"])


if uploaded_file is not None:
    st.write("PDF File Uploaded Successfully!!  🎯")


submit1 = st.button("Tell me about the Resume !!")

submit2 = st.button("What are the Strength's and Areas of Improvement ??")

submit3 = st.button("Percentage Match of Applicant Resume with JD !!")

# input_prompt1 = """
# You are an experienced human resource manager with 20+ years of technical experience in any one of the job fields of Data Science, Machine Learning, Devops, Cloud Computing, FullStack Web Development and your main task is to review the provided resume aganist the job description provided for these profiles.

# First you need to mention the basic details of the candidate based on the resume like name, education, projects, experience in an ordered format.Then please share your detailed professional evaluation on whether the candidates profile aligns with the job role and also highlight the reasons for either selecting or rejecting the candidates application based on your evaluation.
# """

input_prompt1="""

You are an experienced human resource manager with 20+ years of technical experience in any one of the job fields of Data Science, Machine Learning, Devops, Cloud Computing, FullStack Web Development and your main task is to review the provided resume aganist the job description provided for these profiles.

Extract and summarize the candidate's basic details, including name, education, projects, and experience in an ordered format from the resume. Provide a detailed professional evaluation of how well the candidate's profile aligns with the job role specified in the job description. Highlight reasons for selecting or rejecting the candidate based on your evaluation.
"""


# input_prompt2="""
# You are an experienced human resource manager with 20+ years of technical experience in any one of the job fields of Cloud Computing, Data Science, FullStack Web Development, Graphic Design, Machine Learning, Devops and your main task is to review the provided resume aganist the job description of these profiles according to the company requirements in current times.

# Also you should identify and mention the strengths and the areas of development i.e weakness,  so that based on which the percentage of acceptance of the candidate will get increased in the future in relation to the specified job role, along with this you should provide some guidance on learning some in-demand skills & also advise the candidate by giving some important courses and projects recommendations that are having a great demand.
# """

input_prompt2="""
Review the resume against the job description for roles in Cloud Computing, Data Science, FullStack Web Development, Graphic Design, Machine Learning, and Devops. Identify and specifically highlight mainly the strengths and areas needing improvement seperatley in clear and concise bullet points format. 

Then Suggest strategies tailored for the specified job role, including in-demand skills, recommended courses, and projects, but keep it minimal, straight forward and effective to the candidate job.
"""

# input_prompt3 = """
# You are an Skilled ATS (Application Tracking System) scanner with a deep understanding of  Graphic Design, Machine Learning, Cloud Computing, Devops, Data Science, FullStack Web Development, Big Data Engineering and deep ATS functionality.

# Your task is to evaluate the resume aganist the provided job description and give me the percentage of match if the resume matches with the job description. First the output should come as percentage and then the keywords missing and at last give your final thoughts.  
# """

input_prompt3="""
Evaluate the resume against the provided job description using ATS (Application Tracking System) scanner deep functionality. Calculate and Highlight the percentage match between the resume and job description at the top of the response. 

Then Highlight keywords and skills from the job description that are missing in the resume specifically and clearly in bullet points format listing all the important and main keywords and skills under different headings. 

At last Conclude with insights on the overall fit of the resume for the specified job role, but keep it minimal, straight forward and effective to the candidate job.   
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Resume Details: ")
        st.write(response)
    else:
        st.write("Please Upload Your Resume or File Not Uploaded 🔍")
        
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("Nature of Resume: ")
        st.write(response)
    else:
        st.write("Please Upload Your Resume or File Not Uploaded 🔍") 

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Resume x JD Match Percentage: ")
        st.write(response)
    else:
        st.write("Please Upload Your Resume or File Not Uploaded 🔍")     
