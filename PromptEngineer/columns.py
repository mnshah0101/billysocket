from PromptEngineer.util import Prompt


TeamLogColumns = Prompt("TeamGameLog", "Columns",
                        """
GameKey (BIGINT): 
Date (TEXT): Format: 'YYYY-MM-DDTHH:MM:SS'. Remember, this is not a Date type, it is a TEXT type.
SeasonType (BIGINT): (1=Regular Season, 2=Preseason, 3=Postseason, 4=Offseason, 5=AllStar). The default season type is 1.
Season (BIGINT): The default season is 2024.
Week (BIGINT): The week resets for each season type. The default week is 1. Week 17 is the last week of the regular season.
Team (TEXT): Represents the team name with shorthand, e.g. 'KC' for Kansas City Chiefs.
Opponent (TEXT): The name of the opponent team. This is the team that the team played against. The opponent team name is represented with shorthand, e.g. 'KC' for Kansas City Chiefs.
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
TeamName (TEXT): The full name of the team (e.g. New England Patriots)
DayOfWeek (TEXT): The day of the week this game was played on (e.g. Sunday, Monday)
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
HomeConference (TEXT): Can be AFC or NFC.
HomeDivision (TEXT): Can be North, East, West, South.
HomeFullName (TEXT):
HomeOffensiveScheme (TEXT): (3-4, 4-3).
HomeDefensiveScheme (TEXT): (PRO, 2TE, 3WR).
HomeCity (TEXT):
HomeStadiumDetails (TEXT): A map that looks like "{'StadiumID': 3, 'Name': 'MetLife Stadium', 'City': 'East Rutherford', 'State': 'NJ', 'Country': 'USA', 'Capacity': 82500, 'PlayingSurface': 'Artificial', 'GeoLat': 40.813528, 'GeoLong': -74.074361, 'Type': 'Outdoor'}".
TeamCoach (TEXT):
OpponentCoach (TEXT):
AwayConference (TEXT): Can be AFC or NFC.
AwayDivision (TEXT): Can be North, South, East, or West.
AwayFullName (TEXT):
AwayOffensiveScheme (TEXT): (PRO, 2TE, 3WR).
AwayDefensiveScheme (TEXT): (3-4, 4-3).
AwayCity (TEXT):
Wins (BIGINT): These are the wins up to the current game. They reset each season and each season type.
Losses (BIGINT): These are the losses up to the current game. They reset each season and each season type.
OpponentWins (BIGINT): These are the opponent's wins up to the current game. They reset each season and each season type.
OpponentLosses (BIGINT): These are the opponent's losses up to the current game. They reset each season and each season type.
Wins_After (BIGINT): These are the wins after the current game. They reset each season and each season type.
Losses_After (BIGINT): These are the losses after the current game. They reset each season and each season type.
OpponentWins_After (BIGINT): These are the opponent's wins after the current game. They reset each season and each season type.
OpponentLosses_After (BIGINT): These are the opponent's losses after the current game. They reset each season and each season type.
StadiumID (BIGINT):
Stadium (TEXT): Where the game was played. Games in London were played in Wembley Stadium or Tottenham Hotspur Stadium.
Name (TEXT): Home team stadium name. If not foreign game, it will be where the game was played.
City (TEXT): Home team city.
State (TEXT): Home team state.
Country (TEXT): Home team country.
Capacity (BIGINT): Home team stadium capacity.
PlayingSurface (TEXT): Home team stadium playing surface.
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
Team (text) - Represents the team name with shorthand, e.g. 'KC' for Kansas City Chiefs.
Opponent (text) - The name of the opponent team. This is the team that the team played against. The opponent team name is represented with shorthand, e.g. 'KC' for Kansas City Chiefs.
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
Day (TEXT): This looks like 2024-10-03T00:00:00, and can be used when you don't know the exact game time. You can extract the day of the week from this, and use it to determine the game day.
DateTime (text)
GlobalGameID (bigint)
GlobalTeamID (bigint)
GlobalOpponentID (bigint)
ScoreID (bigint)
FantasyPointsFantasyDraft (double precision)
OffensiveFumbleRecoveryTouchdowns (double precision)
SnapCountsConfirmed (bigint)
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
Experience (double precision) - The number of years the player has played in the NFL. Since it is updated every spring, rookies in the 2024 season have a value of 2.
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
Updated (text)
Created (text)
Team (text) - Shorthand for the team, e.g. 'KC' for Kansas City Chiefs
Opponent (text) - Shorthand for the opponent team, e.g. 'KC' for Kansas City Chiefs
Down (bigint) - Which down it is (1, 2, 3, 4)
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
                             This table is called 'props'
                             GlobalHomeTeamID(bigint)
                             PointSpreadAwayTeamMoneyLine(bigint)
                             PointSpreadHomeTeamMoneyLine(bigint)
                             ScoreID(bigint) - Unique identifier for the game score
                             Week(bigint) - The week number of the game in the season
                             OverPayout(bigint) - Payout for betting over the total points
                             UnderPayout(bigint) - Payout for betting under the total points
                             PlayerID(double precision) - Unique identifier for a player
                             BettingOutcomeID(double precision) - Unique identifier for a specific betting outcome
                             BettingEventID(bigint) - Unique identifier for a betting event
                             PayoutAmerican(double precision) - Payout in American odds format
                             Value(double precision) - The betting line or total for props
                             TeamID(double precision) - Unique identifier for a team
                             GlobalTeamID(double precision) - Unique identifier for a team across all leagues/sports
                             BettingPeriodTypeID(bigint) - Identifier for the betting period(e.g., full game, first half)
                             BettingMarketID(bigint) - Unique identifier for a betting market
                             PointSpread(double precision) - The point spread for the game
                             OverUnder(double precision) - The over/under total for the game
                             GameKey(bigint) - Unique identifier for the game
                             AwayTeamMoneyLine(bigint) - Money line for betting on the away team to win outright
                             HomeTeamMoneyLine(bigint) - Money line for betting on the home team to win outright
                             SeasonType(bigint) - Type of season(e.g., 1 for regular season, 2 for playoffs)
                             Season(bigint) - The year of the season
                             GlobalGameID(bigint) - Unique identifier for the game across all leagues/sports
                             GlobalAwayTeamID(bigint) - Unique identifier for the away team across all leagues/sports
                             SportsBook(text) - Name of the sportsbook offering the odds Could be['BetMGM', 'Caesars', 'FanDuel', 'Consensus', 'DraftKings', nan]
                             BettingMarketType(text) - Could be['Game Line', 'Player Prop', 'Team Prop', 'Game Prop']
                             BettingBetType(text) - Don't query on this unless it is asking specifically for that type of bet because there is no way to tell beforehand what kind of bet each player will have. For asking for general props, just leave the query on this column out.
                             ['Total Points', 'Spread', 'Moneyline', 'Total Passing Yards',
                                                             'Total Rushing Yards', 'Total Receiving Yards',
                                                             'To Score First Touchdown', 'To Score a Touchdown',
                                                             'To Score a D/ST Touchdown', 'To Score 2+ Touchdowns',
                                                             'To Score 2+ D/ST Touchdowns', 'Total Field Goals Scored',
                                                             'Total Passing Touchdowns', 'Total Rushing + Receiving TDs',
                                                             'Interceptions Thrown', 'Total Fumbles Lost',
                                                             'Total Passing + Rushing Yards', 'Total Rushing & Receiving Yards',
                                                             'Extra Points Made', 'Total Kicking Points',
                                                             'Total Interceptions (DEF/ST)', 'Total Tackles (Solo)',
                                                             'Total Assists', 'Total Tackles (Solo & Assists)',
                                                             'Total Passing Attempts', 'Total Pass Completions',
                                                             'Total Receiving Touchdowns', 'Total Rushing Touchdowns',
                                                             'Longest Reception', 'Player To Score Last Touchdown',
                                                             'Longest Pass', 'To Score 3+ Touchdowns', 'Total Touchdowns',
                                                             'Moneyline (3-Way)', 'Both Teams to Score on Their 1st Drive',
                                                             'Both teams to score 1+ TD in each half', 'Total Points Odd/Even',
                                                             'Race To 20 Points', 'Race To 15 Points', 'Race To 5 Points',
                                                             'To Go To Overtime', 'Both Teams to Scor e 25 Points',
                                                             'Race to 10 Points', 'Both Teams to Score 40 Points',
                                                             'To Score First and Win', 'Both teams to score 3+ TD in each half',
                                                             'Both Teams to Score', 'Both Teams to Score 10 Points',
                                                             'Both Teams to Score 30 Points', 'Both Teams to Score 20 Points',
                                                             'Both Teams to Score 35 Points', 'Last Team To Score',
                                                             'First Team To Score', 'Both teams to score 2+ TD in each half',
                                                             'Both teams to score 4+ TD in each half',
                                                             'To Score First and Lose', 'Race To 25 Points',
                                                             'To Score First Field Goal', 'Both Teams to Score 15 Points',
                                                             'Race To 30 Points', 'Longest Rush',
                                                             'To Score A Defensive Touchdown',
                                                             'To Score 2+ Defensive Touchdowns',
                                                             'Team To Score First Touchdown',
                                                             'Either Team To Score 3 Unanswered Times',
                                                             'A Score In Final Two Minutes', 'To Record A Safety',
                                                             'First Team To Call Timeout', 'To Attempt an Onside Kick',
                                                             'Punt Returned For Touchdown', 'Punt To Be Blocked',
                                                             'Field Goal To Be Blocked', 'Both Teams To Score A Touchdown',
                                                             'Both Teams To Score 2+ Touchdowns',
                                                             'Both Teams To Score 3+ Touchdowns',
                                                             'Both Teams To Score 3+ Points', 'Both Teams To Score 7+ Points',
                                                             'First Team to Use Coach Challenge', 'Total Sacks',
                                                             'Total Receptions', 'To Record Successful Two Point Conversion',
                                                             'To Attempt 2-Point Conversion',
                                                             'Total Pass + Rush + Rec Touchdowns',
                                                             'Punt Downed Inside The 5-yard line', 'Total Rushing Attempts',
                                                             'To Complete First Pass']
                             BettingPeriodType(text) - Could be['Full Game', '1st Quarter', '3rd Quarter', '4th Quarter', '2nd Quarter', 'First Half', 'Second Half', 'Regular Season']
                             PlayerName(text) - If it is a player prop this will be the name of the player for player props, format is first name last name, ex: 'Jordan Love'
                             AwayTeam(text) - Name of the away team in short form, like the San Francisco 49ers are SF
                             HomeTeam(text) - Name of the home team in short form, like the San Francisco 49ers are SF
                             Channel(text) - Name of network provider, could be['PEA', 'NBC', 'FOX', 'CBS', 'ABC', 'ESPN', 'AMZN', 'NFLN', 'NFLX', nan]
                             QuarterDescription(text) - Description of the current quarter or game state
                             Day(text) - Day of the week for the game, formatted like 2024-09-06T00: 00: 00. You can use this when you don't know game time.
                             DateTime(text) - Datetime of the game, formatted like 2024-09-06T20: 15: 00. You can use this when you know the exact starting game time.
                             DateTimeUTC(text) - Datetime of the game in UTC, formatted like 2024-09-07T00: 15: 00. You can use this when you know the exact starting game time.
                             BettingOutcomeType(text) - Could be['Over', 'Under', 'Away', 'Home', nan, 'Yes', 'Draw', 'No', 'Odd',
                              'Even', 'Neither']
                             SportsbookUrl(text) - URL to the sportsbook's page for this game or bet
                             BetPercentage(double precision) - Percentage of bets on this outcome, a lot of these are NaN, but some are not
                             MoneyPercentage(double precision) - Percentage of money on this outcome, a lot of these are NaN, but some are not
                             """)







