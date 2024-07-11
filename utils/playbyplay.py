

import os
import sqlite3
import pandas as pd
import requests
from langchain.agents import initialize_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import time
from langchain_anthropic import ChatAnthropic
import re
prompt_template = ''

# Define the prompt template
prompt_template = """

User:

<instructions>
You are a data analyst for an NFL team and you have been asked to generate a SQL query to answer the following question. You do not have to completely answer the question, just generate the SQL query to answer the question, and the result will be processed. Do your best to answer the question and do not use placeholder information. The question is:
`{user_question}`

</instructions>


<database_schema>
The query will run on a database of NFL Play by Play with the following schema:
{table_metadata_string}
</database_schema>




<special_instructions>
The Team is always short hand, such as WAS for Washington or BAL for Baltimore.
The name of the table is playbyplay. 
Instead of HomeTeam and AwayTeam, reference the Team column and the HomeOrAway Column, The Opponent column will have the opposite side.
You will have to infer player names from little data from your understanding of the NFL. For example, if the user only says Kelce, you have to infer the name Travis Kelce
When looking for specific match ups, look for plays with the same GameKey for the two teams playing each other.

Only respond with the sql query, no explanation or anything else. Encompass the sql query with 
```sql

```

Note, the data only goes back to the 2015 season.

The Season, Week, HomeTeam, AwayTeam, Date, and GameKey columns are only available for scoring plays.

To filter the data for all plays by date, you can use the PlayTime column. The PlayTime column is in the format of 2022-09-11T22:21:49 and is in UTC time.

Scoring plays only count touchdowns, so for extra points, field goals, and safeties you must use other columns to determine if it is a scoring play.


Remember, do not use GameKey, SeasonType, ScoringPlayID, Season, Week, AwayTeam, HomeTeam, Date, Sequence_scoring, Team_scoring, Quarter, TimeRemaining, PlayDescription, AwayScore, HomeScore, or ScoreID in your query unless it is a scoring play.

This is a postgreSQL database, so you can use the full range of postgreSQL functions and operators.
All columns must be surrounded by double quotes, such as "Name" or "Team".

</special_instructions>

<question>


Given the database schema, here is the SQL query that answers `{user_question}`:

</question>


<example_response>

```sql
SELECT SUM("RushingYards") AS Yards
FROM playbyplay
WHERE "Season" = 2023 AND "Name" = 'Patrick Mahomes'
```

</example_response>




Your response will be executed on a database of NFL Play by Play logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.
Also, keep in mind that there are duplicate plays in the database, so you may need to use DISTINCT with the PlayID to get the correct answer. 

Use the attempted and made columns to calculate percentages. For example, if you want to calculate the extra point conversion percentage, you would use ExtraPointsMade and ExtraPointsAttempted.

Assistant: 

"""


sql_prompt = PromptTemplate.from_template(prompt_template)


