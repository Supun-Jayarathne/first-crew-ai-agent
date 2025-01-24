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
# topic = """TECHNICAL EXPERIENCE BISTEC Global  
# Software Engineer  TAFI Project  
# ▪ Collaborating with other programmers to design and implement 
# features.  
# ▪ Producing well -organized and optimized source code.  
# Tools  & Technologies:  ReactJS,  NextJS,  ASP.NET technologies, MS SQL 
# Server, Ant UI, HTML5, CSS, NX Console, Azure DevOps, VS Code , Visual 
# Studio  
# BISTEC Global  
# Software Engineer  Design Grid  
# ▪ Plan and organize the project, set deadlines and milestones, and 
# manage the resources and tasks.  BUSINESS CV  
# Commercial in confidence  
#  BISTEC Global Services (Pvt)  Ltd. 
# No: 14, Sir Baron Jayathilake Mawatha, Colombo 0 0100 
# BISTEC Global Pty Ltd.  Level 2/11 York Street, Sydney, NSW 2000  
#  Tel : (+61) 02 9052 4700 / (+9 4) 07 7768 1014  
# Email  : info@bistecglobal.com  
# Web  : www.bistecglobal.com  
# ▪ Collaborating with other programmers to design and implement 
# features.  
# ▪ Producing well -organized and optimized source code.  
# Tools  & Technologies:  Angular,  ASP.NET technologies, MS SQL Server, 
# Angular Material UI, HTML5, CSS, NX Console, Azure Repository and 
# pipeline, AWS RDS database, AWS S3, AWS Beanstalk , AWS Simple mail 
# service, VS Cod e, Visual Studio  
# BISTEC Global  
# Software Engineer  BDO Chatbot  
# ▪ Collaborating with other programmers to design and implement 
# features.  
# ▪ Producing well -organized and optimized source code.  
# Tools  & Technologies:  Bot Framework, Azure DevOps, Visual Studio  
# BISTEC Global  
# Software Engineer  
#  CSR Project  
# ▪ Working with  other developers to design and implement features.  
# ▪ Producing well -organized and optimized source code.  
# Tools & Technologies:  Sitecore XM Cloud, Next Js, Docker,  
# Visual Studio Code"""
# topic =  'ReactJS, NextJS, ASP.NET technologies, MS SQL Server, Ant UI, HTML5, CSS, NX Console, Azure DevOps, VS Code, Visual Studio'


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
    # Pass the CV content to the agent
    # senior_cv_analyst.goal = f"Understand CVs and extract project names and their related technologies from the following content: {cv_content}"
    # return cv_content 
    global topic
    topic = cv_content
    run()

iface = gr.Interface(
    fn=run_crewai_app,
    inputs=[gr.File(file_types=[".pdf"])],
    outputs="text",
    title="CrewAI CV Extractor",
    description="Upload a CV to extract project details from the CV."
)

iface.launch(share=True)
