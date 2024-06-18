import time
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()



# Define the prompt template
prompt_template = """
<prompt>

You will be given a question about the NFL. You are to choose which bucket it best fits in. You will also correct the grammar and make the question more specific and easier to understand for our computer systems. 

Here are the buckets:

TeamGameLog - This bucket is for questions that can be answered by looking at Team Game Logs in the NFL. This also includes information about coaches and weather.
PlayerGameLog - This bucket is for questions that can be answered by looking at individual Player Game Logs in the NFL. This includes information about player stats at a game level granularity. This is good for season based questions.
PlayByPlay - This bucket is for questions that can be answered by looking at play by play data for the NFL. 
TeamAndPlayerLog - This bucket is for questions that can be answered by looking at both Team and Player Game Logs in the NFL. This is good for questions that require both team and player stats, such as what the record of a team is when a certain player is/is not playing.
NoBucket - This bucket is for questions that are not about the NFL or cannot be answered by looking at stats.

You will also correct the question and make it more digestible for our computer systems.
You will response in the following format

Bucket: BucketName
Question: Corrected Question

<example_response>
Bucket: TeamGameLog
Question: How many games did the 49ers win in 2005?
</example_response>

This is the user inputted question: {user_question}

The default season is 2023. The default SeasonType is the regular season.


Remember, the tables have a lot of information, so if you think there is a chance the question could be answered by looking at the data, choose the appropriate bucket. If the question is not about the NFL choose NoBucket. If the question is not clear, make it more specific and easier to understand.

</prompt>
"""

# Create the prompt template
billy_prompt = PromptTemplate.from_template(prompt_template)

# Function to ask Billy
def question_chooser(model, question):
    start = time.time()

    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4', temperature=1)

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-opus-20240229',
                            )

    llm_chain = billy_prompt | llm

    llm_response = llm_chain.invoke({'user_question': question})
    print(str(time.time() - start) + ' seconds')

    return extract_bucket_and_question(llm_response.content)


def extract_bucket_and_question(input_string):
    # Split the input string by newline characters
    lines = input_string.split("\n")

    # Initialize variables to store bucket and question
    bucket = ""
    question = ""

    # Iterate over each line and extract bucket and question
    for line in lines:
        if line.startswith("Bucket:"):
            bucket = line.split("Bucket:")[1].strip()
        elif line.startswith("Question:"):
            question = line.split("Question:")[1].strip()

    return bucket, question


