#!/usr/bin/env python
import sys
import warnings
import PyPDF2
import gradio as gr

from datetime import datetime

from extract_report_agent.crew import ExtractReportAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
topic = ''

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': topic,
        # 'current_year': str(datetime.now().year)
    }
    
    try:
        ExtractReportAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'topic': topic,
    }
    try:
        ExtractReportAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ExtractReportAgent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'topic': topic,
    }
    try:
        ExtractReportAgent().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

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
