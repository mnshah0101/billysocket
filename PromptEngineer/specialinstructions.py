from PromptEngineer.util import Prompt


TeamLogInstructions = Prompt(
    'TeamGameLog',
    "SpecialInstructions",
    """
    The name of the table is teamlog.
    The team in the Team column isn't always the home team, it could be the away team, so use HomeOrAway to determine if the team is the home team or the away team. This is very important for determining who is what team in the game.
    Your response will be executed on a database of NFL Team Logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.
    A clever way to get the last game of a team is to do MAX(GameKey), which will give you the last game of the team.
    All columns must be surrounded by double quotes, such as "Name" or "Team".
    To calculate record, use WinsAfter for record after the game and Wins for record before the game. The same goes for losses.
    The games are doubled counted in the TeamLog, so you will have to use DISTINCT to get the unique games for a team. They are double counted in that in one occurrence the home team is the Team and away the Opponent and in the other occurrence the away team is the Team and the home team is the Opponent. You can do this with SELECT DISTINCT ON ("GameKey")
    There is no weather column, so use a combination of temperature, humidity, and wind speed to determine the weather conditions of the game.
    
    """
)

PlayerLogInstructions = Prompt(
    'PlayerGameLog',
    "SpecialInstructions",
    """
    The name of the table is `playerlog`.
    - Instead of HomeTeam and AwayTeam, reference the Team column and the HomeOrAway Column, The Opponent column will have the opposite side.
    - You will have to infer player names from little data from your understanding of the NFL. For example, if the user only says Kelce, you have to infer the name Travis Kelce
    - To find games where two players have played against each other, you can join the table on the GameKey where the Name matches the player.
    - You can use MIN(GameKey) to get the earliest game and MAX(GameKey) to get the latest game.
    - Remember, rookies have a value of 2 in the Experience column.
    - A player is injured if the InjuryStatus is Doubtful, Out, or Questionable.
    - Usually, even when a player is out or injured, they will have a record in the database. However, sometimes, they might not have a record. Therefore to see how many games a player missed, you can use 17 (or whatever number) - COUNT(DISTINCT GameKey where the player played).
    - Be careful of periods in the player name. For example, TJ Watt is T.J. Watt in the database.
    - If asked for ranking, make sure you rank everyone in that position by the criteria given and then output the rank of the player for that criteria. This is important.
    - You can never not include the player name in the SQL query - doing so would be catastrophic.
    - All columns must be surrounded by double quotes, such as "Name" or "Team".
    - There is no weather column, so use a combination of temperature, humidity, and wind speed to determine the weather conditions of the game.
    - When asking about a player, assume that we want logs where the player has played, unless the question specifies otherwise like for injuries or missed games.
    - Your response will be executed on a database of NFL Player Logs and the answer will be returned to the User, so make sure the query is correct and will return the correct information.
     -You may have to use the "like" operator to match player names, as the user may not provide the full name of the player or the database may have a different format for the player name.

    """
)

PlayByPlayInstructions = Prompt(
    'PlayByPlay',
    "SpecialInstructions",
    """
    - Use the table `playbyplay`.
    - Columns to use for scoring plays: Season, Week, HomeTeam, AwayTeam, Date, and GameKey.
    - Use the `PlayTime` column for filtering all plays by date (format: `YYYY-MM-DDTHH:MM:SS` UTC).
    - Identify players by inferring full names from partial mentions (e.g., "Kelce" implies "Travis Kelce").
    - Use double quotes for column names (e.g., `"RushingYards"`).
    - Avoid using specific columns unless the play is a scoring play: GameKey, SeasonType, ScoringPlayID, Season, Week, AwayTeam, HomeTeam, Date, Sequence_scoring, Team_scoring, Quarter, TimeRemaining, AwayScore, HomeScore, ScoreID.
    - Use `DISTINCT` for `PlayID` to handle duplicate plays.
    - Calculate percentages using attempted and made columns (e.g., `ExtraPointsMade` / `ExtraPointsAttempted`).
    - A way to get WR1 is to look for the player with the most receiving yards in a season for a team.
    - The Season, Week, HomeTeam, AwayTeam, Date, and GameKey columns are only available for scoring plays.
    - To filter the data for all plays by date, you can use the PlayTime column. The PlayTime column is in the format of 2022-09-11T22:21:49 and is in UTC time.
    - Scoring plays only count touchdowns, so for extra points, field goals, and safeties you must use other columns to determine if it is a scoring play.
    - Since you don't have GameKey, you can use Team, nd Date to determine the game.
    - Remember, do not use GameKey, SeasonType, ScoringPlayID, Season, Week, AwayTeam, HomeTeam, Date, Sequence_scoring, Team_scoring, Quarter, TimeRemaining, AwayScore, HomeScore, or ScoreID in your query unless it is a scoring play.
    - In the slot means the direction is Middle.
    Note: The database is a PostgreSQL database, and the data only goes back to the 2015 season.

    """
)

BettingPropsInstructions = Prompt(
    'Props',
    "SpecialInstructions",
    """
    The name of the table is `props`.
    Be careful of the type of the columns, as some are integers, double precision and some are strings.
    The props are for the 2024 season, which is the upcoming season
    Use an available sportsbook, not just consensus lines. Contains prop bets for upcoming games and past games.

    There will only be a player name if the question is about a player, and a team name will only be non-null if the question is about the team. All props data is for 2024 only.
    You must list all the sportsbooks (Draftkings, FanDuel, etc) and corresponding sportsbook urls for all the stats you are providing. 

    When asking for multiple props, only provide at most 3 interesting props. When being asked to decide which props are the most popular, use your intuition to decide which ones most seem popular. 
    For game days, you can use the Day column, if you don't have the time of the game. Make sure your date format is consistent with the data. You can use this to also get Day of the week, with the EXTRACT(DOW FROM "Date") function.
    Your response will be executed on a database of NFL Betting Prompts and the answer will be returned to the User, so make sure the query is correct and will return the correct information.
    The default SeasonType is Regular Season or 1. If the question is about a different SeasonType, please specify in the query. The default season is 2024.
    For BettingBetType, do not query on this column unless the user specifically asks for the prop type, like "Give me props for Kirk Cousins total yards" since there is no way to know if the database has the prop type you are looking for. However, for just "Give me props for Kirk Cousins", you can query on the player name and not the prop type.

    """
)





FuturesInstructions = Prompt(
    'Futures',
    "SpecialInstructions",
    """
  The name of the table is futurestable. 

    There will only be a player name if the question is about a player, and a team name will only be non-null if the question is about the team. All futures data is for 2024 only.
    You must list all the sportsbooks (Draftkings, FanDuel, etc) and corresponding sportsbook urls for all the stats you are providing.
    Do not make things more specific than they should be. For example, no need to give the restriction of BettingMarketType if it is not needed.
    Your response will be executed on a database of NFL Betting Futures and the answer will be returned to the User, so make sure the query is correct and will return the correct information.
    """
)



class SpecialInstructions:
    def __init__(self):
        self.TeamGameLog = TeamLogInstructions
        self.PlayerGameLog = PlayerLogInstructions
        self.PlayByPlay = PlayByPlayInstructions
        self.Props = BettingPropsInstructions
        self.Futures = FuturesInstructions
        

   
