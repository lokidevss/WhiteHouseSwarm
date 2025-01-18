# WhiteHouseSwarm
## AI Agent Swarm Simulation

This project simulates an AI agent swarm where agents collaborate to perform tasks, communicate, and make decisions using **real AI** techniques like reinforcement learning (RL) and natural language processing (NLP).

## Features

- **Multi-Agent System**: Agents with specific roles (e.g., Monitoring, Decision-Making) work together.
- **Task Management**: Tasks are dynamically generated and assigned based on priority and agent roles.
- **Reinforcement Learning (RL)**: Agents use RL to prioritize and assign tasks.
- **Natural Language Processing (NLP)**: Agents communicate using an NLP model (GPT-2) for human-like interaction.
- **Real-Time Simulation**: The simulation runs continuously, generating tasks and simulating agent behavior.

## Requirements

- Python 3.8+
- Libraries: `gym`, `transformers`, `torch`

Install dependencies:

```bash
pip install gym transformers torch
```

## How to Run
Clone the repository:

```bash
git clone https://github.com/yourusername/ai-agent-swarm.git
cd ai-agent-swarm
```

Run the simulation:

```bash
python main.py
```

Press Ctrl+C to stop the simulation.

## Code Overview
- **AIAgent**: Represents an individual agent with a role, tasks, and communication capabilities.
- **AIAgentSwarm**: Manages the swarm of agents, task assignment, and communication.
- **Task**: Represents a task with a description, priority, and required role.
- **RL and NLP Integration**: Uses gym for RL and transformers for NLP-based communication.

## Example Output
```bash
2023-10-30 12:00:00,000 - INFO - Agent 1 (Monitoring) joined the swarm.
2023-10-30 12:00:00,001 - INFO - Agent 2 (Decision-Making) joined the swarm.
2023-10-30 12:00:00,002 - INFO - Agent 3 (Reporting) joined the swarm.
2023-10-30 12:00:00,003 - INFO - Agent 4 (Security) joined the swarm.
2023-10-30 12:00:00,004 - INFO - Agent 5 (Data Analysis) joined the swarm.
2023-10-30 12:00:00,005 - INFO - Added task to queue: Task 1: Monitor network traffic (Priority: HIGH, Role: Monitoring)
2023-10-30 12:00:00,006 - INFO - Agent 1 (Monitoring) started task: Monitor network traffic
2023-10-30 12:00:00,007 - INFO - Agent 1 completed task: Monitor network traffic
2023-10-30 12:00:02,008 - INFO - Agent 1 sending message to Agent 2: Agent 1 says: We need to analyze the latest data trends.
2023-10-30 12:00:02,009 - INFO - Agent 2 received message from Agent 1: Agent 1 says: We need to analyze the latest data trends.
```

## License
This project is licensed under the MIT License. See LICENSE for details.
