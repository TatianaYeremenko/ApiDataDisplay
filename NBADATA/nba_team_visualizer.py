#!/usr/bin/env python3
"""
NBA Team Game Results Visualizer with HTML Output
Uses real NBA data for all teams with balanced home/away comparison
"""

from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import teams
from datetime import datetime, timedelta
import pandas as pd
import webbrowser
import os
import json
import time

# CHANGE THIS VARIABLE TO VIEW DIFFERENT TEAMS
team_name = "Golden State Warriors"

def get_team_games(team_name, show_progress=True):
    """
    Get game results for any NBA team from the last 6 months
    """
    try:
        # Get team ID
        team_matches = teams.find_teams_by_full_name(team_name)
        if not team_matches:
            if show_progress:
                print(f"Team '{team_name}' not found. Skipping...")
            return None
            
        team_info = team_matches[0]
        team_id = team_info['id']
        
        # Calculate date 6 months ago
        six_months_ago = datetime.now() - timedelta(days=180)
        season = "2024-25"
        
        if show_progress:
            print(f"Fetching data for {team_name}...")
        
        # Get team game log
        gamelog = teamgamelog.TeamGameLog(
            team_id=team_id,
            season=season,
            season_type_all_star='Regular Season'
        )
        
        # Get games data
        games_df = gamelog.get_data_frames()[0]
        
        if games_df.empty:
            if show_progress:
                print(f"No games found for {team_name} in {season} season")
            return None
        
        # Convert GAME_DATE to datetime
        try:
            games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])
        except:
            games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'], format='%Y-%m-%d')
        
        # Filter games from last 6 months
        recent_games = games_df[games_df['GAME_DATE'] >= six_months_ago]
        
        if recent_games.empty:
            if show_progress:
                print(f"No recent games found for {team_name} in the last 6 months")
            return None
        
        # Sort by date (most recent first)
        recent_games = recent_games.sort_values('GAME_DATE', ascending=False)
        
        if show_progress:
            # Calculate home/away records for display
            home_games = recent_games[recent_games['MATCHUP'].str.contains('vs', na=False)]
            away_games = recent_games[recent_games['MATCHUP'].str.contains('@', na=False)]
            
            home_wins = len(home_games[home_games['WL'] == 'W'])
            home_losses = len(home_games[home_games['WL'] == 'L'])
            away_wins = len(away_games[away_games['WL'] == 'W'])
            away_losses = len(away_games[away_games['WL'] == 'L'])
            
            total_wins = recent_games['WL'].value_counts().get('W', 0)
            total_losses = recent_games['WL'].value_counts().get('L', 0)
            
            print(f"  Total Games: {len(recent_games)} | Record: {total_wins}-{total_losses}")
            print(f"  Home: {home_wins}-{home_losses} ({len(home_games)} games) | Away: {away_wins}-{away_losses} ({len(away_games)} games)")
        
        return recent_games
        
    except Exception as e:
        if show_progress:
            print(f"Error fetching data for {team_name}: {e}")
        return None

def process_team_data(team_data):
    """Convert team data to JavaScript format"""
    if team_data is None:
        return []
    
    processed_data = []
    for _, game in team_data.iterrows():
        processed_data.append({
            'GAME_DATE': game['GAME_DATE'].strftime('%Y-%m-%d'),
            'PTS': int(game['PTS']) if pd.notna(game['PTS']) else 0,
            'HOME_AWAY': 'Home' if 'vs' in str(game['MATCHUP']) else 'Away',
            'WL': game['WL']
        })
    
    return processed_data

def get_all_teams_data():
    """Fetch real NBA data for all teams"""
    print("Fetching real NBA data for all teams...")
    print("This may take a few minutes due to API rate limits...")
    print("=" * 60)
    
    all_teams_data = {}

    # nba_teams= ["Golden State Warriors","Toronto Raptors"]
    
    # Get list of all NBA teams
    try:
        nba_teams = teams.get_teams()
    except:
        print("Error getting NBA teams list. Using fallback list.")
        nba_teams = [
            {'full_name': 'Atlanta Hawks'}, {'full_name': 'Boston Celtics'},
            {'full_name': 'Brooklyn Nets'}, {'full_name': 'Charlotte Hornets'},
            {'full_name': 'Chicago Bulls'}, {'full_name': 'Cleveland Cavaliers'},
            {'full_name': 'Dallas Mavericks'}, {'full_name': 'Denver Nuggets'},
            {'full_name': 'Detroit Pistons'}, {'full_name': 'Golden State Warriors'},
            {'full_name': 'Houston Rockets'}, {'full_name': 'Indiana Pacers'},
            {'full_name': 'LA Clippers'}, {'full_name': 'Los Angeles Lakers'},
            {'full_name': 'Memphis Grizzlies'}, {'full_name': 'Miami Heat'},
            {'full_name': 'Milwaukee Bucks'}, {'full_name': 'Minnesota Timberwolves'},
            {'full_name': 'New Orleans Pelicans'}, {'full_name': 'New York Knicks'},
            {'full_name': 'Oklahoma City Thunder'}, {'full_name': 'Orlando Magic'},
            {'full_name': 'Philadelphia 76ers'}, {'full_name': 'Phoenix Suns'},
            {'full_name': 'Portland Trail Blazers'}, {'full_name': 'Sacramento Kings'},
            {'full_name': 'San Antonio Spurs'}, {'full_name': 'Toronto Raptors'},
            {'full_name': 'Utah Jazz'}, {'full_name': 'Washington Wizards'}
        ]
    
    successful_teams = 0
    for i, team in enumerate(nba_teams):
        team_full_name = team['full_name']
        
        # Get team data
        team_data = get_team_games(team_full_name, show_progress=True)
        
        if team_data is not None:
            all_teams_data[team_full_name] = process_team_data(team_data)
            successful_teams += 1
        
        # Add delay to respect NBA API rate limits
        if i < len(nba_teams) - 1:  # Don't delay after last team
            time.sleep(0.6)  # 600ms delay between requests
        
        # Progress update
        print(f"Progress: {i + 1}/{len(nba_teams)} teams processed")
    
    print("=" * 60)
    print(f"Successfully fetched data for {successful_teams} teams")
    return all_teams_data

