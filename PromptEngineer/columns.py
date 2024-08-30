from PromptEngineer.util import Prompt


TeamLogColumns = Prompt("TeamGameLog", "Columns",
                        """
GameKey (BIGINT):
Date (TEXT): Format: 'YYYY-MM-DDTHH:MM:SS'. Remember, this is not a Date type, it is a TEXT type.
SeasonType (BIGINT): (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar). The default season type is 1.
Season (BIGINT): The default season is 2023.
Week (BIGINT): The week resets for each season type. The default week is 1. Week 17 is the last week of the regular season.
Team (TEXT): This is the short abbreviation of the team name.
Opponent (TEXT): The short abbreviation of the opponent team name, like 'KC' for the Kansas City Chiefs.
HomeOrAway (TEXT): Could be HOME or AWAY.
Score (BIGINT):
OpponentScore (BIGINT):
TotalScore (BIGINT):
Stadium (TEXT): This is where the game was played. Games in England were played in Wembley Stadium or Tottenham Hotspur Stadium.
PlayingSurface (TEXT): Could be Artificial or Grass.
Temperature (DOUBLE PRECISION):
Humidity (DOUBLE PRECISION):
WindSpeed (DOUBLE PRECISION):
OverUnder (DOUBLE PRECISION): Estimated total points scored in the game. Divide by 2 to get the average points per team.
PointSpread (DOUBLE PRECISION):
ScoreQuarter1 (BIGINT):
ScoreQuarter2 (BIGINT):
ScoreQuarter3 (BIGINT):
ScoreQuarter4 (BIGINT):
ScoreOvertime (BIGINT):
TimeOfPossessionMinutes (BIGINT):
TimeOfPossessionSeconds (BIGINT):
TimeOfPossession (TEXT)
FirstDowns (BIGINT):
FirstDownsByRushing (DOUBLE PRECISION):
FirstDownsByPassing (DOUBLE PRECISION):
FirstDownsByPenalty (DOUBLE PRECISION):
OffensivePlays (BIGINT):
OffensiveYards (BIGINT):
OffensiveYardsPerPlay (DOUBLE PRECISION):
Touchdowns (DOUBLE PRECISION):
RushingAttempts (BIGINT):
RushingYards (BIGINT):
RushingYardsPerAttempt (DOUBLE PRECISION):
RushingTouchdowns (DOUBLE PRECISION):
PassingAttempts (BIGINT):
PassingCompletions (BIGINT):
PassingYards (BIGINT):
PassingTouchdowns (DOUBLE PRECISION):
PassingInterceptions (BIGINT):
PassingYardsPerAttempt (DOUBLE PRECISION):
PassingYardsPerCompletion (DOUBLE PRECISION):
CompletionPercentage (DOUBLE PRECISION):
PasserRating (DOUBLE PRECISION):
ThirdDownAttempts (DOUBLE PRECISION):
ThirdDownConversions (DOUBLE PRECISION):
ThirdDownPercentage (DOUBLE PRECISION):
FourthDownAttempts (DOUBLE PRECISION):
FourthDownConversions (DOUBLE PRECISION):
FourthDownPercentage (DOUBLE PRECISION):
RedZoneAttempts (DOUBLE PRECISION):
RedZoneConversions (DOUBLE PRECISION):
GoalToGoAttempts (DOUBLE PRECISION):
GoalToGoConversions (DOUBLE PRECISION):
ReturnYards (BIGINT):
Penalties (BIGINT):
PenaltyYards (BIGINT):
Fumbles (BIGINT):
FumblesLost (BIGINT):
TimesSacked (BIGINT):
TimesSackedYards (BIGINT):
QuarterbackHits (DOUBLE PRECISION):
TacklesForLoss (DOUBLE PRECISION):
Safeties (DOUBLE PRECISION):
Punts (BIGINT):
PuntYards (BIGINT):
PuntAverage (DOUBLE PRECISION):
Giveaways (BIGINT):
Takeaways (BIGINT):
TurnoverDifferential (BIGINT):
OpponentScoreQuarter1 (BIGINT):
OpponentScoreQuarter2 (BIGINT):
OpponentScoreQuarter3 (BIGINT):
OpponentScoreQuarter4 (BIGINT):
OpponentScoreOvertime (BIGINT):
OpponentTimeOfPossessionMinutes (BIGINT):
OpponentTimeOfPossessionSeconds (BIGINT):
OpponentTimeOfPossession (TEXT)
OpponentFirstDowns (BIGINT):
OpponentFirstDownsByRushing (DOUBLE PRECISION):
OpponentFirstDownsByPassing (DOUBLE PRECISION):
OpponentFirstDownsByPenalty (DOUBLE PRECISION):
OpponentOffensivePlays (BIGINT):
OpponentOffensiveYards (BIGINT):
OpponentOffensiveYardsPerPlay (DOUBLE PRECISION):
OpponentTouchdowns (DOUBLE PRECISION):
OpponentRushingAttempts (BIGINT):
OpponentRushingYards (BIGINT):
OpponentRushingYardsPerAttempt (DOUBLE PRECISION):
OpponentRushingTouchdowns (DOUBLE PRECISION):
OpponentPassingAttempts (BIGINT):
OpponentPassingCompletions (BIGINT):
OpponentPassingYards (BIGINT):
OpponentPassingTouchdowns (DOUBLE PRECISION):
OpponentPassingInterceptions (BIGINT):
OpponentPassingYardsPerAttempt (DOUBLE PRECISION):
OpponentPassingYardsPerCompletion (DOUBLE PRECISION):
OpponentCompletionPercentage (DOUBLE PRECISION):
OpponentPasserRating (DOUBLE PRECISION):
OpponentThirdDownAttempts (DOUBLE PRECISION):
OpponentThirdDownConversions (DOUBLE PRECISION):
OpponentThirdDownPercentage (DOUBLE PRECISION):
OpponentFourthDownAttempts (DOUBLE PRECISION):
OpponentFourthDownConversions (DOUBLE PRECISION):
OpponentFourthDownPercentage (DOUBLE PRECISION):
OpponentRedZoneAttempts (DOUBLE PRECISION):
OpponentRedZoneConversions (DOUBLE PRECISION):
OpponentGoalToGoAttempts (DOUBLE PRECISION):
OpponentGoalToGoConversions (DOUBLE PRECISION):
OpponentReturnYards (BIGINT):
OpponentPenalties (BIGINT):
OpponentPenaltyYards (BIGINT):
OpponentFumbles (BIGINT):
OpponentFumblesLost (BIGINT):
OpponentTimesSacked (BIGINT):
OpponentTimesSackedYards (BIGINT):
OpponentQuarterbackHits (DOUBLE PRECISION):
OpponentTacklesForLoss (DOUBLE PRECISION):
OpponentSafeties (DOUBLE PRECISION):
OpponentPunts (BIGINT):
OpponentPuntYards (BIGINT):
OpponentPuntAverage (DOUBLE PRECISION):
OpponentGiveaways (BIGINT):
OpponentTakeaways (BIGINT):
OpponentTurnoverDifferential (BIGINT):
RedZonePercentage (DOUBLE PRECISION):
GoalToGoPercentage (DOUBLE PRECISION):
QuarterbackHitsDifferential (BIGINT):
TacklesForLossDifferential (BIGINT):
QuarterbackSacksDifferential (BIGINT):
TacklesForLossPercentage (DOUBLE PRECISION):
QuarterbackHitsPercentage (DOUBLE PRECISION):
TimesSackedPercentage (DOUBLE PRECISION):
OpponentRedZonePercentage (DOUBLE PRECISION):
OpponentGoalToGoPercentage (DOUBLE PRECISION):
OpponentQuarterbackHitsDifferential (BIGINT):
OpponentTacklesForLossDifferential (BIGINT):
OpponentQuarterbackSacksDifferential (BIGINT):
OpponentTacklesForLossPercentage (DOUBLE PRECISION):
OpponentQuarterbackHitsPercentage (DOUBLE PRECISION):
OpponentTimesSackedPercentage (DOUBLE PRECISION):
Kickoffs (DOUBLE PRECISION):
KickoffsInEndZone (DOUBLE PRECISION):
KickoffTouchbacks (DOUBLE PRECISION):
PuntsHadBlocked (DOUBLE PRECISION):
PuntNetAverage (DOUBLE PRECISION):
ExtraPointKickingAttempts (DOUBLE PRECISION):
ExtraPointKickingConversions (DOUBLE PRECISION):
ExtraPointsHadBlocked (DOUBLE PRECISION):
ExtraPointPassingAttempts (DOUBLE PRECISION):
ExtraPointPassingConversions (DOUBLE PRECISION):
ExtraPointRushingAttempts (DOUBLE PRECISION):
ExtraPointRushingConversions (DOUBLE PRECISION):
FieldGoalAttempts (DOUBLE PRECISION):
FieldGoalsMade (DOUBLE PRECISION):
FieldGoalsHadBlocked (DOUBLE PRECISION):
PuntReturns (DOUBLE PRECISION):
PuntReturnYards (DOUBLE PRECISION):
KickReturns (DOUBLE PRECISION):
KickReturnYards (DOUBLE PRECISION):
InterceptionReturns (DOUBLE PRECISION):
InterceptionReturnYards (DOUBLE PRECISION):
OpponentKickoffs (DOUBLE PRECISION):
OpponentKickoffsInEndZone (DOUBLE PRECISION):
OpponentKickoffTouchbacks (DOUBLE PRECISION):
OpponentPuntsHadBlocked (DOUBLE PRECISION):
OpponentPuntNetAverage (DOUBLE PRECISION):
OpponentExtraPointKickingAttempts (DOUBLE PRECISION):
OpponentExtraPointKickingConversions (DOUBLE PRECISION):
OpponentExtraPointsHadBlocked (DOUBLE PRECISION):
OpponentExtraPointPassingAttempts (DOUBLE PRECISION):
OpponentExtraPointPassingConversions (DOUBLE PRECISION):
OpponentExtraPointRushingAttempts (DOUBLE PRECISION):
OpponentExtraPointRushingConversions (DOUBLE PRECISION):
OpponentFieldGoalAttempts (DOUBLE PRECISION):
OpponentFieldGoalsMade (DOUBLE PRECISION):
OpponentFieldGoalsHadBlocked (DOUBLE PRECISION):
OpponentPuntReturns (DOUBLE PRECISION):
OpponentPuntReturnYards (DOUBLE PRECISION):
OpponentKickReturns (DOUBLE PRECISION):
OpponentKickReturnYards (DOUBLE PRECISION):
OpponentInterceptionReturns (DOUBLE PRECISION):
OpponentInterceptionReturnYards (DOUBLE PRECISION):
SoloTackles (DOUBLE PRECISION):
AssistedTackles (DOUBLE PRECISION):
Sacks (DOUBLE PRECISION):
SackYards (DOUBLE PRECISION):
PassesDefended (DOUBLE PRECISION):
FumblesForced (DOUBLE PRECISION):
FumblesRecovered (DOUBLE PRECISION):
FumbleReturnYards (DOUBLE PRECISION):
FumbleReturnTouchdowns (DOUBLE PRECISION):
InterceptionReturnTouchdowns (DOUBLE PRECISION):
BlockedKicks (DOUBLE PRECISION):
PuntReturnTouchdowns (DOUBLE PRECISION):
PuntReturnLong (DOUBLE PRECISION):
KickReturnTouchdowns (DOUBLE PRECISION):
KickReturnLong (DOUBLE PRECISION):
BlockedKickReturnYards (DOUBLE PRECISION):
BlockedKickReturnTouchdowns (DOUBLE PRECISION):
FieldGoalReturnYards (DOUBLE PRECISION):
FieldGoalReturnTouchdowns (DOUBLE PRECISION):
PuntNetYards (DOUBLE PRECISION):
OpponentSoloTackles (DOUBLE PRECISION):
OpponentAssistedTackles (DOUBLE PRECISION):
OpponentSacks (DOUBLE PRECISION):
OpponentSackYards (DOUBLE PRECISION):
OpponentPassesDefended (DOUBLE PRECISION):
OpponentFumblesForced (DOUBLE PRECISION):
OpponentFumblesRecovered (DOUBLE PRECISION):
OpponentFumbleReturnYards (DOUBLE PRECISION):
OpponentFumbleReturnTouchdowns (DOUBLE PRECISION):
OpponentInterceptionReturnTouchdowns (DOUBLE PRECISION):
OpponentBlockedKicks (DOUBLE PRECISION):
OpponentPuntReturnTouchdowns (DOUBLE PRECISION):
OpponentPuntReturnLong (DOUBLE PRECISION):
OpponentKickReturnTouchdowns (DOUBLE PRECISION):
OpponentKickReturnLong (DOUBLE PRECISION):
OpponentBlockedKickReturnYards (DOUBLE PRECISION):
OpponentBlockedKickReturnTouchdowns (DOUBLE PRECISION):
OpponentFieldGoalReturnYards (DOUBLE PRECISION):
OpponentFieldGoalReturnTouchdowns (DOUBLE PRECISION):
OpponentPuntNetYards (DOUBLE PRECISION):
IsGameOver (BIGINT):
TeamName (TEXT):
DayOfWeek (TEXT):
PassingDropbacks (BIGINT):
OpponentPassingDropbacks (BIGINT):
TeamGameID (BIGINT):
TwoPointConversionReturns (BIGINT):
OpponentTwoPointConversionReturns (BIGINT):
TeamID (BIGINT):
OpponentID (BIGINT):
Day (TEXT):
DateTime (TEXT): Looks like 2024-01-15T20:15:00
GlobalGameID (BIGINT):
GlobalTeamID (BIGINT):
GlobalOpponentID (BIGINT):
ScoreID (BIGINT):
outer_key (TEXT):
Wins (BIGINT): These are the wins up to the current game. They reset each season and each season type.
Losses (BIGINT): These are the losses up to the current game. They reset each season and each season type.
OpponentWins (BIGINT): These are the opponent's wins up to the current game. They reset each season and each season type.
OpponentLosses (BIGINT): These are the opponent's losses up to the current game. They reset each season and each season type.
StadiumID (BIGINT):
Name (TEXT): Home team Stadium Name.
City (TEXT): Home team City.
State (TEXT): Home team State.
Country (TEXT): Home team Country.
Capacity (BIGINT): Home team stadium Capacity.
PlayingSurface (TEXT): Home team stadium PlayingSurface.
GeoLat (DOUBLE PRECISION): Home team Latitude.
GeoLong (DOUBLE PRECISION): Home team Longitude.
Type (TEXT): Home team type of stadium (Outdoor or Indoor).
IsShortWeek (BIGINT): 1 if the team is playing on a short week, 0 if not.
""")

