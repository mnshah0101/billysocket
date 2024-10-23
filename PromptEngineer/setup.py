from PromptEngineer.util import Table, Prompt, PromptEngineer

from PromptEngineer.columns import Columns
from PromptEngineer.specialinstructions import SpecialInstructions





Columns = Columns()
SpecialInstructions = SpecialInstructions()

#create tables

TeamGameLog = Table('TeamGameLog',"This bucket is for questions that can be answered by looking at Team Game Logs in the NFL. This also includes information about coaches and weather. This include against the spread stats.",

                    Columns.TeamGameLog,
                    SpecialInstructions.TeamGameLog)

PlayerGameLog = Table('PlayerGameLog',
                      "This bucket is for questions that can be answered by looking at individual Player Game Logs in the NFL. This includes information about player stats at a game level granularity. This is good for season based questions for players. You can also use this to compare player stats in the same game or over a stretch of games. You can also use this to see how a player performs against a certain team or player. This include against the spread stat for the games so this can be used to also see how player teams perform by score and spread. You can use this bucket to see if a player is a rookie or not . You can also use this for information about player injuries.",
                        Columns.PlayerGameLog,
                        SpecialInstructions.PlayerGameLog)


PlayByPlay = Table('PlayByPlay',
                   "This bucket is for questions that can be answered by looking at play by play data for the NFL. This is good for questions that require a more granular look at the game, such as what the score was at a certain point in the game or what the result of a specific play was. You can also use this to see how players perform in certain situations or against certain teams or players in a single game, some time period, or in some situation. Use this for player red zone stats.",
                     Columns.PlayByPlay,
                   SpecialInstructions.PlayByPlay)


Futures = Table('Futures',
                "This bucket is for questions that can be answered by looking at futures data for teams or players. This is good if the user inquires about futures information for a specific player or team this upcoming season.",
                Columns.Futures,
                SpecialInstructions.Futures)
Props = Table('Props',
              'This bucket is for questions that can be answered by looking at betting props for teams or players. This is good if the user inquires about betting information for a specific player or team this upcoming season.',
              Columns.Props,
              SpecialInstructions.Props)


ExpertAnalysis = Table('ExpertAnalysis',
                       "This bucket is for questions that require expert analysis or opinion. This is good for questions that require a more subjective answer, such as who the best player in the NFL is or what the best team in the NFL is . This is also good for questions that require a more in -depth analysis, such as what the best strategy is for a team to win the Super Bowl. This can also provide real time analysis of games or players, or odds for future/current games. This tool is also good for non-betting related questions about upcoming games or games that have not happened yet.",
                       '',
                       '')
Conversation = Table('Conversation',
                     "This bucket is if the user is just trying to have a conversation with Billy. ",
                     '',
                     '')




Billy = PromptEngineer([TeamGameLog, PlayerGameLog, PlayByPlay, Futures, Props, ExpertAnalysis, Conversation])
                   


