from agent_base import AgentBase
import logging
import time
import random
import json
from transformers import pipeline
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')

class MrMeeseeks(AgentBase):
    def __init__(self, agent_id, task):
        super().__init__(agent_id)
        self.task = task
        self.start_time = time.time()
        self.classifier = pipeline("zero-shot-classification")
        logging.info(f"Initialized Mr. Meeseeks agent: {self.agent_id} with task: {self.task}")

    def can_handle(self, task):
        return False

    def perform_task(self):
        try:
            logging.info(f"{self.agent_id} says: I'm Mr. Meeseeks, look at me!")
            result = self.execute_task(self.task)
            self.report({'agent': self.agent_id, 'result': result})
        except Exception as e:
            logging.error(f"Error performing task by {self.agent_id}: {e}")
            self.report({'agent': self.agent_id, 'error': str(e)})
        finally:
            self.self_destruct()

    def execute_task(self, task):
        task_type = task.get('type')
        logging.info(f"{self.agent_id} is executing task: {task_type}")

        if task_type == 'collect_data':
            return self.collect_data(task)
        elif task_type == 'preprocess_data':
            return self.preprocess_data(task)
        elif task_type == 'solve_problem':
            return self.solve_problem(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    def collect_data(self, task):
        sensor_id = task.get('sensor_id', 'default_sensor')
        logging.info(f"{self.agent_id} is collecting data from sensor: {sensor_id}")
        data = {'sensor_id': sensor_id, 'timestamp': datetime.utcnow().isoformat(), 'value': random.uniform(0, 100)}
        return json.dumps(data)

    def preprocess_data(self, task):
        data = task.get('data')
        logging.info(f"{self.agent_id} is preprocessing data: {data}")
        processed_data = {'original_data': data, 'processed_data': f"Processed {data}"}
        return json.dumps(processed_data)

    def solve_problem(self, task):
        problem_description = task.get('description', 'default_problem')
        logging.info(f"{self.agent_id} is solving problem: {problem_description}")
        solution = self.classifier(problem_description, candidate_labels=["solution1", "solution2", "solution3"])
        return json.dumps(solution)

    def self_destruct(self):
        logging.info(f"{self.agent_id} has completed its task and will now self-destruct.")
        time.sleep(1)
        if self.core:
            del self.core.agents[self.agent_id]
            logging.info(f"{self.agent_id} removed from core's agent list.")

# Example usage
if __name__ == '__main__':
    task_example = {'type': 'collect_data', 'sensor_id': 'sensor_42'}
    meeseeks = MrMeeseeks("Meeseeks_1", task_example)
    meeseeks.perform_task()
