from learning_agent_base import LearningAgentBase
import logging
import requests
from bs4 import BeautifulSoup
import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname=s - %(message=s')

class CuriosityEngine(LearningAgentBase):
    def __init__(self, agent_id):
        state_size = 100  # Define based on actual states
        action_size = 10  # Define based on actual actions
        super().__init__(agent_id, state_size, action_size)
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        self.vectorizer = TfidfVectorizer(stop_words='english')
        logging.info(f"CuriosityEngine {self.agent_id} initialized")

    def can_handle(self, task):
        return task.get('type') == 'explore'

    def receive_task(self, task):
        topic = task.get('topic')
        try:
            state = self.get_state(topic)
            action = self.act(state)
            findings = self.explore(topic, action)
            reward = self.evaluate_findings(findings)
            next_state = self.get_state(topic)
            self.remember(state, action, reward, next_state, done=False)
            self.report({'agent': self.agent_id, 'topic': topic, 'findings': findings})
            self.replay(batch_size=32)  # Adjust batch size as needed
        except Exception as e:
            logging.error(f"Error exploring topic by {self.agent_id}: {e}")
            self.report({'agent': self.agent_id, 'error': str(e)})

    def explore(self, topic, action):
        logging.info(f"{self.agent_id} is exploring the topic: {topic} with action: {action}")
        search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        snippets = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        content = " ".join([snippet.text for snippet in snippets[:10]])  # More snippets for comprehensive analysis
        logging.info(f"{self.agent_id} fetched content: {content}")

        summary = self.summarizer(content, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        logging.info(f"{self.agent_id} generated summary: {summary}")

        doc = self.nlp(content)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        logging.info(f"{self.agent_id} identified entities: {entities}")

        tfidf_matrix = self.vectorizer.fit_transform([snippet.text for snippet in snippets])
        num_clusters = 5
        km = KMeans(n_clusters=num_clusters)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()
        logging.info(f"{self.agent_id} performed clustering: {clusters}")

        return {'summary': summary, 'entities': entities, 'clusters': clusters}

    def get_state(self, topic):
        return hash(topic) % self.state_size

    def evaluate_findings(self, findings):
        return len(findings['entities']) + len(set(findings['clusters']))  # Reward based on entities and unique clusters

# Example usage
if __name__ == '__main__':
    task_example = {'type': 'explore', 'topic': 'artificial intelligence'}
    curiosity_engine = CuriosityEngine("CuriosityEngine_1")
    curiosity_engine.receive_task(task_example)