testnfl_metadata = """
Columns in table 'playbyplay':
PlayID (INTEGER)
QuarterName (TEXT) - 1, 2, 3, 4, OT
Sequence (INTEGER)
TimeRemainingMinutes (REAL)
TimeRemainingSeconds (REAL)
PlayTime (TEXT)
Updated (TEXT)
Created (TEXT)
Team (TEXT)
Opponent (TEXT)
Down (INTEGER)
Distance (INTEGER)
YardLine (INTEGER)
YardLineTerritory (TEXT)
YardsToEndZone (INTEGER)
Type (TEXT) - The Type of Play that occurred (possible values: Rush, PassCompleted, PassIncomplete, PassIntercepted, TwoPointConversion, Punt, Kickoff, FieldGoal, ExtraPoint, Fumble, Penalty, Sack, Timeout, Period)
YardsGained (INTEGER)
Description (TEXT)
IsScoringPlay (INTEGER) - Only counts for touchdowns.
PlayStatID (REAL)
PlayID_playstats (REAL)
Sequence_playstats (REAL)
PlayerID (REAL)
Name (TEXT)
Team_playstats (TEXT)
Opponent_playstats (TEXT)
HomeOrAway (TEXT)  - HOME or AWAY
Direction (TEXT)
Updated_playstats (TEXT)
Created_playstats (TEXT)
PassingAttempts (REAL)
PassingCompletions (REAL)
PassingYards (REAL)
PassingTouchdowns (REAL)
PassingInterceptions (REAL)
PassingSacks (REAL)
PassingSackYards (REAL)
RushingAttempts (REAL)
RushingYards (REAL)
RushingTouchdowns (REAL)
ReceivingTargets (REAL)
Receptions (REAL)
ReceivingYards (REAL)
ReceivingTouchdowns (REAL)
Fumbles (REAL)
FumblesLost (REAL)
TwoPointConversionAttempts (REAL) - The number of times a player attempted a two point conversion
TwoPointConversionPasses (REAL) - The number of times a player passed for a two point conversion
TwoPointConversionRuns (REAL) - The number of times a player ran for a two point conversion
TwoPointConversionReceptions (REAL) - The number of times a player caught a two point conversion
TwoPointConversionReturns (REAL) - The number of times a player returned a two point conversion
SoloTackles (REAL)
AssistedTackles (REAL)
TacklesForLoss (REAL)
Sacks (REAL)
SackYards (REAL)
PassesDefended (REAL)
Safeties (REAL)
FumblesForced (REAL)
FumblesRecovered (REAL)
FumbleReturnYards (REAL)
FumbleReturnTouchdowns (REAL)
Interceptions (REAL)
InterceptionReturnYards (REAL)
InterceptionReturnTouchdowns (REAL)
PuntReturns (REAL)
PuntReturnYards (REAL)
PuntReturnTouchdowns (REAL)
KickReturns (REAL)
KickReturnYards (REAL)
KickReturnTouchdowns (REAL)
BlockedKicks (REAL)
BlockedKickReturns (REAL)
BlockedKickReturnYards (REAL)
BlockedKickReturnTouchdowns (REAL)
FieldGoalReturns (REAL)
FieldGoalReturnYards (REAL)
FieldGoalReturnTouchdowns (REAL)
Kickoffs (REAL)
KickoffYards (REAL)
KickoffTouchbacks (REAL)
Punts (REAL)
PuntYards (REAL)
PuntTouchbacks (REAL)
PuntsHadBlocked (REAL)
FieldGoalsAttempted (REAL)
FieldGoalsMade (REAL)
FieldGoalsYards (REAL)
FieldGoalsHadBlocked (REAL)
ExtraPointsAttempted (REAL)
ExtraPointsMade (REAL)
ExtraPointsHadBlocked (REAL)
Penalties (REAL)
PenaltyYards (REAL)
GameKey (REAL) - If this is a scoring play, this is the GameKey of the game
SeasonType (REAL) - If this is a scoring play, this is the SeasonType of the game
ScoringPlayID (REAL) - If this is a scoring play, this is the PlayID of the scoring play
Season (REAL) - If this is a scoring play, this is Season of the game
Week (REAL) - If this is a scoring play, this is the Week of the game
AwayTeam (TEXT) - If this is a scoring play, this is the AwayTeam of the game
HomeTeam (TEXT) - If this is a scoring play, this is the HomeTeam of the game
Date (TEXT) - If this is a scoring play, this is the Date of the game
Sequence_scoring (REAL) - The order in which the scoring play happened
Team_scoring (TEXT) - If this is a scoring play, the Team that scored
Quarter (TEXT) - If this is a scoring play, the Quarter in which the scoring play happened
TimeRemaining (TEXT) - If this is a scoring play, the Time Remaining in the Quarter when the scoring play happened
PlayDescription (TEXT) - If this is a scoring play, the PlayDescription of the scoring play
AwayScore (REAL) - If this is a scoring play, the AwayScore (REAL)
HomeScore (REAL) - If this is a scoring play, the HomeScore (REAL)
ScoreID (REAL) - If this is a scoring play, the ScoreID (REAL)
"""


def play_by_play_get_answer(model, question):
    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4o')

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620')

    llm_chain = sql_prompt | llm
    answer = llm_chain.invoke(
        {'user_question': question, "table_metadata_string": testnfl_metadata})

    return answer.content

