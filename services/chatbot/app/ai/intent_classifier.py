"""
Intent Classification Engine
Classifies user intent from messages
"""

import os

class IntentClassifier:
    """Classifies user intent."""
    
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.initialized = False
        self.intents = {}
        
    def initialize(self):
        """Initialize intent classifier with Ollama."""
        try:
            # Load intents from metadata or Ollama
            self.initialized = True
            print(f"✓ Intent Classifier initialized ({self.ollama_host})")
        except Exception as e:
            print(f"✗ Intent Classifier init failed: {e}")
    
    def classify(self, message: str) -> str:
        """Classify message intent."""
        if not self.initialized:
            return "unknown"
        
        # Classification logic will go here
        return "general"
    
    def get_intents(self) -> dict:
        """Get available intents."""
        return self.intents


def init_intent_classifier() -> IntentClassifier:
    """Initialize intent classifier."""
    classifier = IntentClassifier()
    classifier.initialize()
    return classifier
