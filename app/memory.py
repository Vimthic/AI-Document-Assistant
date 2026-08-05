from typing import List, Dict

class ConversationMemory:
    def __init__(self, max_history_turns: int = 4):
        """Initializes conversation tracker restricted to a specific lookback window."""
        self.max_history_turns = max_history_turns

    def get_formatted_history(self, messages: List[Dict[str, str]]) -> str:
        """
        Filters recent message pairs from Streamlit log logs.
        Converts array schemas into clean prompt injection strings.
        """
        # Filter down to user and assistant statements exclusively
        chat_turns = [m for m in messages if m["role"] in ["user", "assistant"]]
        
        # Slice only the most recent entries based on lookback limits (2 entries per turn)
        recent_turns = chat_turns[-(self.max_history_turns * 2):] if chat_turns else []
        
        if not recent_turns:
            return "No previous conversation history."
            
        formatted_lines = []
        for msg in recent_turns:
            speaker = "User" if msg["role"] == "user" else "Assistant"
            formatted_lines.append(f"{speaker}: {msg['content']}")
            
        return "\n".join(formatted_lines)
