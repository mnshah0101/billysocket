

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
prompt_template = """

User:

<instructions>
Generate a SQL query to answer the following question:
`{user_question}`

</instructions>


<database_schema>
The query will run on a database of Player Game Logs with the following schema:
{table_metadata_string}
</database_schema>




<special_instructions>
The Team is always short hand, such as WAS for Washington or BAL for Baltimore.
The name of the table is playerlog. 
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
FROM playerlog
WHERE Season = 2023 AND Name = 'Patrick Mahomes'
```

</example_response>


Your response will be executed on a database of NFL Player Logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.



Assistant: 

"""


sql_prompt = PromptTemplate.from_template(prompt_template)


testnfl_metadata = """
GameKey (INTEGER)
PlayerID (INTEGER)
SeasonType (INTEGER) - (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar).
Season (INTEGER)
GameDate (TEXT)
Week (INTEGER) - The week resets for each season type. So the first week of the regular season is 1, the first week of the preseason is 1, etc.
Team (TEXT)
Opponent (TEXT)
HomeOrAway (TEXT) - HOME or AWAY
Number (INTEGER)
Name (TEXT) - First Name and Last Name
Position (TEXT)
PositionCategory (TEXT)
Activated (INTEGER)
Played (INTEGER)
Started (INTEGER)
PassingAttempts (REAL)
PassingCompletions (REAL)
PassingYards (REAL)
PassingCompletionPercentage (REAL)
PassingYardsPerAttempt (REAL)
PassingYardsPerCompletion (REAL)
PassingTouchdowns (REAL)
PassingInterceptions (REAL)
PassingRating (REAL)
PassingLong (REAL)
PassingSacks (REAL)
PassingSackYards (REAL)
RushingAttempts (REAL)
RushingYards (REAL)
RushingYardsPerAttempt (REAL)
RushingTouchdowns (REAL)
RushingLong (REAL)
ReceivingTargets (REAL)
Receptions (REAL)
ReceivingYards (REAL)
ReceivingYardsPerReception (REAL)
ReceivingTouchdowns (REAL)
ReceivingLong (REAL)
Fumbles (REAL)
FumblesLost (REAL)
PuntReturns (REAL)
PuntReturnYards (REAL)
PuntReturnYardsPerAttempt (REAL)
PuntReturnTouchdowns (REAL)
PuntReturnLong (REAL)
KickReturns (REAL)
KickReturnYards (REAL)
KickReturnYardsPerAttempt (REAL)
KickReturnTouchdowns (REAL)
KickReturnLong (REAL)
SoloTackles (REAL)
AssistedTackles (REAL)
TacklesForLoss (REAL)
Sacks (REAL)
SackYards (REAL)
QuarterbackHits (REAL)
PassesDefended (REAL)
FumblesForced (REAL)
FumblesRecovered (REAL)
FumbleReturnYards (REAL)
FumbleReturnTouchdowns (REAL)
Interceptions (REAL)
InterceptionReturnYards (REAL)
InterceptionReturnTouchdowns (REAL)
BlockedKicks (REAL)
SpecialTeamsSoloTackles (REAL)
SpecialTeamsAssistedTackles (REAL)
MiscSoloTackles (REAL)
MiscAssistedTackles (REAL)
Punts (REAL)
PuntYards (REAL)
PuntAverage (REAL)
FieldGoalsAttempted (REAL)
FieldGoalsMade (REAL)
FieldGoalsLongestMade (REAL)
ExtraPointsMade (REAL)
TwoPointConversionPasses (REAL)
TwoPointConversionRuns (REAL)
TwoPointConversionReceptions (REAL)
FantasyPoints (REAL)
FantasyPointsPPR (REAL)
ReceptionPercentage (REAL)
ReceivingYardsPerTarget (REAL)
Tackles (INTEGER)
OffensiveTouchdowns (INTEGER)
DefensiveTouchdowns (INTEGER)
SpecialTeamsTouchdowns (INTEGER)
Touchdowns (INTEGER)
FantasyPosition (TEXT)
FieldGoalPercentage (REAL)
PlayerGameID (INTEGER)
FumblesOwnRecoveries (REAL)
FumblesOutOfBounds (REAL)
KickReturnFairCatches (REAL)
PuntReturnFairCatches (REAL)
PuntTouchbacks (REAL)
PuntInside20 (REAL)
PuntNetAverage (INTEGER)
ExtraPointsAttempted (REAL)
BlockedKickReturnTouchdowns (REAL)
FieldGoalReturnTouchdowns (REAL)
Safeties (REAL)
FieldGoalsHadBlocked (REAL)
PuntsHadBlocked (REAL)
ExtraPointsHadBlocked (REAL)
PuntLong (REAL)
BlockedKickReturnYards (REAL)
FieldGoalReturnYards (REAL)
PuntNetYards (REAL)
SpecialTeamsFumblesForced (REAL)
SpecialTeamsFumblesRecovered (REAL)
MiscFumblesForced (REAL)
MiscFumblesRecovered (REAL)
ShortName (TEXT)
PlayingSurface (TEXT) - Artificial or Grass
IsGameOver (INTEGER)
SafetiesAllowed (REAL)
Stadium (TEXT)
Temperature (REAL)
Humidity (REAL)
WindSpeed (REAL)
FanDuelSalary (REAL)
DraftKingsSalary (REAL)
FantasyDataSalary (REAL)
OffensiveSnapsPlayed (REAL)
DefensiveSnapsPlayed (REAL)
SpecialTeamsSnapsPlayed (REAL)
OffensiveTeamSnaps (REAL)
DefensiveTeamSnaps (REAL)
SpecialTeamsTeamSnaps (REAL)
VictivSalary (REAL)
TwoPointConversionReturns (REAL)
FantasyPointsFanDuel (REAL)
FieldGoalsMade0to19 (REAL)
FieldGoalsMade20to29 (REAL)
FieldGoalsMade30to39 (REAL)
FieldGoalsMade40to49 (REAL)
FieldGoalsMade50Plus (REAL)
FantasyPointsDraftKings (REAL)
YahooSalary (REAL)
FantasyPointsYahoo (REAL)
InjuryStatus (TEXT)
InjuryBodyPart (TEXT)
InjuryStartDate (TEXT)
InjuryNotes (TEXT)
FanDuelPosition (TEXT)
DraftKingsPosition (TEXT)
YahooPosition (TEXT)
OpponentRank (REAL)
OpponentPositionRank (REAL)
InjuryPractice (REAL)
InjuryPracticeDescription (REAL)
DeclaredInactive (INTEGER)
FantasyDraftSalary (REAL)
FantasyDraftPosition (REAL)
TeamID (INTEGER)
OpponentID (INTEGER)
Day (TEXT)
DateTime (TEXT)
GlobalGameID (INTEGER)
GlobalTeamID (INTEGER)
GlobalOpponentID (INTEGER)
ScoreID (INTEGER)
FantasyPointsFantasyDraft (REAL)
OffensiveFumbleRecoveryTouchdowns (REAL)
SnapCountsConfirmed (INTEGER)
Updated (TEXT)
ScoringDetails (TEXT)
source (INTEGER))"""


def player_log_get_answer(model, question):
    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4o', temperature=0.96)

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-opus-20240229',
                           )

    llm_chain = sql_prompt | llm
    answer = llm_chain.invoke(
        {'user_question': question, "table_metadata_string": testnfl_metadata})

    return answer.content