FuturesColumns = Prompt("Futures", "Columns",
                        """
PlayerID (double precision) - If this is a player future, this is the unique identifier for the player
BettingOutcomeID (bigint)
BettingMarketID (bigint)
PayoutAmerican (bigint) - This is the payout in American odds format
GlobalTeamID (double precision) - This is the unique identifier for a team if it is a team future
BettingEventID (bigint) 
BettingOutcomeType (text) - Can be [nan, 'No', 'Yes', 'Under', 'Over']
SportsbookUrl (text) - This is the url for the sportsbook
SportsBook (text) - This can be ['FanDuel', 'Caesars', 'Consensus', 'BetMGM', 'Fanatics', 'DraftKings']
BettingMarketType (text) - Can be ['Team Future', 'Player Future', 'Coach Future',
       'Miscellaneous Future']
BettingBetType (text)- ['NFL Championship Winner', 'AFC Champion', 'NFC Champion', 'MVP',
       'To Make the Playoffs', 'Win Total', 'Coach of the Year',
       'Offensive Player of the Year', 'Defensive Player of the Year',
       'AFC South Division Winner', 'AFC West Division Winner',
       'NFC East Division Winner', 'NFC North Division Winner',
       'AFC East Division Winner', 'NFC South Division Winner',
       'NFC West Division Winner', 'AFC North Division Winner',
       'Total Receiving Yards', 'Total Receiving Touchdowns',
       'Total Rushing Yards', 'Total Rushing Touchdowns',
       'AFC East Second Place', 'AFC East Third Place',
       'AFC East Fourth Place', 'AFC North Fourth Place',
       'AFC North Second Place', 'AFC North Third Place',
       'AFC South Second Place', 'AFC South Third Place',
       'AFC South Fourth Place', 'AFC West Top 2 Finish',
       'AFC West Second Place', 'AFC West Third Place',
       'AFC West Fourth Place', 'NFC East Second Place',
       'NFC East Third Place', 'NFC East Fourth Place',
       'NFC East Top 2 Finish', 'AFC East Top 2 Finish',
       'NFC North Second Place', 'NFC North Third Place',
       'NFC North Fourth Place', 'NFC South Second Place',
       'NFC South Third Place', 'NFC South Fourth Place',
       'NFC West Third Place', 'NFC West Fourth Place',
       'NFC West Top 2 Finish', 'NFC West Second Place',
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
       'Total Division Wins', 'Worst Record', 'Receptions Leader',
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
       'Highest Receiving Yards Total', 'Assistant Coach of the Year',
       'To Be Named AP First Team All-Pro DE',
       'To Be Named AP First Team All-Pro DL',
       'To Be Named AP First Team All-Pro LB',
       'To Be Named AP First Team All-Pro TE',
       'To Be Named AP First Team All-Pro LG',
       'To Be Named AP First Team All-Pro LT',
       'To Be Named AP First Team All-Pro RB',
       'To Be Named AP First Team All-Pro RG',
       'To Be Named AP First Team All-Pro C',
       'To Be Named AP First Team All-Pro RT',
       'To Be Named AP First Team All-Pro CB',
       'To Be Named AP First Team All-Pro WR',
       'To Be Named AP First Team All-Pro QB',
       'To Be Named AP First Team All-Pro S',
       'To Be Named AP First Team All-Pro K',
       'To Be Named AP First Team All-Pro P']
BettingPeriodType (text) -Can be['NFL Championship Game', 'Regular Season - Including Playoffs',
       'Regular Season']
TeamKey (text) -  If it a team future, this will have the short form of the team, for example the 49ers are SF.
PlayerName (text) - If it is a player future, this will be the name of the player
Created (text) - Timestamp of when the record was created, looks like  looks like 2024-09-07T00:15:00
Updated (text) - Timestamp of when the record was last updated, looks like  looks like 2024-09-07T00:15:00

"""
    
    )



class Columns:
    def __init__(self):
        self.TeamGameLog = TeamLogColumns
        self.PlayerGameLog = PlayerLogColumns
        self.PlayByPlay = PlayByPlayColumns
        self.Props = BettingPropsColumns
        self.Futures = FuturesColumns

   