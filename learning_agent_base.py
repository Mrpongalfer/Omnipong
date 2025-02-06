from agent_base import AgentBase
import numpy as np
import random
import json
import logging
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')

class LearningAgentBase(AgentBase):
    def __init__(self, agent_id, state_size, action_size):
        super().__init__(agent_id)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        logging.info(f"LearningAgentBase {self.agent_id} initialized with state size {self.state_size} and action size {self.action_size}")

    def _build_model(self):
        # Neural Network for Deep Q-Learning
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        logging.info("Neural network model built for Q-learning")
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        logging.info(f"Memory updated with state: {state}, action: {action}, reward: {reward}, next_state: {next_state}, done: {done}")

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            action = random.randrange(self.action_size)
            logging.info(f"Random action chosen due to exploration: {action}")
            return action
        act_values = self.model.predict(state)
        action = np.argmax(act_values[0])
        logging.info(f"Action chosen based on model prediction: {action}")
        return action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
            logging.info(f"Replay memory updated and model trained for state: {state}")
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            logging.info(f"Epsilon updated: {self.epsilon}")

    def load(self, name):
        self.model.load_weights(name)
        logging.info(f"Model weights loaded from {name}")

    def save(self, name):
        self.model.save_weights(name)
        logging.info(f"Model weights saved to {name}")

# Example usage
if __name__ == '__main__':
    state_size = 4  # Example state size
    action_size = 2  # Example action size
    agent = LearningAgentBase('LearningAgent_1', state_size, action_size)
    state = np.reshape([1, 0, 0, 0], [1, state_size])
    action = agent.act(state)
    next_state = np.reshape([0, 1, 0, 0], [1, state_size])
    agent.remember(state, action, 1, next_state, False)
    agent.replay(1)
    agent.save("model_weights.h5")
    agent.load("model_weights.h5")
