from omnipong.agents.curiosity_engine import CuriosityEngine
from omnipong.agents.problem_solver import ProblemSolver
from omnipong.agents.mr_meeseeks import MrMeeseeks
from omnipong.agents.fog_node_agent import FogNodeAgent
from omnipong.agents.edge_node_agent import EdgeNodeAgent
import logging

# Rest of the code remains unchanged


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_agent(agent_type, agent_id, task=None):
    try:
        if agent_type == 'CuriosityEngine':
            agent = CuriosityEngine(agent_id)
        elif agent_type == 'ProblemSolver':
            agent = ProblemSolver(agent_id)
        elif agent_type == 'MrMeeseeks':
            agent = MrMeeseeks(agent_id, task)
        elif agent_type == 'FogNodeAgent':
            agent = FogNodeAgent(agent_id)
        elif agent_type == 'EdgeNodeAgent':
            agent = EdgeNodeAgent(agent_id)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

        logging.info(f"Created agent: {agent_type} with ID: {agent_id}")
        return agent
    except Exception as e:
        logging.error(f"Error creating agent: {e}")
        raise

# Example usage
if __name__ == '__main__':
    agent = create_agent('CuriosityEngine', 'CuriosityEngine_1')
    print(f"Created agent: {agent.agent_id}")
