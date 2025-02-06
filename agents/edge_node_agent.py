from learning_agent_base import LearningAgentBase
import logging
import random
import json
import numpy as np
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime=s - %(levelname=s - %(message=s')

class EdgeNodeAgent(LearningAgentBase):
    def __init__(self, agent_id):
        state_size = 100  # Define based on actual states
        action_size = 10  # Define based on actual actions
        super().__init__(agent_id, state_size, action_size)
        self.scaler = StandardScaler()
        logging.info(f"EdgeNodeAgent {self.agent_id} initialized")

    def can_handle(self, task):
        return task.get('type') in ['collect_data', 'preprocess_data']

    def receive_task(self, task):
        task_type = task.get('type')
        try:
            if task_type == 'collect_data':
                data = self.collect_data(task)
            elif task_type == 'preprocess_data':
                data = self.preprocess_data(task)
            self.report({'agent': self.agent_id, 'result': data})
        except Exception as e:
            logging.error(f"Error handling task by {self.agent_id}: {e}")
            self.report({'agent': self.agent_id, 'error': str(e)})

    def collect_data(self, task):
        sensor_id = task.get('sensor_id', 'default_sensor')
        logging.info(f"{self.agent_id} is collecting data from sensor: {sensor_id}")
        data = {'sensor_id': sensor_id, 'timestamp': time.time(), 'value': random.uniform(0, 100)}
        logging.info(f"Collected data: {data}")
        return json.dumps(data)

    def preprocess_data(self, task):
        raw_data = task.get('data')
        logging.info(f"{self.agent_id} is preprocessing data: {raw_data}")
        data = json.loads(raw_data)
        values = np.array([data['value']]).reshape(-1, 1)
        scaled_values = self.scaler.fit_transform(values)
        processed_data = {'original_data': data, 'processed_data': scaled_values.tolist()}
        logging.info(f"Preprocessed data: {processed_data}")
        return json.dumps(processed_data)

# Example usage
if __name__ == '__main__':
    task_collect = {'type': 'collect_data', 'sensor_id': 'sensor_42'}
    task_preprocess = {'type': 'preprocess_data', 'data': '{"sensor_id": "sensor_42", "timestamp": 1234567890, "value": 42}'}
    edge_node_agent = EdgeNodeAgent("EdgeNodeAgent_1")
    edge_node_agent.receive_task(task_collect)
    edge_node_agent.receive_task(task_preprocess)