def visualize_team_games(all_teams_data, initial_team):
    """Create interactive HTML chart with real data for all teams"""
    
    # Get sorted list of teams
    available_teams = sorted(all_teams_data.keys())
    
    if initial_team not in available_teams and available_teams:
        initial_team = available_teams[0]
        print(f"Initial team not available, using {initial_team} instead")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NBA Team Analysis - Real Data for All Teams</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .controls {{ 
                margin: 20px 0; 
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }}
            .controls select {{
                padding: 8px 12px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }}
            .stats {{ 
                background-color: #e3f2fd; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 20px 0; 
                border-left: 4px solid #2196f3; 
                font-weight: bold;
            }}
            .info {{
                background-color: #d4edda;
                color: #155724;
                padding: 10px;
                border-radius: 4px;
                border-left: 4px solid #28a745;
                margin: 10px 0;
            }}
            .real-data {{
                background-color: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 4px;
                border-left: 4px solid #ffc107;
                margin: 10px 0;
            }}
            #chart {{
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>NBA Team Performance Analysis</h1>
            <h2>Real NBA Data - Balanced Home vs Away Comparison</h2>
            
            <div class="controls">
                <label for="teamSelect">Select Team: </label>
                <select id="teamSelect" onchange="updateChart()">
                    {"".join(f'<option value="{team}" {"selected" if team == initial_team else ""}>{team}</option>' for team in available_teams)}
                </select>
            </div>
            
            <div class="real-data">
                <strong>Real NBA Data:</strong> All data is fetched live from the NBA API for the 2024-25 season (last 6 months).
            </div>
            
            <div class="info">
                <strong>Balanced Analysis:</strong> Uses equal numbers of home and away games for fair statistical comparison.
            </div>
            
            <div id="stats"></div>
            <div id="chart"></div>
        </div>
        
        <script>
            // Real NBA data for all teams
            const allTeamsData = {json.dumps(all_teams_data)};
            const initialTeam = "{initial_team}";
            
            function balanceHomeAwayGames(data) {{
                const homeGames = data.filter(d => d.HOME_AWAY === 'Home');
                const awayGames = data.filter(d => d.HOME_AWAY === 'Away');
                
                // Take equal number of most recent games from each
                const minGames = Math.min(homeGames.length, awayGames.length);
                
                if (minGames === 0) {{
                    return data;
                }}
                
                // Sort each type by date (most recent first) and take equal amounts
                homeGames.sort((a, b) => new Date(b.GAME_DATE) - new Date(a.GAME_DATE));
                awayGames.sort((a, b) => new Date(b.GAME_DATE) - new Date(a.GAME_DATE));
                
                const balancedData = [
                    ...homeGames.slice(0, minGames),
                    ...awayGames.slice(0, minGames)
                ];
                
                return balancedData.sort((a, b) => new Date(a.GAME_DATE) - new Date(b.GAME_DATE));
            }}
            
            function updateChart() {{
                const teamName = document.getElementById('teamSelect').value;
                
                // Get real data for the selected team
                const rawData = allTeamsData[teamName] || [];
                const data = balanceHomeAwayGames(rawData);
                
                if (data.length === 0) {{
                    document.getElementById('stats').innerHTML = '<div class="info">No data available for this team.</div>';
                    document.getElementById('chart').innerHTML = '';
                    return;
                }}
                
                const homeData = data.filter(d => d.HOME_AWAY === 'Home');
                const awayData = data.filter(d => d.HOME_AWAY === 'Away');
                
                const homeAvg = homeData.length > 0 ? homeData.reduce((sum, d) => sum + d.PTS, 0) / homeData.length : 0;
                const awayAvg = awayData.length > 0 ? awayData.reduce((sum, d) => sum + d.PTS, 0) / awayData.length : 0;
                
                const wins = data.filter(d => d.WL === 'W').length;
                const losses = data.filter(d => d.WL === 'L').length;
                
                const traces = [
                    {{
                        x: homeData.map(d => d.GAME_DATE),
                        y: homeData.map(d => d.PTS),
                        mode: 'markers+lines',
                        name: `Home Games (${{homeData.length}})`,
                        marker: {{ 
                            color: homeData.map(d => d.WL === 'W' ? 'green' : 'red'),
                            size: 8, 
                            symbol: 'circle',
                            line: {{ color: 'white', width: 1 }}
                        }},
                        line: {{ color: 'blue', width: 2 }}
                    }},
                    {{
                        x: awayData.map(d => d.GAME_DATE),
                        y: awayData.map(d => d.PTS),
                        mode: 'markers+lines',
                        name: `Away Games (${{awayData.length}})`,
                        marker: {{ 
                            color: awayData.map(d => d.WL === 'W' ? 'lightgreen' : 'pink'),
                            size: 8, 
                            symbol: 'triangle-up',
                            line: {{ color: 'white', width: 1 }}
                        }},
                        line: {{ color: 'orange', width: 2 }}
                    }}
                ];
                
                const layout = {{
                    title: {{
                        text: `${{teamName}} - Real NBA Performance Data`,
                        font: {{ size: 18 }}
                    }},
                    xaxis: {{ 
                        title: 'Game Date',
                        type: 'date'
                    }},
                    yaxis: {{ 
                        title: 'Points Scored',
                        range: [75, 145]
                    }},
                    template: 'plotly_white',
                    hovermode: 'closest',
                    showlegend: true,
                    shapes: homeData.length > 0 && awayData.length > 0 ? [
                        {{
                            type: 'line',
                            x0: data[0].GAME_DATE,
                            x1: data[data.length-1].GAME_DATE,
                            y0: homeAvg,
                            y1: homeAvg,
                            line: {{ color: 'blue', width: 2, dash: 'dash' }}
                        }},
                        {{
                            type: 'line',
                            x0: data[0].GAME_DATE,
                            x1: data[data.length-1].GAME_DATE,
                            y0: awayAvg,
                            y1: awayAvg,
                            line: {{ color: 'orange', width: 2, dash: 'dash' }}
                        }}
                    ] : []
                }};
                
                Plotly.newPlot('chart', traces, layout, {{responsive: true}});
                
                // Update stats display
                const advantage = homeAvg - awayAvg;
                const homeWins = homeData.filter(d => d.WL === 'W').length;
                const awayWins = awayData.filter(d => d.WL === 'W').length;
                const homeLosses = homeData.length - homeWins;
                const awayLosses = awayData.length - awayWins;
                const homeRecord = `${{homeWins}}-${{homeLosses}}`;
                const awayRecord = `${{awayWins}}-${{awayLosses}}`;
                
                const balanceStatus = homeData.length === awayData.length ? 
                    `Balanced: ${{homeData.length}} games each` : 
                    `Unbalanced: ${{homeData.length}} home vs ${{awayData.length}} away`;
                
                const rawHomeGames = rawData.filter(d => d.HOME_AWAY === 'Home').length;
                const rawAwayGames = rawData.filter(d => d.HOME_AWAY === 'Away').length;
                
                const statsHtml = `
                    <div class="stats">
                        <strong>${{teamName}}</strong> (Real NBA Data)<br>
                        <strong>${{balanceStatus}}</strong><br>
                        Overall Record: ${{wins}}-${{losses}}<br>
                        Home Record: ${{homeRecord}} | Away Record: ${{awayRecord}}<br><br>
                        Home Average: ${{homeAvg.toFixed(1)}} pts | Away Average: ${{awayAvg.toFixed(1)}} pts<br>
                        <strong>Home Advantage: ${{advantage > 0 ? '+' : ''}}${{advantage.toFixed(1)}} points</strong>
                    </div>
                `;
                document.getElementById('stats').innerHTML = statsHtml;
            }}
            
            // Initial chart load
            updateChart();
        </script>
    </body>
    </html>
    """
    
    # Save HTML file
    filename = "nba_real_data_analyzer.html"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\nInteractive HTML page saved as: {filename}")
        print(f"Real NBA data loaded for {len(all_teams_data)} teams")
        print("Features: Real NBA data with balanced home/away comparison")
        
        # Open in browser
        webbrowser.open('file://' + os.path.realpath(filename))
        
    except Exception as e:
        print(f"Error creating HTML file: {e}")

def main():
    print("NBA Team Game Results Visualizer")
    print("Real NBA Data for All Teams")
    print("=" * 40)
    
    # Fetch real data for all teams
    all_teams_data = get_all_teams_data()
    
    if not all_teams_data:
        print("No team data was successfully fetched. Please check your internet connection and try again.")
        return
    
    # Create visualization with all real data
    visualize_team_games(all_teams_data, team_name)

if __name__ == "__main__":
    main()