PlayerLogColumns = Prompt("PlayerGameLog", "Columns",
"""
GameKey (bigint)
PlayerID (bigint)
SeasonType (bigint) - (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar).
Season (bigint)
GameDate (text)
Week (bigint) - The week resets for each season type. So the first week of the regular season is 1, the first week of the preseason is 1, etc.
Team (text)
Opponent (text)
HomeOrAway (text) - HOME or AWAY
Number (bigint)
Name (text) - First Name and Last Name
Position (text) - Player's position for this particular game or season. Possible values: C, CB, DB, DE, DE/LB, DL, DT, FB, FS, G, ILB, K, KR, LB, LS, NT, OL, OLB, OT, P, QB, RB, S, SS, T, TE, WR
PositionCategory (text) - Abbreviation of either Offense, Defense or Special Teams (OFF, DEF, ST)
Activated (bigint)
Played (bigint) - 1 if player has atleast one play, 0 otherwise
Started (bigint) - 1 is player has started
PassingAttempts (double precision)
PassingCompletions (double precision)
PassingYards (double precision)
PassingCompletionPercentage (double precision)
PassingYardsPerAttempt (double precision)
PassingYardsPerCompletion (double precision)
PassingTouchdowns (double precision)
PassingInterceptions (double precision)
PassingRating (double precision)
PassingLong (double precision)
PassingSacks (double precision)
PassingSackYards (double precision)
RushingAttempts (double precision)
RushingYards (double precision)
RushingYardsPerAttempt (double precision)
RushingTouchdowns (double precision)
RushingLong (double precision)
ReceivingTargets (double precision)
Receptions (double precision)
ReceivingYards (double precision)
ReceivingYardsPerReception (double precision)
ReceivingTouchdowns (double precision)
ReceivingLong (double precision)
Fumbles (double precision)
FumblesLost (double precision)
PuntReturns (double precision)
PuntReturnYards (double precision)
PuntReturnYardsPerAttempt (double precision)
PuntReturnTouchdowns (double precision)
PuntReturnLong (double precision)
KickReturns (double precision)
KickReturnYards (double precision)
KickReturnYardsPerAttempt (double precision)
KickReturnTouchdowns (double precision)
KickReturnLong (double precision)
SoloTackles (double precision)
AssistedTackles (double precision)
TacklesForLoss (double precision)
Sacks (double precision)
SackYards (double precision)
QuarterbackHits (double precision)
PassesDefended (double precision)
FumblesForced (double precision)
FumblesRecovered (double precision)
FumbleReturnYards (double precision)
FumbleReturnTouchdowns (double precision)
Interceptions (double precision)
InterceptionReturnYards (double precision)
InterceptionReturnTouchdowns (double precision)
BlockedKicks (double precision)
SpecialTeamsSoloTackles (double precision)
SpecialTeamsAssistedTackles (double precision)
MiscSoloTackles (double precision)
MiscAssistedTackles (double precision)
Punts (double precision)
PuntYards (double precision)
PuntAverage (double precision)
FieldGoalsAttempted (double precision)
FieldGoalsMade (double precision)
FieldGoalsLongestMade (double precision)
ExtraPointsMade (double precision)
TwoPointConversionPasses (double precision)
TwoPointConversionRuns (double precision)
TwoPointConversionReceptions (double precision)
FantasyPoints (double precision)
FantasyPointsPPR (double precision)
ReceptionPercentage (double precision)
ReceivingYardsPerTarget (double precision)
Tackles (bigint)
OffensiveTouchdowns (bigint)
DefensiveTouchdowns (bigint)
SpecialTeamsTouchdowns (bigint)
Touchdowns (bigint)
FantasyPosition (text)
FieldGoalPercentage (double precision)
PlayerGameID (bigint)
FumblesOwnRecoveries (double precision)
FumblesOutOfBounds (double precision)
KickReturnFairCatches (double precision)
PuntReturnFairCatches (double precision)
PuntTouchbacks (double precision)
PuntInside20 (double precision)
PuntNetAverage (bigint)
ExtraPointsAttempted (double precision)
BlockedKickReturnTouchdowns (double precision)
FieldGoalReturnTouchdowns (double precision)
Safeties (double precision)
FieldGoalsHadBlocked (double precision)
PuntsHadBlocked (double precision)
ExtraPointsHadBlocked (double precision)
PuntLong (double precision)
BlockedKickReturnYards (double precision)
FieldGoalReturnYards (double precision)
PuntNetYards (double precision)
SpecialTeamsFumblesForced (double precision)
SpecialTeamsFumblesRecovered (double precision)
MiscFumblesForced (double precision)
MiscFumblesRecovered (double precision)
ShortName (text)
PlayingSurface (text) - Artificial or Grass
IsGameOver (bigint)
SafetiesAllowed (double precision)
Stadium (text)
Temperature (double precision)
Humidity (double precision)
WindSpeed (double precision)
FanDuelSalary (double precision)
DraftKingsSalary (double precision)
FantasyDataSalary (double precision)
OffensiveSnapsPlayed (double precision)
DefensiveSnapsPlayed (double precision)
SpecialTeamsSnapsPlayed (double precision)
OffensiveTeamSnaps (double precision)
DefensiveTeamSnaps (double precision)
SpecialTeamsTeamSnaps (double precision)
VictivSalary (double precision)
TwoPointConversionReturns (double precision)
FantasyPointsFanDuel (double precision)
FieldGoalsMade0to19 (double precision)
FieldGoalsMade20to29 (double precision)
FieldGoalsMade30to39 (double precision)
FieldGoalsMade40to49 (double precision)
FieldGoalsMade50Plus (double precision)
FantasyPointsDraftKings (double precision)
YahooSalary (double precision)
FantasyPointsYahoo (double precision)
InjuryStatus (text) - [None, 'Questionable', 'Probable', 'Out', 'Doubtful']
InjuryBodyPart (text)
FanDuelPosition (text)
DraftKingsPosition (text)
YahooPosition (text)
OpponentRank (double precision)
OpponentPositionRank (double precision)
InjuryPractice (double precision)
InjuryPracticeDescription (double precision)
DeclaredInactive (bigint) - If the player is retired or still playing.
FantasyDraftSalary (double precision)
FantasyDraftPosition (double precision)
TeamID (bigint)
OpponentID (bigint)
Day (text)
DateTime (text)
GlobalGameID (bigint)
GlobalTeamID (bigint)
GlobalOpponentID (bigint)
ScoreID (bigint)
FantasyPointsFantasyDraft (double precision)
OffensiveFumbleRecoveryTouchdowns (double precision)
SnapCountsConfirmed (bigint)
Updated (text)
source (bigint))
Wins (double precision) - This is the number of wins the team had in the season up to this point
OpponentWins (double precision) - This is the number of wins the opponent had in the season up to this point
Losses (double precision)  - This is the number of losses the team had in the season up to this point
OpponentLosses (double precision)  - This is the number of losses the opponent had in the season up to this point
PointSpread (double precision) - This is the point spread of the game.
Score (double precision) - This is the score of the team
OpponentScore (double precision) - This is the score of the opponent
Status (text) - Active or Inactive
Height (text) - Height in feet and inches like 6'0"
BirthDate (text) - The birthdate of the player like 1999-08-31T00:00:00
Weight (double precision) - The weight of the player in pounds
College (text) - The college the player attended
Experience (double precision) - The number of years the player has played in the NFL. Since it is updated every spring, rookies in the 2023 season have a value of 2.
""")
                        

