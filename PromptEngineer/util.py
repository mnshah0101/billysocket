import dotenv
import os
import time
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic
import time
from openai import OpenAI
import pinecone
from pinecone import Pinecone, ServerlessSpec

dotenv.load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=open_ai_key)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_key)

index_name = "billy-cache"  

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)


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
        cuurent_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        # Define the prompt template with dynamically generated bucket descriptions
        prompt_template = f"""
        <prompt>
        You are Billy, a chatbot that answers questions about the NFL.
        You will be given a chat history with a user with a question at the end about the NFL. You are to choose bucket or buckets that best fits the question to answer it. You will also correct the grammar of the question.

        Remember, the current question is the last line of the chat history. 

        Here are the buckets:

        {bucket_descriptions}

        You will also correct the question and make it grammatically correct. Do not change anything else about the question.
        By the way, the database does not have weather data, just temperature data.
        You may have to use multiple buckets to answer the question.

        You will response in the following format, where there are multiple buckets:
        Bucket: BucketName1
        Bucket: BucketName2
        Bucket: BucketName3
        Question: Corrected Question

        <example_response>
        Bucket: TeamGameLog
        Question: How many games did the 49ers win in 2005 regular season?
        </example_response>

        This is the user inputted question: {{user_question}}

        If you need the most recently played season, it is the 2024 season. We are in the midst of the 2024 season, so we have data for the weeks that have been played. For betting props, the only available information is in 2024 and we have future week data as well, but its not totally complete for some of the later weeks. If no season is specified, assume the most recent season and the Season Type to be the regular season unless said otherwise. For all props, the data is for 2024. For current season, use 2024.


        Remember, the tables have a lot of information, so if you think there is a chance the question could be answered by looking at the data, choose the appropriate bucket. If the question is not about the NFL choose NoBucket. If the question is not clear, make it more specific and easier to understand.

        If you choose NoBucket, instead of a question in the question field, put the reason why it is NoBucket. Remember this is going to be shown to the user, so make sure it is clear and concise. If it is too vague, ask for clarification. Use your knowledge of the NFL to to see if a question is too vague.

        If you choose Conversation, instead of a question in the question field, put the natural conversation you would have with the user. That is going to be returned to the user, so make sure it is clear and concise.
        If you need the current date, it is {cuurent_date}. If the questions mentions today, or tonight or anything of the sort, include this date in the response.
        We just finished week 8 of the 2024 season and are currently in week 9. The 2024 season is the most recent season. We only have performance data up to the weeks that have been played, so use internet tool when asking for weeks that haven't been played. For props, we have data for the 2024 season and future weeks, but it is not totally complete for some of the later weeks. Some teams have not played all weeks.
        Remember, players may have moved teams since when you were last trained, so don't assume you know where players play all the time and still choose an appropriate bucket.
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
                llm = ChatOpenAI(model='gpt-4', temperature=0.3)

            elif model == 'anthropic':
                llm = ChatAnthropic(model_name='claude-3-opus-20240229')

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
                if line.startswith("Bucket:"):
                    buckets.append(line.split("Bucket: ")[1].strip())
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

        similar_question, query = self.find_similar_question_sql(question)

        


        return f"""

        This is the example question: {similar_question}
        
                ```sql
                {query}
                ```
            """
    
    def get_embedding(self, text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding
    
    def find_similar_question_sql(self, question, top_k=1):
        query_embedding = self.get_embedding(question)

        search_results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        if not search_results.matches:
            return None, None

        top_result = search_results.matches[0]

        similar_question = top_result.metadata.get('question')
        sql_query = top_result.metadata.get('sql_query')

        return similar_question, sql_query

    def create_sql_query(self, question, tables, example):

        # Prepare the columns and instructions based on selected tables
        table_information = ''



        for table in tables:
            table_information += f"\n<table>\nTable Name:{table.name}\n<columns>\n{table.columns}\n</columns>\n"
            table_information += f"\n<special_instructions>\n{table.special_instructions}\n</special_instructions>\n</table>\n"

        



        raw_llm_prompt = f"""
            User:

            <instructions>
        You are a data analyst for an NFL team and you have been asked to generate a SQL query to answer the following question. You do not have to completely answer the question, just generate the SQL query to answer the question, and the result will be processed. Do your best to answer the question and do not use placeholder information. 
        The question is: `{question}`

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

            If the question cannot be answered with the data provided, please return the string "Data Error: Cannot Answer Question With Data Provided."


            This is a postgres database. 


            Besides the type CAST syntax, you can use the following syntax to convert a value of one type into another (cast :: operator):
            SELECT ROUND(value::numeric, 2) from table_x; 
            The default SeasonType is Regular Season or 1. If the question is about a different SeasonType, please specify in the query. The default season is 2024.
            Notice that the cast syntax with the cast operator (::) is PostgreSQL-specific and does not conform to the SQL standard.
            All columns should be
            The date is {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}. Use this to reference the current date in your query, 
            the last season there is data for, which is the 2024 season, or the newest season. For betting data use the 2024 season. If no season is specified, assume the most recent season, which is 2024 and the Season Type to be the regular season unless said otherwise.
            If the question cannot be answered with the data provided, return the string "Error: Cannot Be Answered".
            We just finished Week 8 of the 2024 season and are in the midst of Week 9.  There is no historical data for Week 9 yet, but you can answer using historical data from games up until. We have props for future weeks. Some teams haven't played all the games just because of how the schedule has lined up.
            Make sure you surround columns with double quotes since it is case sensitive. An example is p."PlayerName". 
            Only use the columns that are in the table. Do not create any new columns or tables.
            """
        
        add_line = os.getenv('ADD_LINE')

        raw_llm_prompt += add_line
        raw_llm_prompt += f"\nAssitant: "
        

        
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
                llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620', temperature=0.5)

            print(llm)
            llm_chain = sql_prompt | llm
            answer = llm_chain.invoke(input={})

            return answer.content
        
        query = player_log_get_answer('openai', question)

        print(query)





        return query

    def get_query(self, question):
        tables, question = self.choose_tables(question)
        print("This is the question")
        print(question)
    

        if 'Conversation' in [table.name for table in tables]:
            return 'Conversation', question
        if 'NoBucket' in [table.name for table in tables]:
            return 'NoBucket', "I am sorry, I do not have an answer for that question."
        if 'ExpertAnalysis' in [table.name for table in tables]:
            return 'ExpertAnalysis', question




        example = self.get_example(question)
        return 'SQL',self.create_sql_query(question, tables, example)
