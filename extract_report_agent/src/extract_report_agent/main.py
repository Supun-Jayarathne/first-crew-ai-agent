import warnings
import PyPDF2
import gradio as gr
from extract_report_agent.crew import ExtractReportAgent
from transformers import pipeline
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

content = ''

def run():
    """
    Run the crew.
    """
    inputs = {
        'content': content,
    }
    
    try:
        ExtractReportAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def summarize_text(text, max_length=1000):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def read_cv_content(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            content += page.extract_text()
    return content


def run_crewai_app(cv_file):
    cv_content = read_cv_content(cv_file.name)
    summarized_content = summarize_text(cv_content)
    global content
    content = summarized_content
    final_answer = ExtractReportAgent().crew().kickoff(inputs={'content': content})
    return final_answer

iface = gr.Interface(
    fn=run_crewai_app,
    inputs=[gr.File(file_types=[".pdf"])],
    outputs="text",
    title="CrewAI CV Extractor and Blog Writer",
    description="Upload a CV to extract project details from the CV and write a blog post about the technologies.",
    css="footer{display:none !important}",
    flagging_options=[],
)

iface.launch(share=True)
