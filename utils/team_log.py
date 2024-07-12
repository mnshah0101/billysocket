
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
You are a data analyst for an NFL team and you have been asked to generate a SQL query to answer the following question. You do not have to completely answer the question, just generate the SQL query to answer the question, and the result will be processed. Do your best to answer the question and do not use placeholder information. The question is:
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
To calculate "Against the Spread" (ATS), you need to determine whether a team has covered the point spread in a game. The formula for ATS can be derived using the team score, opponent score, and point spread as follows:

Formula:
Calculate the Cover Margin:
Cover Margin=(Score+PointSpread)-OpponentScore
Determine ATS Result:

If Cover Margin > 0, the team covered the spread.
If Cover Margin < 0, the team did not cover the spread.
If Cover Margin = 0, it is a push (no winner against the spread).

A negative point spread means the team is favored to win, and a positive point spread means the team is the underdog.


Only respond with the sql query, no explanation or anything else. Encompass the sql query with 
```sql

```


A clever way to get the last game of a team is to do MAX(GameKey), which will give you the last game of the team. 


All columns must be surrounded by double quotes, such as "Name" or "Team".

There is no weather column, so use a combination of temperature, humidity, and wind speed to determine the weather conditions of the game.

</special_instructions>

<question>


Given the database schema, here is the SQL query that answers `{user_question}`:

</question>

Here is an example response for the question: "Ravens record against the spread vs teams with winning records"


<example_response>


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

</example_response>

Your response will be executed on a database of NFL Team Logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.
The default SeasonType is Regular Season or 1. If the question is about a different SeasonType, please specify in the query. The default season is 2023.
Use the Wins and Losses columns to determine the number of wins and losses for a team. They reset each season and each season type. Remember, they are cumulative up to the current game.



Assistant: 

"""


sql_prompt = PromptTemplate.from_template(prompt_template)


testnfl_metadata = """GameKey (INTEGER)
Date (TEXT) - Format: 'YYYY-MM-DDTHH:MM:SS' Remember, this is not a Date type, it is a TEXT type.
SeasonType (REAL)  - (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar). The default season type is 1.
Season (REAL) - The default season is 2023.
Week (REAL)- The week resets for each season type. The default week is 1. Week 17 is the last week of the regular season.
Team (TEXT) 
Opponent (TEXT) - The name of the opponent team.
HomeOrAway (TEXT) - Could be HOME or AWAY
Score (REAL)
OpponentScore (REAL)
TotalScore (REAL)
Stadium (TEXT) - This is where the game was played. Games in England were played in Wembley Stadium or Tottenham Hotspur Stadium
PlayingSurface (TEXT) - Could be Artificial or Grass
Temperature (REAL)
Humidity (REAL)
WindSpeed (REAL)
OverUnder (REAL) - estimated total points scored in the game. Divide by 2 to get the average points per team.
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
DateTime (TEXT) - Looks like 2024-01-15T20:15:00
GlobalGameID (REAL)
GlobalTeamID (REAL)
GlobalOpponentID (REAL)
ScoreID (REAL)
outer_key (INTEGER)
HomeConference (TEXT) - Can be AFC or NFC
HomeDivision (TEXT) - Can be North, East, West, South
HomeFullName (TEXT)
HomeOffensiveScheme (TEXT) -   (3-4, 4-3)
HomeDefensiveScheme (TEXT) - (PRO, 2TE, 3WR)
HomeCity (TEXT)
HomeStadiumDetails (TEXT) - A map that looks like "{'StadiumID': 3, 'Name': 'MetLife Stadium', 'City': 'East Rutherford', 'State': 'NJ', 'Country': 'USA', 'Capacity': 82500, 'PlayingSurface': 'Artificial', 'GeoLat': 40.813528, 'GeoLong': -74.074361, 'Type': 'Outdoor'}"
HomeHeadCoach (TEXT)
AwayConference (TEXT) - Can be AFC or NFC
AwayDivision (TEXT) - Can be North, South, East, or West
AwayFullName (TEXT)
AwayOffensiveScheme (TEXT) - (PRO, 2TE, 3WR
AwayDefensiveScheme (TEXT) - (3-4, 4-3)
AwayCity (TEXT)
AwayStadiumDetails (TEXT) - A map that looks like "{'StadiumID': 3, 'Name': 'MetLife Stadium', 'City': 'East Rutherford', 'State': 'NJ', 'Country': 'USA', 'Capacity': 82500, 'PlayingSurface': 'Artificial', 'GeoLat': 40.813528, 'GeoLong': -74.074361, 'Type': 'Outdoor'}"
AwayHeadCoach (TEXT)
HomeOffensiveCoordinator (TEXT)
HomeDefensiveCoordinator (TEXT)
HomeSpecialTeamsCoach (TEXT)
AwayOffensiveCoordinator (TEXT)
AwayDefensiveCoordinator (TEXT)
AWaySpecialTeamsCoach (TEXT)
Wins (REAL) - These are the wins up to the current game. They reset each season and each season type.
Losses (REAL) - These are the losses up to the current game. They reset each season and each season type.
OpponentWins (REAL) - These are the opponent's wins up to the current game. They reset each season and each season type.
OpponentLosses (REAL) - These are the opponent's losses up to the current game. They reset each season and each season type.
StadiumID (INTEGER)
Name (TEXT) - Home team Stadium Name
City (TEXT) - Home team  City
State (TEXT) - Home team state State
Country (TEXT) - Home team Country
Capacity (INTEGER) - Home team stadium Capacity
PlayingSurface.1 (TEXT) - Home team stadium PlayingSurface
GeoLat (REAL) - Home team Latitude
GeoLong (REAL) - Home team Longitude
Type (TEXT) - Home team type of stadium (Outdoor or Indoor)
IsShortWeek (INTEGER) - 1 if the team is playing on a short week, 0 if not

"""


def team_log_get_answer(model, question):
    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4o', temperature=0.8)

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620')
        

    llm_chain = sql_prompt | llm
    answer = llm_chain.invoke(
        {'user_question': question, "table_metadata_string": testnfl_metadata})

    return answer.content





