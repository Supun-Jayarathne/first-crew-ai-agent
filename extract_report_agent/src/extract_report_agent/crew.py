from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
@CrewBase
class ExtractReportAgent():
	"""ExtractReportAgent crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def extract_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['extract_agent'],
			verbose=True
		)

	@agent
	def news_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_agent'],
			verbose=True
		)
	
	@agent
	def blog_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['blog_writer'],
			verbose=True,
			allow_delegation=True
		)

	@task
	def extract_task(self) -> Task:
		return Task(
			config=self.tasks_config['extract_task'],
		)

	@task
	def news_finder_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_finder_task'],
			output_file='news.md'
		)
	
	@task
	def blog_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['blog_writer_task'],
			output_file='blog.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ExtractReportAgent crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical,
		)
