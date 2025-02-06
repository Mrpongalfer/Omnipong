import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgentBase:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.core = None  # Will be set when registered with the core
        self.state = {}
        logging.info(f"AgentBase {self.agent_id} initialized")

    def can_handle(self, task):
        return False

    def receive_task(self, task):
        pass

    def report(self, data):
        if self.core:
            self.core.receive_report(self.agent_id, data)
        else:
            logging.warning(f"{self.agent_id} has no core reference")

    def update_state(self, key, value):
        self.state[key] = value
        logging.info(f"{self.agent_id} state updated: {key} = {value}")

    def get_state(self, key):
        return self.state.get(key, None)

    def save_state(self, filepath):
        try:
            with open(filepath, 'w') as file:
                json.dump(self.state, file)
            logging.info(f"{self.agent_id} state saved to {filepath}")
        except Exception as e:
            logging.error(f"Error saving state for {self.agent_id}: {e}")

    def load_state(self, filepath):
        try:
            with open(filepath, 'r') as file:
                self.state = json.load(file)
            logging.info(f"{self.agent_id} state loaded from {filepath}")
        except Exception as e:
            logging.error(f"Error loading state for {self.agent_id}: {e}")

# Example usage
if __name__ == '__main__':
    agent = AgentBase('AgentBase_1')
    agent.update_state('health', 100)
    agent.save_state('agent_state.json')
    agent.load_state('agent_state.json')
    print(f"Agent state: {agent.get_state('health')}")