PlayByPlayColumns = Prompt("PlayByPlay", "Columns",
"""
Columns in table 'playbyplay':
PlayID (bigint)
QuarterName (text) - 1, 2, 3, 4, OT
Sequence (bigint)
TimeRemainingMinutes (double precision)
TimeRemainingSeconds (double precision)
PlayTime (text)
Updated (text) - Looks like 2024-05-15T20:29:55
Created (text) - Looks like 2024-05-15T20:29:55
Team (text)
Opponent (text)
Down (bigint)
Distance (bigint)
YardLine (bigint)
YardLineTerritory (text)
YardsToEndZone (bigint)
Type (text) - The Type of Play that occurred (possible values: Rush, PassCompleted, PassIncomplete, PassIntercepted, TwoPointConversion, Punt, Kickoff, FieldGoal, ExtraPoint, Fumble, Penalty, Sack, Timeout, Period)
YardsGained (bigint)
IsScoringPlay (bigint) - Only counts for touchdowns.
PlayStatID (double precision)
PlayID_playstats (double precision)
Sequence_playstats (double precision)
PlayerID (double precision)
Name (text)
Team_playstats (text)
Opponent_playstats (text)
HomeOrAway (text)  - HOME or AWAY
Direction (text) - The direction of the play (possible values: Left, Middle, Right)
Updated_playstats (text)
Created_playstats (text)
PassingAttempts (double precision)
PassingCompletions (double precision)
PassingYards (double precision)
PassingTouchdowns (double precision)
PassingInterceptions (double precision)
PassingSacks (double precision)
PassingSackYards (double precision)
RushingAttempts (double precision)
RushingYards (double precision)
RushingTouchdowns (double precision)
ReceivingTargets (double precision)
Receptions (double precision)
ReceivingYards (double precision)
ReceivingTouchdowns (double precision)
Fumbles (double precision)
FumblesLost (double precision)
TwoPointConversionAttempts (double precision) - The number of times a player attempted a two point conversion
TwoPointConversionPasses (double precision) - The number of times a player passed for a two point conversion
TwoPointConversionRuns (double precision) - The number of times a player ran for a two point conversion
TwoPointConversionReceptions (double precision) - The number of times a player caught a two point conversion
TwoPointConversionReturns (double precision) - The number of times a player returned a two point conversion
SoloTackles (double precision)
AssistedTackles (double precision)
TacklesForLoss (double precision)
Sacks (double precision)
SackYards (double precision)
PassesDefended (double precision)
Safeties (double precision)
FumblesForced (double precision)
FumblesRecovered (double precision)
FumbleReturnYards (double precision)
FumbleReturnTouchdowns (double precision)
Interceptions (double precision)
InterceptionReturnYards (double precision)
InterceptionReturnTouchdowns (double precision)
PuntReturns (double precision)
PuntReturnYards (double precision)
PuntReturnTouchdowns (double precision)
KickReturns (double precision)
KickReturnYards (double precision)
KickReturnTouchdowns (double precision)
BlockedKicks (double precision)
BlockedKickReturns (double precision)
BlockedKickReturnYards (double precision)
BlockedKickReturnTouchdowns (double precision)
FieldGoalReturns (double precision)
FieldGoalReturnYards (double precision)
FieldGoalReturnTouchdowns (double precision)
Kickoffs (double precision)
KickoffYards (double precision)
KickoffTouchbacks (double precision)
Punts (double precision)
PuntYards (double precision)
PuntTouchbacks (double precision)
PuntsHadBlocked (double precision)
FieldGoalsAttempted (double precision)
FieldGoalsMade (double precision)
FieldGoalsYards (double precision)
FieldGoalsHadBlocked (double precision)
ExtraPointsAttempted (double precision)
ExtraPointsMade (double precision)
ExtraPointsHadBlocked (double precision)
Penalties (double precision)
PenaltyYards (double precision)
GameKey (double precision) - If this is a scoring play, this is the GameKey of the game
SeasonType (double precision) - If this is a scoring play, this is the SeasonType of the game
ScoringPlayID (double precision) - If this is a scoring play, this is the PlayID of the scoring play
Season (double precision) - If this is a scoring play, this is Season of the game
Week (double precision) - If this is a scoring play, this is the Week of the game
AwayTeam (text) - If this is a scoring play, this is the AwayTeam of the game
HomeTeam (text) - If this is a scoring play, this is the HomeTeam of the game
Date (text) - If this is a scoring play, this is the Date of the game
Sequence_scoring (double precision) - The order in which the scoring play happened
Team_scoring (text) - If this is a scoring play, the Team that scored
Quarter (text) - If this is a scoring play, the Quarter in which the scoring play happened
TimeRemaining (text) - If this is a scoring play, the Time Remaining in the Quarter when the scoring play happened
AwayScore (double precision) - If this is a scoring play, the AwayScore (double precision)
HomeScore (double precision) - If this is a scoring play, the HomeScore (double precision)
ScoreID (double precision) - If this is a scoring play, the ScoreID (double precision)
""")


