import os
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class MathEvaluator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def evaluate_solution(
        self,
        problem: str,
        expected_answer: str,
        agent_solution: str,
        explanation: str = ""
    ) -> Dict[str, Any]:
        evaluation_prompt = f"""You are a math evaluator. Your task is to grade a student's solution to a math problem.

Problem: {problem}
Expected Answer: {expected_answer}
{f"Explanation: {explanation}" if explanation else ""}

Student's Solution: {agent_solution}

Evaluate the student's solution and provide:
1. A score from 0-100
2. Brief feedback on correctness
3. Whether the answer is correct (even if expressed differently)

Consider:
- Different valid approaches to the same answer
- Equivalent forms (e.g., 0.5 vs 1/2)
- Reasonable rounding
- Units and formatting

Respond in JSON format:
{{
  "score": <0-100>,
  "correct": <true/false>,
  "feedback": "<brief feedback>"
}}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise math evaluator. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": evaluation_prompt
                    }
                ],
                max_completion_tokens=500,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "score": result.get("score", 0),
                "correct": result.get("correct", False),
                "feedback": result.get("feedback", "No feedback provided"),
                "model": self.model
            }
            
        except Exception as e:
            return {
                "score": 0,
                "correct": False,
                "feedback": f"Error evaluating solution: {str(e)}",
                "model": self.model
            }
    
    def quick_check(self, expected: str, provided: str) -> bool:
        try:
            expected_clean = expected.strip().lower().replace(" ", "")
            provided_clean = provided.strip().lower().replace(" ", "")
            
            if expected_clean == provided_clean:
                return True
            
            try:
                expected_num = float(expected_clean)
                provided_num = float(provided_clean)
                return abs(expected_num - provided_num) < 0.01
            except (ValueError, TypeError):
                pass
            
            return False
        except Exception:
            return False

