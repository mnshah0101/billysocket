

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
You are a data analyst for an NFL team and you have been asked to generate a SQL query to answer the following question. You do not have to completely answer the question, just generate the SQL query to answer the question, and the result will be processed. Do your best to answer the question and do not use placeholder information. The question is:
`{user_question}`

</instructions>


<database_schema>
The query will run on a database of Player Game Logs and Team Game Logs with the following schema:
{table_metadata_string}
</database_schema>




<special_instructions>
The Team is always short hand, such as WAS for Washington or BAL for Baltimore.
The tables to query are playerlog and teamlog.
Make sure game keys are unique.
Instead of HomeTeam and AwayTeam, reference the Team column and the HomeOrAway Column, The Opponent column will have the opposite side.
You will have to infer player names from little data from your understanding of the NFL. For example, if the user only says Kelce, you have to infer the name Travis Kelce
To calculate "Against the Spread" (ATS), you need to determine whether a team has covered the point spread in a game. The formula for ATS can be derived using the team score, opponent score, and point spread as follows:

Formula:
Calculate the Cover Margin:


Cover Margin=(Score+PointSpread)-OpponentScore
Determine ATS Result:

If Cover Margin > 0, the team covered the spread.
If Cover Margin < 0, the team did not cover the spread.
If Cover Margin = 0, it is a push (no winner against the spread).

Only respond with the sql query, no explanation or anything else. Encompass the sql query with 
```sql

```

You can use MIN(GameKey) to get the earliest game and MAX(GameKey) to get the latest game.

Remember, rookies in the 2023 season have a value of 2 in the Experience column.

A player is injured if the InjuryStatus is Doubtful, Out, or Questionable.

Make sure to use the DISTINCT keyword when necessary to avoid duplicate data.

Usually, even when a player is out or injured, they will have a record in the database. However, sometimes, they might not have a record. Therefore to see how many games a player missed, you can use 17 (or whatever number) - COUNT(DISTINCT GameKey where the player played).

Be careful of periods in the player name. For example, TJ Watt is T.J. Watt in the database.

All columns must be surrounded by double quotes, such as "Name" or "Team".


There is no weather column, so use a combination of temperature, humidity, and wind speed to determine the weather conditions of the game.




</special_instructions>

<question>


Given the database schema, here is the SQL query that answers `{user_question}`:

</question>


<example_response>

```sql
SELECT SUM("RushingYards") AS Yards
FROM playerlog
WHERE "Season" = 2023 AND "Name" = 'Patrick Mahomes'
```

</example_response>


Your response will be executed on a database of NFL Player Logs and NFL Team Logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.

If the question cannot be answered with the data provided, please return the string "Error: Cannot answer question with data provided."



Assistant: 

"""


sql_prompt = PromptTemplate.from_template(prompt_template)


testnfl_metadata = """
Table: TeamLog
GameKey (INTEGER)
Date (TEXT)
SeasonType (REAL)  - (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar). The default season type is 1.
Season (REAL) - The default season is 2023.
Week (REAL)- The week resets for each season type. The default week is 1. Week 17 is the last week of the regular season.
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
AWaySpecialTeamsCoach (TEXT)
Wins (REAL) - These are the wins up to the current game. They reset each season and each season type.
Losses (REAL) - These are the losses up to the current game. They reset each season and each season type.
OpponentWins (REAL) - These are the opponent's wins up to the current game. They reset each season and each season type.
OpponentLosses (REAL) - These are the opponent's losses up to the current game. They reset each season and each season type.
IsShortWeek (INTEGER) - 1 if the team has a short week, 0 otherwise
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

Table: playerlog
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
Position (TEXT) - Player's position for this particular game or season. Possible values: C, CB, DB, DE, DE/LB, DL, DT, FB, FS, G, ILB, K, KR, LB, LS, NT, OL, OLB, OT, P, QB, RB, S, SS, T, TE, WR
PositionCategory (TEXT) - Abbreviation of either Offense, Defense or Special Teams (OFF, DEF, ST)
Activated (INTEGER)
Played (INTEGER) - 1 if player has atleast one play, 0 otherwise
Started (INTEGER) - 1 is player has started
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
InjuryStatus (TEXT) = [None, 'Questionable', 'Probable', 'Out', 'Doubtful']
InjuryBodyPart (TEXT)
FanDuelPosition (TEXT)
DraftKingsPosition (TEXT)
YahooPosition (TEXT)
OpponentRank (REAL)
OpponentPositionRank (REAL)
InjuryPractice (REAL)
InjuryPracticeDescription (REAL)
DeclaredInactive (INTEGER) - If the player is retired or still playing.
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
ScoringDetails (TEXT) - A JSON array of scoring details if the player scored any points in the game. It looks like this: 
[{'GameKey': '200230131',
  'SeasonType': 3,
  'PlayerID': 8223,
  'Team': 'SF',
  'Season': 2002,
  'Week': 1,
  'ScoringType': 'RushingTouchdown',
  'Length': 14,
  'ScoringDetailID': 292738,
  'PlayerGameID': 1797109,
  'ScoringPlayID': 78786}]

source (INTEGER))
Wins (REAL) - This is the number of wins the team had in the season up to this point
OpponentWins (REAL) - This is the number of wins the opponent had in the season up to this point
Losses (REAL)  - This is the number of losses the team had in the season up to this point
OpponentLosses (REAL)  - This is the number of losses the opponent had in the season up to this point
PointSpread (REAL) - This is the point spread of the game.
Score (REAL) - This is the score of the team
OpponentScore (REAL) - This is the score of the opponent
Status (TEXT) - Active or Inactive
Height (TEXT) - Height in feet and inches like 6'0"
BirthDate (TEXT) - The birthdate of the player like 1999-08-31T00:00:00
Weight (REAL) - The weight of the player in pounds
College (TEXT) - The college the player attended
Experience (REAL) - The number of years the player has played in the NFL. Since it is updated every spring, rookies in the 2023 season have a value of 2.

"""


def player_and_team_log_get_answer(model, question):
    llm = None
    if model == 'openai':
        llm = ChatOpenAI(model='gpt-4o', temperature=0.96)

    elif model == 'anthropic':
        llm = ChatAnthropic(model_name='claude-3-5-sonnet-20240620',
                           )

    llm_chain = sql_prompt | llm
    answer = llm_chain.invoke(
    {'user_question': question, "table_metadata_string": testnfl_metadata})

    return answer.content