BettingPropsColumns = Prompt("BettingProps", "Columns",
"""
Note that the double parentheses are used to represent a dictionary in the text format. For example, {{'SportsbookID': 8, 'Name': 'FanDuel'}} is a dictionary in the text format. When you see double parentheses, you should treat it as single parentheses in the actual data.
Columns in table 'bettingprops':
Closed (boolean)
ConsensusOutcomes (double precision)
BettingBetTypeID (bigint) - The unique ID of the bet type.
AwayTeamID (bigint)
HomeTeamID (bigint)
GlobalGameID (bigint)
GlobalAwayTeamID (bigint)
GlobalHomeTeamID (bigint)
PointSpreadAwayTeamMoneyLine (bigint)
PointSpreadHomeTeamMoneyLine (bigint)
ScoreID (bigint)
GameKey (bigint)
HomeRotationNumber (double precision)
AwayRotationNumber (double precision)
OverPayout (bigint)
UnderPayout (bigint)
SeasonType (bigint)
Attendance (bigint)
IsClosed (boolean)
Season (bigint)
Week (bigint)
BettingMarketTypeID (bigint)
BettingPeriodTypeID (bigint)
AnyBetsAvailable (boolean)
BettingEventID (bigint) - The unique ID of the event in the market.
PointSpread (double precision) 
OverUnder (double precision)
HasStarted (boolean)
IsInProgress (boolean)
IsOver (boolean)
Has1stQuarterStarted (boolean)
Has2ndQuarterStarted (boolean)
Has3rdQuarterStarted (boolean)
Has4thQuarterStarted (boolean)
IsOvertime (boolean)
PlayerID (double precision) - Player id if is player prop or None
StadiumID (bigint) - The unique ID of the stadium where the game is played.
BettingMarketID (bigint) - The unique ID of the bet in the market.
AwayTeamMoneyLine (bigint)
HomeTeamMoneyLine (bigint)
Canceled (boolean)
LastUpdated (text) -
BettingMarketType (text) - Could be ['Game Line', 'Player Prop', 'Team Prop', 'Game Prop']
BettingBetType (text) - Could be ['Total Points', 'Spread', 'Moneyline', 'Total Passing Yards', 'Total Rushing Yards', 'Total Receiving Yards', 'To Score a Touchdown', 'Player To Score Last Touchdown', 'To Score First Touchdown', 'To Score a D/ST Touchdown','Total Points Odd/Even', 'To Go To Overtime','First Team To Score', 'Total Rushing + Receiving TDs', 'Team To Score First Touchdown', 'Total Rushing & Receiving Yards', 'Total Field Goals Scored', 'Total Receptions', 'Race to 10 Points', 'Race To 20 Points', 'Race To 15 Points', 'Race To 25 Points', 'Moneyline (3-Way)', 'To Complete First Pass']
BettingPeriodType (text) - Could be ['Full Game', 'First Half', '1st Quarter', 'Regular Season']
PlayerName (text) - Player name if player prop or None
Created (text)
Updated (text)
AvailableSportsbooks (text) - An array of the names of the available sportsbooks, like [FanDuel, DraftKings, BetMGM, Caesars, Consensus] without the quotes.
AvailableSportsbooksNames (text) - An array of the names of the available sportsbooks, like ['FanDuel', 'DraftKings', 'BetMGM', 'Caesars', 'Consensus'], with the quotes.
Date (text)
AwayTeam (text) - The short name of the away team, like SF for the San Francisco 49ers.
HomeTeam (text) - The short name of the home team, like DET for the Detroit Lions.
Channel (text)
Day (text)
DateTime (text)
Status (text) - Could be ['Scheduled', 'Final']
DateTimeUTC (text)
StadiumDetails (text) - Looks like {{'StadiumID': 87, 'Name': 'Arena Corinthians', 'City': 'Sao Paulo', 'State': None, 'Country': 'Brazil', 'Capacity': 47252, 'PlayingSurface': 'Grass', 'GeoLat': -23.54525, 'GeoLong': -46.474278, 'Type': 'Outdoor'}}
""")

