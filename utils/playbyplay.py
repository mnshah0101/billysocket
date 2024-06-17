

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
Generate a SQL query to answer the following question:
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


Only respond with the sql query, no explanation or anything else. Encompass the sql query with 
```sql

```


</special_instructions>

<question>


Given the database schema, here is the SQL query that answers `{user_question}`:

</question>


<example_response>

```sql
SELECT SUM(RushingYards) AS Yards
FROM teamlog
WHERE Season = 2023 AND Name = 'Patrick Mahomes'
```

</example_response>





Assistant: 

"""


sql_prompt = PromptTemplate.from_template(prompt_template)


testnfl_metadata = """
Columns in table 'playbyplay':
PlayID (INTEGER)
QuarterID (INTEGER)
QuarterName (TEXT)
Sequence (INTEGER)
TimeRemainingMinutes (INTEGER)
TimeRemainingSeconds (INTEGER)
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
Type (TEXT) - Can be one of ['Kickoff', 'Rush', 'PassCompleted', 'PassIncomplete', 'Punt', 'Penalty', 'Timeout', 'FieldGoal', 'Sack', 'ExtraPoint', 'Period','PassIntercepted', 'Fumble', 'TwoPointConversion']
YardsGained (INTEGER)
Description (TEXT)
IsScoringPlay (INTEGER)
ScoringPlay (REAL)
PlayStatID (REAL)
PlayID_playstats (REAL)
Sequence_playstats (REAL)
PlayerID (REAL)
Name (TEXT) - This is Player Name First Name Last Name
Team_playstats (TEXT)
Opponent_playstats (TEXT)
HomeOrAway (TEXT)
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
TwoPointConversionAttempts (REAL)
TwoPointConversionPasses (REAL)
TwoPointConversionRuns (REAL)
TwoPointConversionReceptions (REAL)
TwoPointConversionReturns (REAL)
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
ScoringPlay.GameKey (REAL)
ScoringPlay.SeasonType (REAL)
ScoringPlay.ScoringPlayID (REAL)
ScoringPlay.Season (REAL)
ScoringPlay.Week (REAL)
ScoringPlay.AwayTeam (TEXT)
ScoringPlay.HomeTeam (TEXT)
ScoringPlay.Date (TEXT)
ScoringPlay.Sequence (REAL)
ScoringPlay.Team (TEXT)
ScoringPlay.Quarter (TEXT)
ScoringPlay.TimeRemaining (TEXT)
ScoringPlay.PlayDescription (TEXT)
ScoringPlay.AwayScore (REAL)
ScoringPlay.HomeScore (REAL)
ScoringPlay.ScoreID (REAL)
GameKey (REAL)
SeasonType (REAL)
ScoringPlayID (REAL)
Season (REAL)
Week (REAL)
AwayTeam (TEXT)
HomeTeam (TEXT)
Date (TEXT)
Sequence_scoringplay (REAL)
Team_scoringplay (TEXT)
Quarter (TEXT)
TimeRemaining (TEXT)
PlayDescription (TEXT)
AwayScore (REAL)
HomeScore (REAL)
ScoreID (REAL)
PlayStatID_stat (REAL)
PlayID_stat (REAL)
Sequence_stat (REAL)
PlayerID_stat (REAL)
Name_stat (TEXT)
Team_stat (TEXT)
Opponent_stat (TEXT)
HomeOrAway_stat (TEXT)
Direction_stat (TEXT)
Updated_stat (TEXT)
Created_stat (TEXT)
PassingAttempts_stat (REAL)
PassingCompletions_stat (REAL)
PassingYards_stat (REAL)
PassingTouchdowns_stat (REAL)
PassingInterceptions_stat (REAL)
PassingSacks_stat (REAL)
PassingSackYards_stat (REAL)
RushingAttempts_stat (REAL)
RushingYards_stat (REAL)
RushingTouchdowns_stat (REAL)
ReceivingTargets_stat (REAL)
Receptions_stat (REAL)
ReceivingYards_stat (REAL)
ReceivingTouchdowns_stat (REAL)
Fumbles_stat (REAL)
FumblesLost_stat (REAL)
TwoPointConversionAttempts_stat (REAL)
TwoPointConversionPasses_stat (REAL)
TwoPointConversionRuns_stat (REAL)
TwoPointConversionReceptions_stat (REAL)
TwoPointConversionReturns_stat (REAL)
SoloTackles_stat (REAL)
AssistedTackles_stat (REAL)
TacklesForLoss_stat (REAL)
Sacks_stat (REAL)
SackYards_stat (REAL)
PassesDefended_stat (REAL)
Safeties_stat (REAL)
FumblesForced_stat (REAL)
FumblesRecovered_stat (REAL)
FumbleReturnYards_stat (REAL)
FumbleReturnTouchdowns_stat (REAL)
Interceptions_stat (REAL)
InterceptionReturnYards_stat (REAL)
InterceptionReturnTouchdowns_stat (REAL)
PuntReturns_stat (REAL)
PuntReturnYards_stat (REAL)
PuntReturnTouchdowns_stat (REAL)
KickReturns_stat (REAL)
KickReturnYards_stat (REAL)
KickReturnTouchdowns_stat (REAL)
BlockedKicks_stat (REAL)
BlockedKickReturns_stat (REAL)
BlockedKickReturnYards_stat (REAL)
BlockedKickReturnTouchdowns_stat (REAL)
FieldGoalReturns_stat (REAL)
FieldGoalReturnYards_stat (REAL)
FieldGoalReturnTouchdowns_stat (REAL)
Kickoffs_stat (REAL)
KickoffYards_stat (REAL)
KickoffTouchbacks_stat (REAL)
Punts_stat (REAL)
PuntYards_stat (REAL)
PuntTouchbacks_stat (REAL)
PuntsHadBlocked_stat (REAL)
FieldGoalsAttempted_stat (REAL)
FieldGoalsMade_stat (REAL)
FieldGoalsYards_stat (REAL)
FieldGoalsHadBlocked_stat (REAL)
ExtraPointsAttempted_stat (REAL)
ExtraPointsMade_stat (REAL)
ExtraPointsHadBlocked_stat (REAL)
Penalties_stat (REAL)
PenaltyYards_stat (REAL)
"""


def play_by_play_get_answer(model, question):
    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4o')

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-opus-20240229')

    llm_chain = sql_prompt | llm
    answer = llm_chain.invoke(
        {'user_question': question, "table_metadata_string": testnfl_metadata})

    return answer.content

