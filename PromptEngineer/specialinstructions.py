from PromptEngineer.util import Prompt

# Create prompts

TeamLogInstructions = Prompt(
    'TeamGameLog',
    "SpecialInstructions",
    """
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

    """
)

PlayerLogInstructions = Prompt(
    'PlayerGameLog',
    "SpecialInstructions",
    """
    The name of the table is `playerlog`.
    
    The Team is always short hand, such as WAS for Washington or BAL for Baltimore.
    Instead of HomeTeam and AwayTeam, reference the Team column and the HomeOrAway Column, The Opponent column will have the opposite side.
    You will have to infer player names from little data from your understanding of the NFL. For example, if the user only says Kelce, you have to infer the name Travis Kelce
    To find games where two players have played against each other, you can join the table on the GameKey where the Name matches the player.
    To calculate "Against the Spread" (ATS), you need to determine whether a team has covered the point spread in a game. The formula for ATS can be derived using the team score, opponent score, and point spread as follows:


    Formula:
    Calculate the Cover Margin:
    Cover Margin=(Score+PointSpread)-OpponentScore
    Determine ATS Result:


    If Cover Margin > 0, the team covered the spread.
    If Cover Margin < 0, the team did not cover the spread.
    If Cover Margin = 0, it is a push (no winner against the spread).




    You can use MIN(GameKey) to get the earliest game and MAX(GameKey) to get the latest game.


    Remember, rookies have a value of 2 in the Experience column.


    A player is injured if the InjuryStatus is Doubtful, Out, or Questionable.


    Make sure to use the DISTINCT keyword when necessary to avoid duplicate data.


    Usually, even when a player is out or injured, they will have a record in the database. However, sometimes, they might not have a record. Therefore to see how many games a player missed, you can use 17 (or whatever number) - COUNT(DISTINCT GameKey where the player played).


    Be careful of periods in the player name. For example, TJ Watt is T.J. Watt in the database.


    To see how many games a played missed in the regular season, you can use 17 - COUNT(DISTINCT GameKey where the player played).
    Use this logic




    Only respond with the sql query, no explanation or anything else. Encompass the sql query with
    ```sql


    ```


    All columns must be surrounded by double quotes, such as "Name" or "Team".


    There is no weather column, so use a combination of temperature, humidity, and wind speed to determine the weather conditions of the game.



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




    Remember, do not use GameKey, SeasonType, ScoringPlayID, Season, Week, AwayTeam, HomeTeam, Date, Sequence_scoring, Team_scoring, Quarter, TimeRemaining, AwayScore, HomeScore, or ScoreID in your query unless it is a scoring play.


    All columns must be surrounded by double quotes, such as
    In the slot means the direction is Middle.


    If the question cannot be answered with the provided data, return: "Error: Cannot answer question with data provided."


    Respond only with the SQL query, enclosed in:


    ```sql
    <SQL_QUERY_HERE>
    ```

    Note: The database is a PostgreSQL database, and the data only goes back to the 2015 season.

    """
)

BettingPropsInstructions = Prompt(
    'BettingProps',
    "SpecialInstructions",
    """
    The name of the table is `bettingprops`.
    Be careful of the type of the columns, as some are integers, double precision and some are strings.
    The props are for the 2024 season, which is the upcoming season
        Use an available sportsbook, not just consensus lines.

    """
)

ByeWeekInstructions = Prompt(
    'ByeWeek',
    "SpecialInstructions",
    """
    The name of the table is `byeweeks`.
    The team is the abbreviation of the team name. For example 49ers is `SF`.
    """
)

BettingOutcomesInstructions = Prompt(
    'BettingOutcomes',
    "SpecialInstructions",
    """
    The name of the table is `outcomes`.
    Be careful of the type of the columns, as some are integers, double precision and some are strings.
    The outcomes map to a Betting Prop. 
    There is only data for the 2024 season, which is the upcoming season.
        Use an available sportsbook, not just consensus lines.

    """
)

TeamInfoInstructions = Prompt(
    'TeamInfo',
    "SpecialInstructions",
    """
    The name of the table is `teaminfo`.
    The team is the abbreviation of the team name. For example 49ers is `SF`.
    Use this table to find specific information about a team in a specific season, like who the coach is, what the offensive and defensive schemes are, and the team's salary.
    You can do things like join this table with the TeamGameLog table on a season and Team/Key to get more information about a team's performance.
    """
)

FuturesInstructions = Prompt(
    'Futures',
    "SpecialInstructions",
    """
    The name of the table is `futures`.
    Be careful of the type of the columns, as some are integers, double precision and some are strings.
    The futures are for the 2024 season, which is the upcoming season.
    Use the futures outcomes to determine the outcome/line/value of the bet.
        Use an available sportsbook, not just consensus lines.

    """
)

FuturesOutcomesInstructions = Prompt(
    'FuturesOutcomes',
    "SpecialInstructions",
    """
    The name of the table is `futuresoutcomes`.
    Be careful of the type of the columns, as some are integers, double precision and some are strings.
    The outcomes map to a Future. 
    There is only data for the 2024 season, which is the upcoming season.
    Use an available sportsbook, not just consensus lines.
    """
)

class SpecialInstructions:
    def __init__(self):
        self.TeamGameLog = TeamLogInstructions
        self.PlayerGameLog = PlayerLogInstructions
        self.PlayByPlay = PlayByPlayInstructions
        self.BettingProps = BettingPropsInstructions
        self.ByeWeek = ByeWeekInstructions
        self.BettingOutcomes = BettingOutcomesInstructions
        self.TeamInfo = TeamInfoInstructions
        self.Futures = FuturesInstructions
        self.FuturesOutcomes = FuturesOutcomesInstructions
        

   