ByeWeekColumns = Prompt("ByeWeek", "Columns",
""" 
Season (bigint)
Week (bigint)
Team (text)
"""
    
    )



BettingOutcomesColumns = Prompt("BettingOutcomes", "Columns",
"""
GlobalTeamID (double precision)
PayoutDecimal (double precision)
IsInPlay (boolean)
SportsbookMarketID (double precision)
SportsbookOutcomeID (double precision)
BettingOutcomeID (bigint) - The unique ID of the betting outcome.
Value (double precision)
BettingOutcomeTypeID (double precision)
IsAvailable (boolean)
IsAlternate (boolean)
BettingMarketID (bigint) - The unique ID of the betting market.
PayoutAmerican (bigint)
Unlisted (double precision)
TeamID (double precision)
PlayerID (double precision) - Player ID if related to a player prop.
SportsBook (text) - Looks like 'FanDuel' or 'DraftKings' or 'BetMGM' or 'Caesars' or 'Consensus'
BettingOutcomeType (text) - Either ['Over', 'Under', 'Away', 'Home', 'Yes', nan, 'Odd', 'Even', 'No']
Participant (text) - Either full team name or player name. Example: 'New York Giants' or 'Saquon Barkley'
Created (text)
Updated (text)
SportsbookUrl (text)

""")

