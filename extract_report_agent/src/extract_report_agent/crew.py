from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ExtractReportAgent():
	"""ExtractReportAgent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

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

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
