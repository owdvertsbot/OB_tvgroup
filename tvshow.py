import requests

# Replace YOUR_API_KEY with your actual API key
API_KEY = '9555335f868ed5bce03a57c35fa9da19'

# Set up the API endpoint URL
url = f'https://api.themoviedb.org/3/tv/1399?api_key={API_KEY}'

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the relevant information
    poster_path = data['poster_path']
    title = data['name']
    year = data['first_air_date'][:4]
    seasons = data['number_of_seasons']
    total_episodes = data['number_of_episodes']
    run_time = data['episode_run_time'][0]
    actors = [actor['name'] for actor in data['credits']['cast'][:5]]
    directors = [crew['name'] for crew in data['credits']['crew'] if crew['job'] == 'Director']
    genres = [genre['name'] for genre in data['genres']]
    streaming_services = ['HBO', 'HBO Max']

    # Print the TV show information
    print(f'TV Show Poster: ![alt text](https://image.tmdb.org/t/p/w500{poster_path})')
    print(f'Caption: {title} ({year})')
    print(f'Seasons: {seasons}')
    print(f'Total Episodes: {total_episodes}')
    print(f'Run Time: {run_time} minutes per episode')
    print(f'Actors: {actors}')
    print(f'Directors: {directors}')
    print(f'Genre: {genres}')
    print(f'Where to Watch: {streaming_services}')
else:
    # Print an error message if the request failed
    print(f'Request failed with status code {response.status_code}')