TeamInfoColumns = Prompt("TeamInfo", "Columns",
                         """
index (bigint) - The unique index of the record.
TeamID (bigint) - The unique ID of the team.
StadiumID (bigint) - The unique ID of the stadium.
ByeWeek (bigint) - The week in which the team has a bye.
AverageDraftPosition (double precision) - The average draft position of the team.
AverageDraftPositionPPR (double precision) - The average draft position of the team in PPR leagues.
UpcomingSalary (bigint) - The teams's upcoming salary.
UpcomingOpponentRank (bigint) - The rank of the upcoming opponent.
UpcomingOpponentPositionRank (bigint) - The position rank of the upcoming opponent.
UpcomingFanDuelSalary (double precision) - The upcoming salary on FanDuel.
UpcomingDraftKingsSalary (double precision) - The upcoming salary on DraftKings.
UpcomingYahooSalary (double precision) - The upcoming salary on Yahoo.
GlobalTeamID (bigint) - The global ID of the team.
DraftKingsPlayerID (bigint) - The DraftKings-specific ID of the team.
FanDuelPlayerID (bigint) - The FanDuel-specific ID of the player.
FantasyDraftPlayerID (bigint) - The FantasyDraft-specific ID of the team.
YahooPlayerID (bigint) - The Yahoo-specific ID of the team.
AverageDraftPosition2QB (double precision) - The average draft position in 2QB leagues.
AverageDraftPositionDynasty (double precision) - The average draft position in dynasty leagues.
Season (bigint) - The season associated with the data.
FantasyDraftName (text) - The team's name on FantasyDraft.
DraftKingsName (text) - The team's name on DraftKings.
StadiumDetails (text) - Details about the teams stadium.
FanDuelName (text) - The team's name on FanDuel.
Key (text) - The team abbreviation, like DET for the Detroit Lions, or SF for the San Francisco 49ers.
YahooName (text) - The team's name on Yahoo.
PrimaryColor (text) - The primary color associated with the team.
City (text) - The city where the team is based.
Name (text) - The name of the team.
Conference (text) - The conference the team belongs to. This could be AFC or NFC.
Division (text) - The division the team belongs to. This could be East, North, South, or West.
FullName (text) - The full name of the team or team.
SecondaryColor (text) - The secondary color associated with the team.
TertiaryColor (text) - The tertiary color associated with the team.
QuaternaryColor (text) - The quaternary color associated with the team.
WikipediaLogoUrl (text) - The URL to the team's logo on Wikipedia.
HeadCoach (text) - The name of the team's head coach.
OffensiveCoordinator (text) - The name of the team's offensive coordinator.
DefensiveCoordinator (text) - The name of the team's defensive coordinator.
SpecialTeamsCoach (text) - The name of the team's special teams coach.
OffensiveScheme (text) - The offensive scheme used by the team.
DefensiveScheme (text) - The defensive scheme used by the team.
WikipediaWordMarkUrl (text) - The URL to the team's wordmark on Wikipedia.
UpcomingOpponent (text) - The name of the upcoming opponent.

"""
)

