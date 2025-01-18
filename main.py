import logging
import time
import random
import gym
import torch
from transformers import pipeline
from enum import Enum, auto
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class TaskPriority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class AgentRole(Enum):
    MONITORING = "Monitoring"
    DECISION_MAKING = "Decision-Making"
    REPORTING = "Reporting"
    SECURITY = "Security"
    DATA_ANALYSIS = "Data Analysis"

class Task:
    def __init__(self, task_id: int, description: str, priority: TaskPriority, required_role: AgentRole):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.required_role = required_role

    def __str__(self):
        return f"Task {self.task_id}: {self.description} (Priority: {self.priority.name}, Role: {self.required_role.value})"

class AIAgent:
    def __init__(self, agent_id: int, role: AgentRole):
        self.agent_id = agent_id
        self.role = role
        self.swarm = None
        self.current_task = None
        self.task_history = []
        self.nlp = pipeline("text-generation", model="gpt-2")

    def join_swarm(self, swarm):
        self.swarm = swarm
        swarm.add_agent(self)
        logging.info(f"Agent {self.agent_id} ({self.role.value}) joined the swarm.")

    def perform_task(self, task: Task):
        if self.current_task:
            logging.warning(f"Agent {self.agent_id} is already busy with task {self.current_task.task_id}.")
            return

        self.current_task = task
        self.task_history.append(task)
        logging.info(f"Agent {self.agent_id} ({self.role.value}) started task: {task.description}")
        self.complete_task()

    def complete_task(self):
        if self.current_task:
            logging.info(f"Agent {self.agent_id} completed task: {self.current_task.description}")
            self.current_task = None
        else:
            logging.warning(f"Agent {self.agent_id} has no active task to complete.")

    def communicate(self, message: str, recipient_id: Optional[int] = None):
        if recipient_id:
            logging.info(f"Agent {self.agent_id} sending message to Agent {recipient_id}: {message}")
            if self.swarm:
                self.swarm.deliver_message(message, self.agent_id, recipient_id)
        else:
            logging.info(f"Agent {self.agent_id} broadcasting message: {message}")
            if self.swarm:
                self.swarm.broadcast_message(message, self.agent_id)

    def generate_message(self, context: str) -> str:
        response = self.nlp(context, max_length=50, num_return_sequences=1)
        return response[0]["generated_text"]

    def receive_message(self, message: str, sender_id: int):
        logging.info(f"Agent {self.agent_id} received message from Agent {sender_id}: {message}")

    def report_status(self):
        status = f"Agent {self.agent_id} ({self.role.value}) is {'busy' if self.current_task else 'idle'}."
        if self.current_task:
            status += f" Current task: {self.current_task.description}"
        logging.info(status)

class AIAgentSwarm:
    def __init__(self):
        self.agents = {}
        self.task_queue = []
        self.task_counter = 0
        self.env = gym.make("Taxi-v3")

    def add_agent(self, agent: AIAgent):
        self.agents[agent.agent_id] = agent

    def add_task(self, task: Task):
        self.task_queue.append(task)
        logging.info(f"Added task to queue: {task}")
        self.assign_tasks()

    def assign_tasks(self):
        state = self.env.reset()
        for task in sorted(self.task_queue, key=lambda x: x.priority.value, reverse=True):
            for agent in self.agents.values():
                if agent.role == task.required_role and not agent.current_task:
                    action = self.env.action_space.sample()
                    agent.perform_task(task)
                    self.task_queue.remove(task)
                    break

    def broadcast_message(self, message: str, sender_id: int):
        for agent_id, agent in self.agents.items():
            if agent_id != sender_id:
                agent.receive_message(message, sender_id)

    def deliver_message(self, message: str, sender_id: int, recipient_id: int):
        if recipient_id in self.agents:
            self.agents[recipient_id].receive_message(message, sender_id)
        else:
            logging.error(f"Recipient Agent {recipient_id} not found.")

    def generate_swarm_report(self):
        logging.info("Generating swarm status report:")
        for agent in self.agents.values():
            agent.report_status()

    def generate_random_task(self):
        self.task_counter += 1
        task_types = [
            ("Monitor network traffic", TaskPriority.HIGH, AgentRole.MONITORING),
            ("Analyze threat level", TaskPriority.MEDIUM, AgentRole.DATA_ANALYSIS),
            ("Prepare daily report", TaskPriority.LOW, AgentRole.REPORTING),
            ("Secure communication channels", TaskPriority.HIGH, AgentRole.SECURITY),
        ]
        description, priority, role = random.choice(task_types)
        return Task(self.task_counter, description, priority, role)

if __name__ == "__main__":
    whitehouse_swarm = AIAgentSwarm()

    monitoring_agent = AIAgent(agent_id=1, role=AgentRole.MONITORING)
    decision_agent = AIAgent(agent_id=2, role=AgentRole.DECISION_MAKING)
    reporting_agent = AIAgent(agent_id=3, role=AgentRole.REPORTING)
    security_agent = AIAgent(agent_id=4, role=AgentRole.SECURITY)
    data_agent = AIAgent(agent_id=5, role=AgentRole.DATA_ANALYSIS)

    monitoring_agent.join_swarm(whitehouse_swarm)
    decision_agent.join_swarm(whitehouse_swarm)
    reporting_agent.join_swarm(whitehouse_swarm)
    security_agent.join_swarm(whitehouse_swarm)
    data_agent.join_swarm(whitehouse_swarm)

    try:
        while True:
            task = whitehouse_swarm.generate_random_task()
            whitehouse_swarm.add_task(task)

            if random.random() < 0.3:
                sender = random.choice(list(whitehouse_swarm.agents.values()))
                recipient = random.choice(list(whitehouse_swarm.agents.values()))
                if sender.agent_id != recipient.agent_id:
                    context = f"Agent {sender.agent_id} says:"
                    message = sender.generate_message(context)
                    sender.communicate(message, recipient.agent_id)

            if whitehouse_swarm.task_counter % 5 == 0:
                whitehouse_swarm.generate_swarm_report()

            time.sleep(2)

    except KeyboardInterrupt:
        logging.info("Simulation stopped by user.")
