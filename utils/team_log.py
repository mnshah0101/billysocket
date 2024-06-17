
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


# Define the prompt template
prompt_template = """

User:

<instructions>
Generate a SQL query to answer the following question:
`{user_question}`

</instructions>


<database_schema>
The query will run on a database of NFL Team Logs with the following schema:
{table_metadata_string}
</database_schema>




<special_instructions>
The team is always short hand, such as WAS for Washington or BAL for Baltimore.
The name of the table is teamlog. 
Instead of HomeTeam and AwayTeam, reference the Team column and the HomeOrAway Column, The Opponent column will have the opposite side.



Only respond with the sql query, no explanation or anything else. Encompass the sql query with 
```sql

```


<special_instructions>

<question>


Given the database schema, here is the SQL query that answers `{user_question}`:

</question>


<example_response>

```sql
SELECT SUM(Fumbles) AS TotalFumbles
FROM teamlog
WHERE Season = 2023 AND Team = 'CLE' OR Opponent = 'CLE';
```

</example_response>





Assistant: 

"""


sql_prompt = PromptTemplate.from_template(prompt_template)


testnfl_metadata = """GameKey (INTEGER)
Date (TEXT)
SeasonType (REAL)  1 == Regular, 2 == PRE, 3 == POST
Season (REAL)
Week (REAL)
Team (TEXT) 
Opponent (TEXT)
HomeOrAway (TEXT) - Could be HOME or AWAY
Score (REAL)
OpponentScore (REAL)
TotalScore (REAL)
Stadium (TEXT)
PlayingSurface (TEXT) - Could be Artificial or Grass
Temperature (REAL)
Humidity (REAL)
WindSpeed (REAL)
OverUnder (REAL)
PointSpread (REAL)
ScoreQuarter1 (REAL)
ScoreQuarter2 (REAL)
ScoreQuarter3 (REAL)
ScoreQuarter4 (REAL)
ScoreOvertime (REAL)
TimeOfPossessionMinutes (REAL)
TimeOfPossessionSeconds (REAL)
TimeOfPossession (TEXT)
FirstDowns (REAL)
FirstDownsByRushing (REAL)
FirstDownsByPassing (REAL)
FirstDownsByPenalty (REAL)
OffensivePlays (REAL)
OffensiveYards (REAL)
OffensiveYardsPerPlay (REAL)
Touchdowns (REAL)
RushingAttempts (REAL)
RushingYards (REAL)
RushingYardsPerAttempt (REAL)
RushingTouchdowns (REAL)
PassingAttempts (REAL)
PassingCompletions (REAL)
PassingYards (REAL)
PassingTouchdowns (REAL)
PassingInterceptions (REAL)
PassingYardsPerAttempt (REAL)
PassingYardsPerCompletion (REAL)
CompletionPercentage (REAL)
PasserRating (REAL)
ThirdDownAttempts (REAL)
ThirdDownConversions (REAL)
ThirdDownPercentage (REAL)
FourthDownAttempts (REAL)
FourthDownConversions (REAL)
FourthDownPercentage (REAL)
RedZoneAttempts (REAL)
RedZoneConversions (REAL)
GoalToGoAttempts (REAL)
GoalToGoConversions (REAL)
ReturnYards (REAL)
Penalties (REAL)
PenaltyYards (REAL)
Fumbles (REAL)
FumblesLost (REAL)
TimesSacked (REAL)
TimesSackedYards (REAL)
QuarterbackHits (REAL)
TacklesForLoss (REAL)
Safeties (REAL)
Punts (REAL)
PuntYards (REAL)
PuntAverage (REAL)
Giveaways (REAL)
Takeaways (REAL)
TurnoverDifferential (REAL)
OpponentScoreQuarter1 (REAL)
OpponentScoreQuarter2 (REAL)
OpponentScoreQuarter3 (REAL)
OpponentScoreQuarter4 (REAL)
OpponentScoreOvertime (REAL)
OpponentTimeOfPossessionMinutes (REAL)
OpponentTimeOfPossessionSeconds (REAL)
OpponentTimeOfPossession (TEXT)
OpponentFirstDowns (REAL)
OpponentFirstDownsByRushing (REAL)
OpponentFirstDownsByPassing (REAL)
OpponentFirstDownsByPenalty (REAL)
OpponentOffensivePlays (REAL)
OpponentOffensiveYards (REAL)
OpponentOffensiveYardsPerPlay (REAL)
OpponentTouchdowns (REAL)
OpponentRushingAttempts (REAL)
OpponentRushingYards (REAL)
OpponentRushingYardsPerAttempt (REAL)
OpponentRushingTouchdowns (REAL)
OpponentPassingAttempts (REAL)
OpponentPassingCompletions (REAL)
OpponentPassingYards (REAL)
OpponentPassingTouchdowns (REAL)
OpponentPassingInterceptions (REAL)
OpponentPassingYardsPerAttempt (REAL)
OpponentPassingYardsPerCompletion (REAL)
OpponentCompletionPercentage (REAL)
OpponentPasserRating (REAL)
OpponentThirdDownAttempts (REAL)
OpponentThirdDownConversions (REAL)
OpponentThirdDownPercentage (REAL)
OpponentFourthDownAttempts (REAL)
OpponentFourthDownConversions (REAL)
OpponentFourthDownPercentage (REAL)
OpponentRedZoneAttempts (REAL)
OpponentRedZoneConversions (REAL)
OpponentGoalToGoAttempts (REAL)
OpponentGoalToGoConversions (REAL)
OpponentReturnYards (REAL)
OpponentPenalties (REAL)
OpponentPenaltyYards (REAL)
OpponentFumbles (REAL)
OpponentFumblesLost (REAL)
OpponentTimesSacked (REAL)
OpponentTimesSackedYards (REAL)
OpponentQuarterbackHits (REAL)
OpponentTacklesForLoss (REAL)
OpponentSafeties (REAL)
OpponentPunts (REAL)
OpponentPuntYards (REAL)
OpponentPuntAverage (REAL)
OpponentGiveaways (REAL)
OpponentTakeaways (REAL)
OpponentTurnoverDifferential (REAL)
RedZonePercentage (REAL)
GoalToGoPercentage (REAL)
QuarterbackHitsDifferential (REAL)
TacklesForLossDifferential (REAL)
QuarterbackSacksDifferential (REAL)
TacklesForLossPercentage (REAL)
QuarterbackHitsPercentage (REAL)
TimesSackedPercentage (REAL)
OpponentRedZonePercentage (REAL)
OpponentGoalToGoPercentage (REAL)
OpponentQuarterbackHitsDifferential (REAL)
OpponentTacklesForLossDifferential (REAL)
OpponentQuarterbackSacksDifferential (REAL)
OpponentTacklesForLossPercentage (REAL)
OpponentQuarterbackHitsPercentage (REAL)
OpponentTimesSackedPercentage (REAL)
Kickoffs (REAL)
KickoffsInEndZone (REAL)
KickoffTouchbacks (REAL)
PuntsHadBlocked (REAL)
PuntNetAverage (REAL)
ExtraPointKickingAttempts (REAL)
ExtraPointKickingConversions (REAL)
ExtraPointsHadBlocked (REAL)
ExtraPointPassingAttempts (REAL)
ExtraPointPassingConversions (REAL)
ExtraPointRushingAttempts (REAL)
ExtraPointRushingConversions (REAL)
FieldGoalAttempts (REAL)
FieldGoalsMade (REAL)
FieldGoalsHadBlocked (REAL)
PuntReturns (REAL)
PuntReturnYards (REAL)
KickReturns (REAL)
KickReturnYards (REAL)
InterceptionReturns (REAL)
InterceptionReturnYards (REAL)
OpponentKickoffs (REAL)
OpponentKickoffsInEndZone (REAL)
OpponentKickoffTouchbacks (REAL)
OpponentPuntsHadBlocked (REAL)
OpponentPuntNetAverage (REAL)
OpponentExtraPointKickingAttempts (REAL)
OpponentExtraPointKickingConversions (REAL)
OpponentExtraPointsHadBlocked (REAL)
OpponentExtraPointPassingAttempts (REAL)
OpponentExtraPointPassingConversions (REAL)
OpponentExtraPointRushingAttempts (REAL)
OpponentExtraPointRushingConversions (REAL)
OpponentFieldGoalAttempts (REAL)
OpponentFieldGoalsMade (REAL)
OpponentFieldGoalsHadBlocked (REAL)
OpponentPuntReturns (REAL)
OpponentPuntReturnYards (REAL)
OpponentKickReturns (REAL)
OpponentKickReturnYards (REAL)
OpponentInterceptionReturns (REAL)
OpponentInterceptionReturnYards (REAL)
SoloTackles (REAL)
AssistedTackles (REAL)
Sacks (REAL)
SackYards (REAL)
PassesDefended (REAL)
FumblesForced (REAL)
FumblesRecovered (REAL)
FumbleReturnYards (REAL)
FumbleReturnTouchdowns (REAL)
InterceptionReturnTouchdowns (REAL)
BlockedKicks (REAL)
PuntReturnTouchdowns (REAL)
PuntReturnLong (REAL)
KickReturnTouchdowns (REAL)
KickReturnLong (REAL)
BlockedKickReturnYards (REAL)
BlockedKickReturnTouchdowns (REAL)
FieldGoalReturnYards (REAL)
FieldGoalReturnTouchdowns (REAL)
PuntNetYards (REAL)
OpponentSoloTackles (REAL)
OpponentAssistedTackles (REAL)
OpponentSacks (REAL)
OpponentSackYards (REAL)
OpponentPassesDefended (REAL)
OpponentFumblesForced (REAL)
OpponentFumblesRecovered (REAL)
OpponentFumbleReturnYards (REAL)
OpponentFumbleReturnTouchdowns (REAL)
OpponentInterceptionReturnTouchdowns (REAL)
OpponentBlockedKicks (REAL)
OpponentPuntReturnTouchdowns (REAL)
OpponentPuntReturnLong (REAL)
OpponentKickReturnTouchdowns (REAL)
OpponentKickReturnLong (REAL)
OpponentBlockedKickReturnYards (REAL)
OpponentBlockedKickReturnTouchdowns (REAL)
OpponentFieldGoalReturnYards (REAL)
OpponentFieldGoalReturnTouchdowns (REAL)
OpponentPuntNetYards (REAL)
IsGameOver (INTEGER)
TeamName (TEXT)
DayOfWeek (TEXT)
PassingDropbacks (REAL)
OpponentPassingDropbacks (REAL)
TeamGameID (REAL)
TwoPointConversionReturns (REAL)
OpponentTwoPointConversionReturns (REAL)
TeamID (REAL)
OpponentID (REAL)
Day (TEXT)
DateTime (TEXT)
GlobalGameID (REAL)
GlobalTeamID (REAL)
GlobalOpponentID (REAL)
ScoreID (REAL)
outer_key (INTEGER)
HomeConference (TEXT)
HomeDivision (TEXT)
HomeFullName (TEXT)
HomeOffensiveScheme (TEXT)
HomeDefensiveScheme (TEXT)
HomeCity (TEXT)
HomeStadiumDetails (TEXT)
HomeHeadCoach (TEXT)
AwayConference (TEXT)
AwayDivision (TEXT)
AwayFullName (TEXT)
AwayOffensiveScheme (TEXT)
AwayDefensiveScheme (TEXT)
AwayCity (TEXT)
AwayStadiumDetails (TEXT)
AwayHeadCoach (TEXT)
HomeOffensiveCoordinator (TEXT)
HomeDefensiveCoordinator (TEXT)
HomeSpecialTeamsCoach (TEXT)
AwayOffensiveCoordinator (TEXT)
AwayDefensiveCoordinator (TEXT)
AWaySpecialTeamsCoach (TEXT)"""


def team_log_get_answer(model, question):
    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4o')

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-opus-20240229',
                         )

    llm_chain = sql_prompt | llm
    answer = llm_chain.invoke(
        {'user_question': question, "table_metadata_string": testnfl_metadata})

    return answer.content





