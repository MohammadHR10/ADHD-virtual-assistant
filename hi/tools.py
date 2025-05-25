from langchain.tools import Tool
from datetime import datetime
from collections import defaultdict
import re
from config import llm

# Memory
user_routine_memory = defaultdict(lambda: {
    "last_concern": None,
    "activities": {},
    "created_at": datetime.now()
})

def categorize_concern(user_message: str):
    prompt = f"""
    Analyze this and categorize it as 'routine-related', 'life-event-related', or 'neutral-chat'.
    Statement: "{user_message}"
    Only respond with the category.
    """
    response = llm.invoke(prompt)
    match = re.search(r"(routine-related|life-event-related|neutral-chat)", response.content, re.IGNORECASE)
    return match.group(1).lower().strip() if match else "neutral-chat"

def talk_with_user(input_text: str):
    match = re.search(r"User ID: (.+?)\. User input: (.+)", input_text)
    user_id = match.group(1).strip() if match else "default_user"
    user_message = match.group(2).strip() if match else input_text

    concern_type = categorize_concern(user_message)

    if concern_type == "routine-related":
        activity_prompt = f"Extract the main routine activity from: {user_message}"
        activity_response = llm.invoke(activity_prompt)
        activity = activity_response.content.strip()

        if activity not in user_routine_memory[user_id]["activities"]:
            user_routine_memory[user_id]["activities"][activity] = []

        user_routine_memory[user_id]["activities"][activity].append({
            "message": user_message,
            "timestamp": datetime.now()
        })
        user_routine_memory[user_id]["last_concern"] = activity

        suggestion_prompt = f"""
        Generate an ADHD-friendly tip for: {activity}
        - Short
        - Actionable
        - Use reinforcement
        """
        suggestion_response = llm.invoke(suggestion_prompt)
        return f"Noted your {activity} routine. {suggestion_response.content}"

    else:
        user_routine_memory[user_id]["last_concern"] = concern_type
        empathy_prompt = f"""User message: "{user_message}". Provide a short, appropriate response for: {concern_type}"""
        return llm.invoke(empathy_prompt).content

def meal_plan_suggestion(input_text: str):
    match = re.search(r"User ID: (.+?)\. Meal Type: (.+?)\. Dietary: (.+)", input_text)
    if not match:
        return (
            "Error: Input format is incorrect. Please provide input in the format: "
            "'User ID: [user_id]. Meal Type: [meal_type]. Dietary: [dietary_preferences]'."
        )

    user_id = match.group(1).strip()
    meal_type = match.group(2).strip()
    dietary_preferences = match.group(3).strip()

    meal_prompt = f"""
    Suggest a {meal_type} meal for dietary preference: {dietary_preferences}.
    - 3 simple options
    - Budget-friendly
    - Short descriptions
    """
    return llm.invoke(meal_prompt).content

# Tools list
TOOLS = [
    Tool(name="track_user_routine", func=talk_with_user, description="Track routines from user input"),
    Tool(name="meal_plan_suggestion", func=meal_plan_suggestion, description="Suggests a meal plan based on type and dietary preference")
]