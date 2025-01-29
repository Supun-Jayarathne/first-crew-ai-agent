import warnings
import PyPDF2
import gradio as gr
from extract_report_agent.crew import ExtractReportAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

topic = ''

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': topic,
    }
    
    try:
        ExtractReportAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

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
    global topic
    topic = cv_content
    final_answer = ExtractReportAgent().crew().kickoff(inputs={'topic': topic})
    return final_answer

iface = gr.Interface(
    fn=run_crewai_app,
    inputs=[gr.File(file_types=[".pdf"])],
    outputs="text",
    title="CrewAI CV Extractor",
    description="Upload a CV to extract project details from the CV."
)

iface.launch(share=True)
