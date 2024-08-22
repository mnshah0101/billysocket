import dotenv
import os
import time
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic

dotenv.load_dotenv()


class Table:
    def __init__(self, name, table_info, columns, special_instructions):
        self.name = name
        self.columns = columns
        self.special_instructions = special_instructions
        self.table_info = table_info

    def __str__(self):
        return self.name

    def get_prompt(self):
        return self.name + " - " + self.special_instructions


class Prompt:
    def __init__(self, name, type, text):
        self.name = name
        self.type = type
        self.text = text

    def __str__(self):
        return self.text


class PromptEngineer:
    def __init__(self, tables):
        self.tables = tables

    def generate_bucket_descriptions(self):
        descriptions = []
        for table in self.tables:
            descriptions.append(f"{table.name} - {table.special_instructions}")
        return "\n".join(descriptions)

    def choose_tables(self, question):
        # Generate bucket descriptions dynamically from the tables
        bucket_descriptions = self.generate_bucket_descriptions()

        # Define the prompt template with dynamically generated bucket descriptions
        prompt_template = f"""
        <prompt>
        You are Billy, a chatbot that answers questions about the NFL.
        You will be given a chat history with a user with a question at the end about the NFL. You are to choose which buckets it best fits in. You will also correct the grammar of the question.

        Remember, the current question is the last line of the chat history. 

        Here are the buckets:

        {bucket_descriptions}

        You will also correct the question and make it grammatically correct. Do not change anything else about the question.
        You will respond in the following format:

        Buckets: BucketName1, BucketName2, ...
        Question: Corrected Question

        <example_response>
        Buckets: TeamGameLog, PlayerGameLog
        Question: How many games did the 49ers win in 2005 regular season?
        </example_response>

        This is the user inputted question: {{user_question}}

        If you need the most recently played season, it is the 2023 season.  If no season is specified, assume the most recent season and the Season Type to be the regular season unless said otherwise.

        Remember, the tables have a lot of information, so if you think there is a chance the question could be answered by looking at the data, choose the appropriate buckets. If the question is not about the NFL choose NoBucket. If the question is not clear, make it more specific and easier to understand.

        The ExpertAnalysis will be used for anything regarding expert analysis, predictions, live scores, or anything that requires a subjective answer. If you choose expert analysis, in the question field, put the grammatically correct question.

        If you choose NoBucket, instead of a question in the question field, put the reason why it is NoBucket. Remember this is going to be shown to the user, so make sure it is clear and concise. If it is too vague, ask for clarification. Use your knowledge of the NFL to see if a question is too vague.

        If you choose Conversation, instead of a question in the question field, put the natural conversation you would have with the user. 
        </prompt>
        """

        # Create the prompt template
        billy_prompt = PromptTemplate.from_template(prompt_template)

        # Function to ask Billy
        def question_chooser(model, question):
            print('Question: ' + question)
            start = time.time()

            llm = None
            if model == 'openai':
                llm = ChatOpenAI(model='gpt-4', temperature=0.7)

            elif model == 'anthropic':
                llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620')

            llm_chain = billy_prompt | llm

            llm_response = llm_chain.invoke({'user_question': question})

            print(llm_response.content)

            print(str(time.time() - start) + ' seconds')

            return extract_buckets_and_question(llm_response.content)

        def extract_buckets_and_question(input_string):
            # Split the input string by newline characters
            lines = input_string.split("\n")

            # Initialize variables to store buckets and question
            buckets = []
            question = ""

            # Iterate over each line and extract buckets and question
            for line in lines:
                if line.startswith("Buckets:"):
                    buckets = [bucket.strip()
                               for bucket in line.split("Buckets:")[1].split(",")]
                elif line.startswith("Question:"):
                    question = line.split("Question:")[1].strip()

            return buckets, question

        # Use the model from the environment variable to choose the buckets and correct the question
        model = 'openai'
        buckets, fixed_question = question_chooser(model, question)

        # Map the buckets to the corresponding tables
        selected_tables = []
        for table in self.tables:
            if table.name in buckets:
                selected_tables.append(table)

        return selected_tables, fixed_question

    def get_example(self, question):
        return """
                ```sql
                SELECT
                    SUM(CASE WHEN ("Score" + "PointSpread") > "OpponentScore" THEN 1 ELSE 0 END) AS WinsAgainstSpread,
                    SUM(CASE WHEN ("Score" + "PointSpread") < "OpponentScore" THEN 1 ELSE 0 END) AS LossesAgainstSpread,
                    SUM(CASE WHEN ("Score" + "PointSpread") = "OpponentScore" THEN 1 ELSE 0 END) AS PushesAgainstSpread
                FROM
                    teamlog
                WHERE
                    "Season" = 2023
                    AND "SeasonType" = 1
                    AND "Team" = 'BAL'
                    AND "OpponentWins" > OpponentLosses;
                ```
            """

    def create_sql_query(self, question, tables, example):

        # Prepare the columns and instructions based on selected tables
        table_information = ''



        for table in tables:
            table_information += f"\n<table>\nTable Name:{table.name}\n<columns>\n{table.columns}\n</columns>\n"
            table_information += f"\n<special_instructions>\n{table.special_instructions}\n</special_instructions>\n</table>\n"

        



        raw_llm_prompt = f"""
            User:

            <instructions>
            You are a data analyst for an NFL team and you have been asked to generate a SQL query to answer the following question. You do not have to completely answer the question, just generate the SQL query to answer the question, and the result will be processed. Do your best to answer the question and do not use placeholder information. The question is:
            `{question}`

            </instructions>

            I will now provide a series of tables and columns with special instructions for each table to help you answer the question. 

            <table_information>
            The query will run on a database of tables with the following schema. Special instructions for each table are provided below:
            {table_information}
            </information>

        

            Only respond with the sql query, no explanation or anything else. Encompass the sql query with 
            ```sql

            ```
            Note this is a PostgreSQL database and use quotes for column names.
            All columns must be surrounded by double quotes, such as "Name" or "Team".
            Your response will be executed on a database of NFL Player Logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.

            This is an example query that you can use as a template:
            <example_query>
            {example}
            </example_query>

            If the question cannot be answered with the data provided, please return the string "Error: Cannot answer question with data provided."

            This is a postgres database. Do not create any new columns or tables. Only use the columns that are in the table.
            The date is {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}. Use this to reference the current date in your query, the last season there is data for, which is the 2023 season, or the newest season.

            Assistant: 

            """
        
        print("Raw LLM Prompt:")
        print(raw_llm_prompt)
        
        # Create the prompt template
        sql_prompt = PromptTemplate.from_template(
            raw_llm_prompt, validate_template=False)
        
        def player_log_get_answer(model, question):
            llm = None
            if model == 'openai':
                try:
                    llm = ChatOpenAI(model='gpt-4o', temperature=0.96)
                except Exception as e:
                    print("key not given", e)

            elif model == 'anthropic':
                llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620', temperature=0.2)

            print(llm)
            llm_chain = sql_prompt | llm
            answer = llm_chain.invoke(input={})

            return answer.content
        
        query = player_log_get_answer('anthropic', question)

        print(query)





        return query

    def get_query(self, question):
        tables, question = self.choose_tables(question)

        if 'Conversation' in [table.name for table in tables]:
            return 'Conversation', question
        if 'NoBucket' in [table.name for table in tables]:
            return 'NoBucket', "I am sorry, I do not have an answer for that question."
        if 'ExpertAnalysis' in [table.name for table in tables]:
            return 'ExpertAnalysis', question




        example = self.get_example(question)
        return 'SQL',self.create_sql_query(question, tables, example)
