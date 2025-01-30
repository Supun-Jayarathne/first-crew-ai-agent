import os
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import litellm  # Ensure LiteLLM is installed and imported

# Enable verbose debugging for LiteLLM
litellm.set_verbose = True

@CrewBase
class ExtractReportAgent:
    """ExtractReportAgent crew"""

    # File paths to YAML configurations
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Environment variable setup
    os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY", "")

    # Tools initialization
    search_tool = SerperDevTool()

    @agent
    def extract_agent(self) -> Agent:
        """Create and return the extract agent."""
        return Agent(
            config=self.agents_config['extract_agent'],  # Access the dictionary
            verbose=True
        )

    @agent
    def news_agent(self) -> Agent:
        """Create and return the news agent."""
        return Agent(
            config=self.agents_config['news_agent'],  # Access the dictionary
            verbose=True,
        )

    @agent
    def blog_writer(self) -> Agent:
        """Create and return the blog writer agent."""
        return Agent(
            config=self.agents_config['blog_writer'],  # Access the dictionary
            verbose=True,
        )

    @task
    def extract_task(self) -> Task:
        """Create and return the extract task."""
        return Task(
            config=self.tasks_config['extract_task'],  # Access the dictionary
        )

    @task
    def news_finder_task(self) -> Task:
        """Create and return the news finder task."""
        return Task(
            config=self.tasks_config['news_finder_task'],  # Access the dictionary
            output_file='news.md',
            tools=[self.search_tool]
        )

    @task
    def blog_writer_task(self) -> Task:
        """Create and return the blog writer task."""
        return Task(
            config=self.tasks_config['blog_writer_task'],  # Access the dictionary
            output_file='blog.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ExtractReportAgent crew."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
