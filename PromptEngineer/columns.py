from PromptEngineer.util import Prompt


TeamLogColumns = Prompt("TeamGameLog", "Columns",
                        """
GameKey (BIGINT):
Date (TEXT): Format: 'YYYY-MM-DDTHH:MM:SS'. Remember, this is not a Date type, it is a TEXT type.
SeasonType (BIGINT): (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar). The default season type is 1.
Season (BIGINT): The default season is 2023.
Week (BIGINT): The week resets for each season type. The default week is 1. Week 17 is the last week of the regular season.
Team (TEXT):
Opponent (TEXT): The name of the opponent team.
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
HomeConference (TEXT): Can be AFC or NFC.
HomeDivision (TEXT): Can be North, East, West, South.
HomeFullName (TEXT):
HomeOffensiveScheme (TEXT): (3-4, 4-3).
HomeDefensiveScheme (TEXT): (PRO, 2TE, 3WR).
HomeCity (TEXT):
HomeStadiumDetails (TEXT): A map that looks like "'StadiumID': 3, 'Name': 'MetLife Stadium', 'City': 'East Rutherford', 'State': 'NJ', 'Country': 'USA', 'Capacity': 82500, 'PlayingSurface': 'Artificial', 'GeoLat': 40.813528, 'GeoLong': -74.074361, 'Type': 'Outdoor'".
HomeHeadCoach (TEXT):
AwayConference (TEXT): Can be AFC or NFC.
AwayDivision (TEXT): Can be North, South, East, or West.
AwayFullName (TEXT):
AwayOffensiveScheme (TEXT): (PRO, 2TE, 3WR).
AwayDefensiveScheme (TEXT): (3-4, 4-3).
AwayCity (TEXT):
AwayStadiumDetails (TEXT): A map that looks like "'StadiumID': 3, 'Name': 'MetLife Stadium', 'City': 'East Rutherford', 'State': 'NJ', 'Country': 'USA', 'Capacity': 82500, 'PlayingSurface': 'Artificial', 'GeoLat': 40.813528, 'GeoLong': -74.074361, 'Type': 'Outdoor'".
AwayHeadCoach (TEXT):
HomeOffensiveCoordinator (TEXT):
HomeDefensiveCoordinator (TEXT):
HomeSpecialTeamsCoach (TEXT):
AwayOffensiveCoordinator (TEXT):
AwayDefensiveCoordinator (TEXT):
AwaySpecialTeamsCoach (TEXT):
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
BettingMarketType (text)
BettingBetType (text) - Could be ['Total Points', 'Spread', 'Moneyline', 'Total Passing Yards', 'Total Rushing Yards', 'Total Receiving Yards', 'To Score a Touchdown', 'Player To Score Last Touchdown', 'To Score First Touchdown', 'To Score a D/ST Touchdown','Total Points Odd/Even', 'To Go To Overtime','First Team To Score', 'Total Rushing + Receiving TDs', 'Team To Score First Touchdown', 'Total Rushing & Receiving Yards', 'Total Field Goals Scored', 'Total Receptions', 'Race to 10 Points', 'Race To 20 Points', 'Race To 15 Points', 'Race To 25 Points', 'Moneyline (3-Way)', 'To Complete First Pass']
BettingPeriodType (text) - Could be ['Full Game', 'First Half', '1st Quarter', 'Regular Season']
PlayerName (text) - Player name if player prop or None
Created (text)
Updated (text)
AvailableSportsbooks (text) - Looks like [{{'SportsbookID': 8, 'Name': 'FanDuel'}}, {{'SportsbookID': 7, 'Name': 'DraftKings'}}, {{'SportsbookID': 22, 'Name': 'Consensus'}}, {{'SportsbookID': 24, 'Name': 'BetMGM'}}, {{'SportsbookID': 19, 'Name': 'Caesars'}}], which is an array of dictionaries, each containing the SportsbookID and its betting stats.
BettingOutcomes (text) - Looks like {{'BettingOutcomeID': 94547450, 'BettingMarketID': 470742, 'BettingOutcomeTypeID': 2, 'BettingOutcomeType': 'Away', 'PayoutAmerican': -105, 'PayoutDecimal': 1.9523809523809523, 'Value': 1.5, 'Participant': 'Green Bay Packers', 'IsAvailable': True, 'IsAlternate': False, 'Created': '2024-06-08T13:42:52', 'Updated': '2024-08-11T22:44:41', 'Unlisted': None, 'TeamID': 12, 'PlayerID': None, 'GlobalTeamID': 12, 'SportsbookUrl': 'https://sportsbook.fanduel.com/football/nfl/green-bay-packers-@-philadelphia-eagles-33181919', 'IsInPlay': False, 'SportsbookMarketID': '424043453', 'SportsbookOutcomeID': '50192', 'SportsBook': {{'SportsbookID': 8, 'Name': 'FanDuel'}}}}] - where each dictionary contains the BettingOutcomeID, BettingMarketID, BettingOutcomeTypeID, BettingOutcomeType, PayoutAmerican, PayoutDecimal, Value, Participant, IsAvailable, IsAlternate, Created, Updated, Unlisted, TeamID, PlayerID, GlobalTeamID, SportsbookUrl, IsInPlay, SportsbookMarketID, SportsbookOutcomeID, and SportsBook.
AvailableSportsbooksNames (text) - An array of the names of the available sportsbooks, like ['FanDuel', 'DraftKings', 'BetMGM', 'Caesars', 'Consensus']
Date (text)
AwayTeam (text)
HomeTeam (text)
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





class Columns:
    def __init__(self):
        self.TeamGameLog = TeamLogColumns
        self.PlayerGameLog = PlayerLogColumns
        self.PlayByPlay = PlayByPlayColumns
        self.BettingProps = BettingPropsColumns
        self.ByeWeek = ByeWeekColumns

   