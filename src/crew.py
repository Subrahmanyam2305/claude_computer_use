from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import tools
from tools.computer import ComputerTool
from langchain_community.chat_models import BedrockChat

llm = BedrockChat(
		credentials_profile_name="dsexp", model_id="anthropic.claude-3-5-sonnet-20241022-v2:0", region_name="us-west-2"
		)

@CrewBase
class ClaudecomputeruseCrew():
	"""claude_computer_use crew"""

	# Agent definitions
	@agent
	def feedback_giver_agent(self) -> Agent:
	    return Agent(
	        config=self.agents_config['qa_agent'],
	        tools=[],  # add tools here or use `agentstack tools add <tool_name>
	        verbose=True
	    )
	
	@agent
	def computer_agent(self) -> Agent:
	    return Agent(
	        config=self.agents_config['computer_agent'],
			# llm=llm,
	        tools=[ComputerTool()],  # add tools here or use `agentstack tools add <tool_name>
	        verbose=True
	    )
	
	@agent
	def qa_agent(self) -> Agent:
	    return Agent(
	        config=self.agents_config['qa_agent'],
	        tools=[],  # add tools here or use `agentstack tools add <tool_name>
	        verbose=True
	    )
	

	# Task definitions
	@task
	def output_inspect(self) -> Task:
	    return Task(
	        config=self.tasks_config['output_inspect'],
	    )
	
	@task
	def organize_chrome_tabs(self) -> Task:
	    return Task(
	        config=self.tasks_config['organize_chrome_tabs'],
	    )
	
	@task
	def create_obsidian_chart(self) -> Task:
	    return Task(
	        config=self.tasks_config['create_obsidian_chart'],
	    )
	

	@crew
	def crew(self) -> Crew:
		"""Creates the Test crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)