FuturesColumns = Prompt("Futures", "Columns",
"""
TeamID (double precision) - The unique ID of the team if the future is team-related.
BettingMarketTypeID (bigint) - The unique ID of the betting market type.
PlayerID (double precision) - The unique ID of the player if the future is player-related.
BettingPeriodTypeID (bigint) - The unique ID of the betting period type.
BettingEventID (bigint) - The unique ID of the betting event.
BettingBetTypeID (bigint) - The unique ID of the betting bet type.
AnyBetsAvailable (boolean) - Indicates if any bets are available.
BettingMarketID (bigint) - The unique ID of the betting market.
Updated (text) - The timestamp of the last update.
ConsensusOutcomes (text) - The consensus outcomes for the betting market.
BettingMarketType (text) - The type of the betting market. Could be ['Team Future', 'Player Future', 'Coach Future', 'Miscellaneous Future']
BettingBetType (text) - The type of the betting bet. - Could be 'NFL Championship Winner', 'AFC Champion', 'NFC Champion', 'MVP',
       'To Make the Playoffs', 'Win Total', 'Coach of the Year',
       'Offensive Player of the Year', 'Defensive Player of the Year',
       'AFC South Division Winner', 'AFC West Division Winner',
       'NFC East Division Winner', 'NFC North Division Winner',
       'AFC East Division Winner', 'NFC South Division Winner',
       'NFC West Division Winner', 'AFC North Division Winner',
       'Total Receiving Yards', 'Total Receiving Touchdowns',
       'Total Rushing Yards', 'Total Rushing Touchdowns',
       'AFC East Second Place', 'AFC East Third Place',
       'AFC East Fourth Place', 'AFC North Top 2 Finish',
       'AFC North Fourth Place', 'AFC North Second Place',
       'AFC North Third Place', 'AFC South Top 2 Finish',
       'AFC South Second Place', 'AFC South Third Place',
       'AFC South Fourth Place', 'AFC West Top 2 Finish',
       'AFC West Second Place', 'AFC West Third Place',
       'AFC West Fourth Place', 'NFC East Second Place',
       'NFC East Third Place', 'NFC East Fourth Place',
       'NFC East Top 2 Finish', 'AFC East Top 2 Finish',
       'NFC North Second Place', 'NFC North Third Place',
       'NFC North Fourth Place', 'NFC North Top 2 Finish',
       'NFC South Second Place', 'NFC South Third Place',
       'NFC South Fourth Place', 'NFC West Third Place',
       'NFC West Fourth Place', 'NFC West Top 2 Finish',
       'NFC West Second Place', 'NFC South Top 2 Finish',
       'Total Passing Yards', 'Total Passing Touchdowns', 'Total Sacks',
       'Most Passing Yards', 'Offensive Rookie of the Year',
       'Defensive Rookie of the Year', 'Any Team To Go 0-17',
       'Any Team To Go 17-0', 'Most Rookie Passing Yards',
       'Most Rookie Receiving Yards', 'Most Passing Touchdowns',
       'Most Receiving Yards', 'Most Rushing Yards',
       'Comeback Player of the Year', 'Best Record',
       'Lowest Scoring Team', 'Highest Scoring Team', 'AFC #1 Seed',
       'NFC #1 Seed', 'Last Winless Team', 'Last Team to Lose',
       'Team To Start 5-0', 'Team To Start 0-5',
       'Any Game to Finish in a Tie', 'To Win All 6 Division Games',
       'To Win All Home Games', 'To Win All Away Games',
       'To Lose All 6 Division Games', 'To Concede Most Points',
       'To Concede Least Points', 'To Lose All Home Games',
       'To Lose All Road Games', 'Most Rushing Touchdowns',
       'Most Receiving Touchdowns', 'Total Interceptions (DEF/ST)',
       'Least Wins', 'Most Wins', 'Team to Go 20-0 and Win Super Bowl',
       'Team to Go 17-0', 'Team to Go 0-17',
       'Most Tackles Leader (Solo & Assists)',
       'Most Interceptions Thrown', 'Sack Leader', 'Total Points',
       'Total Division Wins', 'Worst Record',
       'Most Quarterback Rushing Yards', 'NFC Wildcard Team',
       'AFC Wildcard Team', 'To Have 750+ Receiving Yards',
       'To Have 1250+ Receiving Yards', 'To Have 1000+ Receiving Yards',
       'Highest Rushing Yards Total', 'Longest Field Goal Made',
       'Highest Passing Yards Total', 'Highest Passing TD Total',
       'Highest Interceptions Thrown Total',
       'Highest Individual Receptions Total',
       'Highest Individual Sack Total',
       'Highest Individual FG Made Total', 'Highest Rushing TD Total',
       'Longest Reception', 'Longest Rush', 'Highest Receiving TD Total',
       'Highest Individual Passing Yards Game',
       'Highest Individual Defensive Interception Total',
       'Total Games To Go To Overtime',
       'Most Receiving Yards in Any Game',
       'Most Rushing Yards in Any Game', 'Total Receptions',
       'To Have 750+ Rushing Yards', 'To Have 1000+ Rushing Yards',
       'To Have 1250+ Rushing Yards',
       'Team To Score 1+ Touchdown in Every Game',
       'Most Kickoff Return Touchdowns', 'Interceptions Thrown',
       'Total Yards of Longest Touchdown', 'To Throw 35+ Touchdowns',
       'To Throw 30+ Touchdowns', 'To Have 10+ Receiving Touchdowns',
       'To Have 12+ Receiving Touchdowns', 'To Throw 40+ Touchdowns',
       'To Score 10+ Rushing Touchdowns',
       'To Have 6+ Receiving Touchdowns',
       'To Have 8+ Receiving Touchdowns', 'Most Rookie Rushing Yards',
       'Total Individual 200+ Receiving Yard Games',
       'Highest Receiving Yards Total',
       'Total Individual 200+ Rushing Yard Games',
       'Assistant Coach of the Year']
BettingPeriodType (text) - The period type for the bet. - ['NFL Championship Game', 'Regular Season - Including Playoffs', 'Regular Season']
TeamKey (text) - The key associated with the team if the future is team-related. The key is the abbreviation of the team, like SF for the San Francisco 49ers.
PlayerName (text) - The name of the player if the future is player-related.
Created (text) - The timestamp when the record was created. Looks like 2024-01-21T18:43:23	
"""
    
    )

