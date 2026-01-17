"""
Online Feature Store (State Management)
=======================================

Purpose:
    - Maintain the "Current State" of every active delivery.
    - Serve low-latency features to the Inference Engine.
    - In-Memory Implementation (Dictionary-based).

Architecture Note:
    - In PRODUCTION, this is replaced by Redis, DynamoDB, or Feast.
    - Key pattern: event -> update state -> get features -> predict.

Author: Real-Time Systems Team
Stage: STAGE 4 - Real-Time System
"""

class OnlineFeatureStore:
    def __init__(self):
        # In-memory Key-Value store: { task_id : feature_dict }
        self._store = {}
        
    def update_state(self, event):
        """
        Process an incoming event and update the feature vector for that task.
        """
        data = event.get('data', {})
        task_id = data.get('task_id')
        
        if not task_id:
            return None
            
        # In a real system, we would calculate features here (e.g., aggregations).
        # For this demo, we assume the 'features' dict is pre-calculated by the upstream pipeline.
        features = data.get('features', {})
        
        # Upsert state
        if task_id not in self._store:
            self._store[task_id] = {}
            
        self._store[task_id].update(features)
        
        # Return the full feature vector ready for inference
        return self._store[task_id]

    def get_features(self, task_id):
        """
        Retrieve features for a specific task. Low latency read.
        """
        return self._store.get(task_id)

    def delete_state(self, task_id):
        """
        Cleanup once delivery is finalized to save memory (Redis TTL).
        """
        if task_id in self._store:
            del self._store[task_id]

# Unit Test
if __name__ == "__main__":
    ofs = OnlineFeatureStore()
    mock_event = {
        "data": {
            "task_id": "T123",
            "features": {"distance_km": 5.5, "is_weekend": 1}
        }
    }
    vector = ofs.update_state(mock_event)
    print(f"State stored for T123: {vector}")
