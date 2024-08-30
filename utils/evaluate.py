from langchain_openai import ChatOpenAI
import requests
from typing import List
import json

# Define the evaluation questions
evaluation_questions = [
    "Which Teams have gone from worst to first in their division in the past 20 seasons? What are the characteristics that make these teams unique?",
    "Can you give me the average stregnth of schedule for the past 10 super bowl winners?",
    "How have teams who have offensive lines ranked in the top 10 performed aganst the spread?",
    "Could you name me the teams who's o-lines are projected to finish in the top 10 in 2023?",
    "What was the TD drive rate of the Baltimore Ravens during the 2023 NFL Season?",
    "How did Lamar Jackson perform wihen the opposing teams defense loaded the box last season?",
    "How did the Baltimore Ravens Defense perform against the run last season?",
    "What was Lamar Jacksons Yards Per Cary on Scrambles last year?",
    "How do the Ravens offensive and defensive lines rank in the leadup to the 2024 NFL season",
    "What is the offensive line and defensive line rank for the Cincinati Bengals this season?",
    "What is Joe Burrows record against the spread?",
    "Who are the quarterbacks that the Cincinatti Bengals are going to play that are in either their first or second season?",
    "What is Nathaniel Hacketts record of hitting the under throughout his coaching career?",
    "What is the Bengals ranking in terms of pass block win rate over the last three seasons?",
    "How do the Bengals perform ATS on a short week?",
    "What is the offensive line and defensive line rank for the Cleveland Browns this season?",
    "What is the Browns stregnth of schedule?",
    "How did Deshaun Watsons performance on the Browns compare to when he's on the Texans?",
    "What are the divisional odds, championship odds, and seasonal o/u for the Pittsburgh Steelers?",
    "What is the Steelers record against the spread as an underdog?",
    "Who is the best coach against the spread from the past 20 seasons?",
    "What was the Steelers record in one score games last season?",
    "What is Brock Purdys record within his division throughout his career?",
    "What is the Niners record with Trent Williams and Deebo Samuel are on the field? How about when they are off the field?",
    "How has the New England Patriots' defense performed against mobile quarterbacks over the past season? Provide data on yards allowed and touchdowns given up.",
    "What is the Green Bay Packers' win-loss record in games decided by 7 points or fewer over the last season? How does this compare to other NFC North teams?",
    "How does Josh Allen's performance (completion percentage, yards per attempt) vary between games played in domes versus outdoor stadiums?",
    "What has been the Pittsburgh Steelers' record in prime-time games over the four seasons? How does this compare to their record in early Sunday games?",
    "How have the Seattle Seahawks performed against the spread in games following a bye week? Provide data from the last ten seasons.",
    "What is the Los Angeles Rams' record in games where they have allowed fewer than 20 points? Compare this to games where they've allowed more than 30 points.",
    "How does Derrick Henry's yards per carry differ in games played against AFC South opponents compared to non-division opponents?",
    "What has been the New Orleans Saints' record in games played in the month of December over the last 4 years? How does this compare to their record in September?",
    "What is the Philadelphia Eagles' win-loss record in games where they've had a turnover differential of +2 or better? Compare this to games with a turnover differential of -2 or worse.",
    "How has Daniel Jones' passer rating varied in games where he was sacked three times or more compared to games with fewer than three sacks?",
    "How have the Miami Dolphins performed in games played in temperatures above 85°F? Compare this to their performance in games below 50°F.",
    "What is Jared Goff's record against NFC North opponents since joining the Detroit Lions? How does this compare to his record against non-divisional teams?"
]

# Define the server URL
SERVER_URL = "http://127.0.0.1:5000"

def get_server_response(question: str) -> str:
    """Send a request to the server and return the response."""
    try:
        response = requests.post(SERVER_URL, json={"message": question})
        response.raise_for_status()
        return response.json()["response"]
    except requests.RequestException as e:
        print(f"Error making request to server: {e}")
        return None

def evaluate_consistency(questions: List[str]) -> (float, List[str]):
    """Evaluate the consistency of server responses using an LLM."""
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key="",
    )

    consistent_count = 0
    total_questions = len(questions)
    inconsistent_questions = []

    for question in questions:
        responses = []
        for _ in range(3):
            response = get_server_response(question)
            if response is not None:
                responses.append(response)

        if len(responses) == 3:
            prompt = f"""
            Question: {question}
            Response 1: {responses[0]}
            Response 2: {responses[1]}
            Response 3: {responses[2]}

            Are these three responses consistent with each other? 
            Answer only 'Yes' if they are consistent, or 'No' if they are not.
            """

            consistency_evaluation = llm.invoke(prompt).content.strip().lower()
            if consistency_evaluation == "yes":
                consistent_count += 1
            else:
                inconsistent_questions.append(question)
        else:
            print(f"Skipping evaluation for '{question}' due to insufficient responses.")

    accuracy = consistent_count / total_questions
    return accuracy, inconsistent_questions

def main():
    accuracy, inconsistent_questions = evaluate_consistency(evaluation_questions)
    print(f"Consistency Accuracy: {accuracy:.2%}")
    print("\nInconsistent questions:")
    for question in inconsistent_questions:
        print(f"- {question}")

if __name__ == "__main__":
    main()