FuturesOutcomesColumns = Prompt("FuturesOutcomes", "Columns",
"""
TeamID (double precision) - The unique ID of the team if the future is team-related.
PlayerID (double precision) - The unique ID of the player if the future is player-related.
GlobalTeamID (double precision) - The global ID of the team if the future is team-related.
IsInPlay (boolean) - Indicates if the event is currently in play.
PayoutDecimal (double precision) - The decimal value of the payout.
Value (double precision) - The value associated with the betting outcome.
BettingOutcomeID (bigint) - The unique ID of the betting outcome.
BettingOutcomeTypeID (double precision) - The unique ID of the betting outcome type.
IsAvailable (boolean) - Indicates if the betting outcome is available.
BettingMarketID (bigint) - The unique ID of the betting market.
PayoutAmerican (bigint) - The American-style payout value.
SportsBook (text) - The name of the sportsbook. Could be ['FanDuel', 'Caesars', 'Consensus', 'DraftKings', 'Fanatics','BetMGM']
BettingOutcomeType (text) - The type of the betting outcome.
Participant (text) - The team full name or player name. Example: 'New York Giants' or 'Saquon Barkley'
Created (text) - The timestamp when the record was created.
Updated (text) - The timestamp of the last update.
SportsbookMarketID (text) - The unique ID of the sportsbook market.
SportsbookOutcomeID (text) - The unique ID of the sportsbook outcome.
""")

class Columns:
    def __init__(self):
        self.TeamGameLog = TeamLogColumns
        self.PlayerGameLog = PlayerLogColumns
        self.PlayByPlay = PlayByPlayColumns
        self.BettingProps = BettingPropsColumns
        self.BettingOutcomes = BettingOutcomesColumns
        self.ByeWeek = ByeWeekColumns
        self.TeamInfo = TeamInfoColumns
        self.Futures = FuturesColumns
        self.FuturesOutcomes = FuturesOutcomesColumns

   