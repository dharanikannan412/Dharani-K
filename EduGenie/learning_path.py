from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
Create a structured learning path for a learner who wants to study:

{topic}

Organize it from beginner to advanced. Include:
- prerequisite knowledge
- stages or topics in a sensible order
- a suggested timeline
- what the learner should be able to do after each stage
- practical exercises or mini-projects
- suggested resource types (videos, articles, books, documentation)
- a final revision/project stage

Do not invent specific URLs. Keep the plan adaptable to the learner's level.
"""
    return generate_text(prompt, temperature=0.4)
