from PromptEngineer.util import Table, Prompt, PromptEngineer

from PromptEngineer.columns import Columns
from PromptEngineer.specialinstructions import SpecialInstructions





Columns = Columns()
SpecialInstructions = SpecialInstructions()

#create tables

TeamGameLog = Table('TeamGameLog',
                    " This bucket is for questions that can be answered by looking at Team Game Logs in the NFL. This also includes information about  weather. This include against the spread stats.",
                    Columns.TeamGameLog,
                    SpecialInstructions.TeamGameLog)

PlayerGameLog = Table('PlayerGameLog',
                        "This bucket is for questions that can be answered by looking at individual Player Game Logs in the NFL. This includes information about player stats at a game level granularity. This is good for season based questions for players. You can also use this to compare player stats in the same game or over a stretch of games. You can also use this to see how a player performs against a certain team or player. This include against the spread stat for the games so this can be used to also see how player teams perform by score and spread. You can use this bucket to see if a player is a rookie or not. You can also use this for information about player injuries.",
                        Columns.PlayerGameLog,
                        SpecialInstructions.PlayerGameLog)


PlayByPlay = Table('PlayByPlay',
                   "This bucket is for questions that can be answered by looking at play by play data for the NFL. This is good for questions that require a more granular look at the game, such as what the score was at a certain point in the game or what the result of a specific play was. You can also use this to see how players perform in certain situations or against certain teams or players in a single game, some time period, or in some situation. Use this for player red zone stats. You can use this to calculate TD Drive rate.",
                     Columns.PlayByPlay,
                   SpecialInstructions.PlayByPlay)

ExpertAnalysis = Table('ExpertAnalysis',
                       "This bucket is for questions that require expert analysis or opinion. This is good for questions that require a more subjective answer, such as who the best player in the NFL is or what the best team in the NFL is. This is also good for questions that such as what the best strategy is for a team to win the Super Bowl, that cannot only be answered by stats. This can also provide real time analysis of games or players, or odds for future/current games. Predictions fall into this category. Use this bucket sparingly, as most questions can be answered with the data provided.",
                       '',
                       '')
Conversation = Table('Conversation',
                     "This bucket is if the user is just trying to have a conversation with Billy.",
                     '',
                     '')

BettingProps = Table('BettingProps',
                     'This bucket has information of betting props for the NFL 2024 season. This includes player props, game lines, and any props that have to do with the 2024 season, which is the upcoming season. Can use this for player props for game props.',
                     Columns.BettingProps,
                     SpecialInstructions.BettingProps)



ByeWeek = Table('ByeWeek',
                "This bucket is to figure out what week a team has a bye week.",
                Columns.ByeWeek,
                SpecialInstructions.ByeWeek)

Outcomes = Table('Outcomes',
                  "This bucket is to figure out the outcomes of betting props, including payouts, the lines, and the bet value. This is for the 2024 season, which is the upcoming season.",
                  Columns.BettingOutcomes,
                  SpecialInstructions.BettingOutcomes)
TeamInfo = Table('TeamInfo',
                 'This bucket is for team info such as team name, team abbreviation, team conference, information about coaches, offensive and defensive scheme, team salary and stadium details. Use this to find specific information about a team in a specific season.',
                 Columns.TeamInfo,
                 SpecialInstructions.TeamInfo)

Futures = Table('Futures',
                'This bucket is for futures bets for the 2024 season. This includes futures bets for the upcoming season, such as Super Bowl winner, MVP, Divison Winner and other futures bets. Always reference the futures outcomes table when you use this table as well to determine the outcome/line/value of the bet. When in doubt include both props and futures, if you are not sure which one to use.',
                Columns.Futures,
                SpecialInstructions.Futures)
FuturesOutcomes = Table('FuturesOutcomes',
                        'This bucket is to figure out the outcomes of futures bets, including payouts, the lines, and the bet value. This is for the 2024 season, which is the upcoming season.',
                        Columns.FuturesOutcomes,
                        SpecialInstructions.FuturesOutcomes)



Billy = PromptEngineer([TeamGameLog, PlayerGameLog, PlayByPlay, ExpertAnalysis, BettingProps, ByeWeek, Conversation, Outcomes, TeamInfo, Futures, FuturesOutcomes])
                   


