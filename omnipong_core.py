import logging
import json
import time
from utils.communication import Communication

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message=s')

class OmnipongCore:
    def __init__(self):
        self.agents = {}
        self.task_queue = []
        self.knowledge_base = {}
        self.communication = Communication()
        logging.info("Omnipong Core initialized")

    def register_agent(self, agent):
        try:
            self.agents[agent.agent_id] = agent
            agent.core = self  # Set reference back to core
            logging.info(f"Agent '{agent.agent_id}' registered")
        except Exception as e:
            logging.error(f"Error registering agent '{agent.agent_id}': {e}")

    def send_task(self, task):
        try:
            self.task_queue.append(task)
            logging.info(f"Task added to queue: {task}")
        except Exception as e:
            logging.error(f"Error adding task to queue: {e}")

    def distribute_tasks(self):
        try:
            while self.task_queue:
                task = self.task_queue.pop(0)
                agent = self.select_agent(task)
                if agent:
                    agent.receive_task(task)
                    logging.info(f"Task '{task}' assigned to agent '{agent.agent_id}'")
                else:
                    logging.warning(f"No suitable agent found for task: {task}")
        except Exception as e:
            logging.error(f"Error distributing tasks: {e}")

    def select_agent(self, task):
        try:
            for agent in self.agents.values():
                if agent.can_handle(task):
                    return agent
            return None
        except Exception as e:
            logging.error(f"Error selecting agent for task '{task}': {e}")
            return None

    def receive_report(self, agent_id, report):
        try:
            logging.info(f"Core received report from '{agent_id}': {report}")
            self.knowledge_base.update(report)
        except Exception as e:
            logging.error(f"Error receiving report from '{agent_id}': {e}")

    def save_knowledge_base(self, filepath):
        try:
            with open(filepath, 'w') as file:
                json.dump(self.knowledge_base, file)
            logging.info(f"Knowledge base saved to {filepath}")
        except Exception as e:
            logging.error(f"Error saving knowledge base: {e}")

    def load_knowledge_base(self, filepath):
        try:
            with open(filepath, 'r') as file:
                self.knowledge_base = json.load(file)
            logging.info(f"Knowledge base loaded from {filepath}")
        except Exception as e:
            logging.error(f"Error loading knowledge base: {e}")

    def automate_task_distribution(self, interval=5):
        import threading
        def distribute():
            while True:
                self.distribute_tasks()
                time.sleep(interval)
        threading.Thread(target=distribute, daemon=True).start()

# Example usage
if __name__ == '__main__':
    core = OmnipongCore()
    core.save_knowledge_base('data/knowledge_base.json')
    core.load_knowledge_base('data/knowledge_base.json')
    core.automate_task_distribution()
