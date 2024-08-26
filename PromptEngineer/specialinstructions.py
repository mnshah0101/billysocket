from PromptEngineer.util import Prompt

# Create prompts

TeamLogInstructions = Prompt(
    'TeamGameLog',
    "SpecialInstructions",
    """
    The name of the table is `teamlog`.
    
    - Reference the `Team` column and the `HomeOrAway` column instead of `HomeTeam` and `AwayTeam`. The `Opponent` column will have the opposite side.
    - To calculate "Against the Spread" (ATS), determine whether a team has covered the point spread using the following formula:

    **Formula:**
    - Calculate the Cover Margin: `CoverMargin = (Score + PointSpread) - OpponentScore`
    - Determine ATS Result:
        - If `CoverMargin > 0`, the team covered the spread.
        - If `CoverMargin < 0`, the team did not cover the spread.
        - If `CoverMargin = 0`, it is a push (no winner against the spread).
    - A negative point spread means the team is favored to win, and a positive point spread means the team is the underdog.
    - To get the last game of a team, use `MAX(GameKey)`.

    **Note:**
    - All column names must be surrounded by double quotes, such as `"Name"` or `"Team"`.
    - There is no `weather` column, so use a combination of temperature, humidity, and wind speed to determine the weather conditions of the game.
    """
)

PlayerLogInstructions = Prompt(
    'PlayerGameLog',
    "SpecialInstructions",
    """
    The name of the table is `playerlog`.
    
    - Reference the `Team` column and the `HomeOrAway` column instead of `HomeTeam` and `AwayTeam`. The `Opponent` column will have the opposite side.
    - Infer player names from limited data. For example, if the user says "Kelce", infer "Travis Kelce".
    - To find games where two players have played against each other, join the table on the `GameKey` where the `Name` matches the player.
    - To calculate "Against the Spread" (ATS), use the following formula:

    **Formula:**
    - Calculate the Cover Margin: `CoverMargin = (Score + PointSpread) - OpponentScore`
    - Determine ATS Result:
        - If `CoverMargin > 0`, the team covered the spread.
        - If `CoverMargin < 0`, the team did not cover the spread.
        - If `CoverMargin = 0`, it is a push (no winner against the spread).
    - Use `MIN(GameKey)` to get the earliest game and `MAX(GameKey)` to get the latest game.

    **Additional Notes:**
    - Rookies have a value of `2` in the `Experience` column.
    - A player is injured if the `InjuryStatus` is `Doubtful`, `Out`, or `Questionable`.
    - Use the `DISTINCT` keyword when necessary to avoid duplicate data.
    - To see how many games a player missed, count the number of games where the `InjuryStatus` is 'Out', 'Doubtful', or 'Questionable'.
    - Be careful of periods in player names, e.g., "T.J. Watt" in the database.
    - Use a combination of temperature, humidity, and wind speed to determine the weather conditions, as there is no `weather` column.
    """
)

PlayByPlayInstructions = Prompt(
    'PlayByPlay',
    "SpecialInstructions",
    """
    The name of the table is `playbyplay`.

    - Columns to use for scoring plays: `Season`, `Week`, `HomeTeam`, `AwayTeam`, `Date`, and `GameKey`.
    - Use the `PlayTime` column for filtering all plays by date (format: `YYYY-MM-DDTHH:MM:SS` UTC).
    - Identify players by inferring full names from partial mentions (e.g., "Kelce" implies "Travis Kelce").
    - Use double quotes for column names, such as `"RushingYards"`.
    - Avoid using specific columns unless the play is a scoring play: `GameKey`, `SeasonType`, `ScoringPlayID`, `Season`, `Week`, `AwayTeam`, `HomeTeam`, `Date`, `Sequence_scoring`, `Team_scoring`, `Quarter`, `TimeRemaining`, `AwayScore`, `HomeScore`, `ScoreID`.
    - Use `DISTINCT` for `PlayID` to handle duplicate plays.
    - Calculate percentages using attempted and made columns (e.g., `ExtraPointsMade / ExtraPointsAttempted`).
    - To find WR1, look for the player with the most receiving yards in a season for a team.
    - Scoring plays only count touchdowns. For extra points, field goals, and safeties, use other columns to determine if it is a scoring play.
    - Since you don't have `GameKey`, use `Team` and `Date` to determine the game.

    **Instructions:**
    - Do not use `GameKey`, `SeasonType`, `ScoringPlayID`, `Season`, `Week`, `AwayTeam`, `HomeTeam`, `Date`, `Sequence_scoring`, `Team_scoring`, `Quarter`, `TimeRemaining`, `AwayScore`, `HomeScore`, or `ScoreID` in your query unless it is a scoring play.
    - In the slot means the direction is `Middle`.
    - If the question cannot be answered with the provided data, return: "Error: Cannot answer question with data provided."
    - For player names, if there is an apostrophe in the name, such as O'Shaughnessy, use the "" to surround the name, and use the single apostrophe in the query, such as "O'Shaughnessy".



    **Note:**
    - The database is a PostgreSQL database, and the data only goes back to the 2015 season.
    """
)

BettingPropsInstructions = Prompt(
    'BettingProps',
    "SpecialInstructions",
    """
    The name of the table is `bettingprops`.
    Be careful of the type of the columns, as some are integers, double precision and some are strings.
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
        

   
