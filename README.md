# Spotify Music Time Machine

A Python project that recreates the Billboard Hot 100 chart from a selected date and creates a private Spotify playlist containing the songs from that chart.

This project was built as part of the **100 Days of Code: The Complete Python Pro Bootcamp**.

## What the Project Does

The program:

1. Asks the user for a date in `YYYY-MM-DD` format.
2. Retrieves the Billboard Hot 100 chart for that date.
3. Extracts the song titles and artists.
4. Searches for the songs on Spotify.
5. Collects the Spotify track URIs for songs that are successfully found.
6. Creates a private Spotify playlist named after the selected chart date.
7. Adds the matched songs to the playlist.

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Spotipy
* Spotify Web API
* python-dotenv
* Billboard Hot 100

## Project Structure

```text
Day_46_TimeMusic_Machine/
│
├── main.py
├── .env.example
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Day_46_TimeMusic_Machine.git
cd Day_46_TimeMusic_Machine
```

### 2. Install the required packages

```bash
pip install requests beautifulsoup4 spotipy python-dotenv
```

### 3. Create your environment file

Create a `.env` file in the project root and add your own credentials.

Use `.env.example` as a template:

```env
BILLBOARD_URL=

SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
REDIRECT_URI=
SCOPE=
```

Do not share or commit your `.env` file.

### 4. Configure Spotify

Create a Spotify application through the Spotify Developer Dashboard and obtain your Client ID and Client Secret.

Configure the Redirect URI to match the value used by the application.

The application requires permission to modify private playlists.

### 5. Run the program

```bash
python main.py
```

Enter a date in the following format when prompted:

```text
YYYY-MM-DD
```

For example:

```text
2020-08-15
```

The program will retrieve the Billboard chart for that date, search for the tracks on Spotify, and create a private playlist containing the tracks that were successfully matched.

## Notes

Not every Billboard song may be found on Spotify. When a song cannot be matched, the program skips it rather than adding an incorrect track.

The project depends on retrieving the Billboard chart and searching Spotify, so changes to either service may affect the application.

## What I Learned

This project helped me practice:

* Working with web requests using `requests`
* Web scraping with BeautifulSoup
* Working with APIs
* Using Spotipy to interact with the Spotify Web API
* Loading environment variables with `python-dotenv`
* Handling user input and validating dates
* Searching for data using multiple pieces of information such as song titles and artists
* Working with Spotify playlists
* Organizing a Python project using functions
* Managing secrets with environment variables and `.gitignore`

## Future Improvements

Possible improvements include:

* Improving Spotify track matching
* Handling more edge cases when scraping Billboard
* Adding better logging
* Providing a summary of songs that could not be found
* Improving error handling for API and network failures

```
```
