from datetime import datetime, timedelta
import json
import time
from uuid import UUID
import dotenv
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import scheduleleaguev2, leaguestandingsv3
from strands import tool
from strands.models.bedrock import BedrockModel
from strands.session.file_session_manager import FileSessionManager
import boto3
from strands import Agent
import pandas as pd

dotenv.load_dotenv()

@tool
def get_nba_live_scores(name:str):
    """Get today's NBA live scores for a given team. 
        This tool doesn't provide past scores.
        Args:
            name (str): team name or city of the NBA team.
        """
    # Today's Score Board
    games = scoreboard.ScoreBoard()
    games_json = json.loads(games.get_json())
    name = name.lower()
    scores = []
    for game in games_json['scoreboard']['games']:
        home_team = game['homeTeam']['teamName'].lower()
        away_team = game['awayTeam']['teamName'].lower()
        if name in [home_team, away_team]:
            scores.append({
                'home_team': game['homeTeam']['teamName'],
                'home_score': game['homeTeam']['score'],
                'away_team': game['awayTeam']['teamName'],
                'away_score': game['awayTeam']['score'],
                'quarter': game['period'],
                'time_remaining': game['gameClock']
            })
            break
    if not scores:
        return f"No games found for team: {name}"
    return scores

@tool
def get_nba_past_scores(name:str, game_date:str):
    """Get past NBA scores for a given team for a specific date (MM/DD/YYYY).
      Use 'today' or 'yesterday' for convenience.
      Args:
          name (str): team name or city of the NBA team.
      """
    if game_date.lower() == "today":
        date = datetime.now().strftime("%m/%d/%Y")
    elif game_date.lower() in ["yesterday", "yday", "prev day", "y'day"]:
        date = (datetime.now() - timedelta(days=1)).strftime("%m/%d/%Y")
    else:
        try:
            date_obj = datetime.strptime(game_date, "%m/%d/%Y")
            date = date_obj.strftime("%m/%d/%Y")
        except ValueError:
            return "Please provide the date in 'MM/DD/YYYY' format or use 'today'/'yesterday'."
    schedule = scheduleleaguev2.ScheduleLeagueV2()
    json_schedule = json.loads(schedule.get_json())
    games = json_schedule['leagueSchedule']['gameDates']
    past_scores = []
    for day_games in games:
        if day_games['gameDate'].startswith(date):
            for game in day_games['games']:
                if name.lower() in [
                        game['homeTeam']['teamName'].lower(),
                        game['homeTeam']['teamCity'].lower(),
                        game['awayTeam']['teamName'].lower(),
                        game['awayTeam']['teamCity'].lower()
                    ]:
                    past_scores.append({
                        'home_team': game['homeTeam']['teamName'],
                        'home_score': game['homeTeam']['score'],
                        'away_team': game['awayTeam']['teamName'],
                        'away_score': game['awayTeam']['score']
                    })
                    break
    if not past_scores:
        if game_date.lower() == "today":
            return f"Also check live scores tool. No past games found for team: {name} today."
        return f"No past games found for team: {name} on date: {date}"
    return past_scores

@tool
def get_team_standings(name:str):
    """Get standings/ranking for a given team.
    
    Args:
        name (str): team name or city of the NBA team.
    """
    standings = leaguestandingsv3.LeagueStandingsV3()
    json_standings = json.loads(standings.get_json())
    df = pd.DataFrame(json_standings['resultSets'][0]['rowSet'], 
                    columns=json_standings['resultSets'][0]['headers'])
    team_status = None
    for index, row in df.iterrows():
        if row['TeamName'].lower() == name.lower() or row['TeamCity'].lower() == name.lower():
            team_status = {
                'Rank': row['PlayoffRank'],
                'Record': row['Record'],
                'Conference': row['Conference']
            }
            break
    if team_status is None:
        return f"No standings found for team: {name}"
    return team_status

def setup_agents() -> Agent:
    boto_session = boto3.Session()
    claud_on_bedrock = BedrockModel(boto_session=boto_session, streaming=False)
    # Create a session manager with a unique session ID
    session_manager = FileSessionManager(session_id=str(UUID(int=time.time_ns())))

    nba_score_agent = \
        Agent(name="Nba Score Agent", model=claud_on_bedrock,
            system_prompt= """You are an agent who provides NBA scores 
            and standings for the given team. Look at the tool output and
            anwer the user query only from that output.
            Be very concise and to the point.
            If anything other than NBA scores or standings is asked, 
            respond with 'I can only provide NBA scores and standings.'.
            When providing live scores use following format:
                'Team A is playing against Team B with current score X-Y.'
                If no games found, just say 'I didn't find any game for the team'
            When providing response to game status use following format:
                'Team A won/lost against Team B with score X-Y.'
                If no games found, just say 'I didn't find any game for the team'
            When providing team status or standings use following format:
                'Team A is currently ranked X in the CONFERENCE with a record of W-L.'
        """,
            tools = [get_nba_live_scores, get_nba_past_scores, get_team_standings],
            description="NBA scores agent", callback_handler=None,
            session_manager=session_manager
        )
    return nba_score_agent

def get_scores(message: str):
    travel_agent = setup_agents()
    response = travel_agent(message)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    nba_agent = setup_agents()
    while True:
        try:
            user_request = input("\nHey, got a question on NBA scores or standings? ")
        except EOFError:
            user_request = "exit"
        if user_request.lower() in ["exit", "quit", ""]:
            print("Exiting the NBA scores agent. Goodbye!")
            break
        response = nba_agent(prompt=user_request)
        print(response.message['content'][0]['text'])
