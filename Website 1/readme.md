# NOTENOUGH Music API

## About the Website
NOTENOUGH Music API is a backend API that provides music information for the music websites.

It stores information about songs and allows other websites to request the music data through API endpoints.

The API provides information such as song title, album, artist, featured artist, writers, producers, year, genre, language, popularity, rating, image, audio, duration, and description.

The API is built using FastAPI and uses an API key to protect the main music endpoints.

## Main Functions
The API has the following main functions:

### Provide Music Data
The API stores the music data and provides it to websites that request it.

The data is organized into song records. Each song contains different information about the music.

### Search Songs
The API allows users to search for songs using information such as:

- Artist
- Song title
- Album
- Year
- Genre
- Description

The search can also sort the results alphabetically or by release year.

### Get One Song
The API can provide information about one specific song when its song ID is requested.

If the requested song does not exist, the API returns a "Song not found" error.

### Get All Songs
The API can return the complete list of available songs.

The response includes the total number of songs and the song data.

### Health Check
The API has a health check endpoint that shows whether the API is working.

It returns the service status, API version, and current timestamp.

## How the API Works
The API works as a connection between the music data and the websites that use it.

A website sends a request to the API.

The API receives the request and checks what information the website needs.

If the request uses a protected endpoint, the API checks the API key.

After the request is accepted, the API finds the requested music data and sends it back in JSON format.

The website then uses the returned information.

## API Configuration and Authentication
The API uses an API key to protect its main music endpoints.

The API checks the `x-api-key` value sent in the request header.

If the API key is missing or incorrect, the API rejects the request and returns a 401 error.

If the API key is correct, the request is allowed to continue.

This helps prevent unauthorized requests to the protected music data.

## Music Data
Each song in the API contains information such as:

- ID
- Title
- Album
- Artist
- Featured artist
- Writers
- Producers
- Year
- Genre
- Language
- Popularity
- Rating
- Spotify URL
- Image URL
- Audio URL
- Duration
- Description

The API uses a data model to check that the song information follows the required format.

## Data Validation
The API uses Pydantic to validate the music data.

The validation checks that required information has the correct type and follows the required rules.

For example, a song must have a title and artist, and the year must be within the allowed range.

The API validates the starting music data when the application starts.

## API Endpoints

### Home Endpoint
The home endpoint provides basic information about the API.

It returns the API welcome message and lists some of the available endpoints.

### Get All Songs
The API provides an endpoint for getting all available songs.

The response contains the number of songs and the complete song list.

### Search Songs
The search endpoint allows the website to search for music.

The search can look through the artist, title, album, year, genre, and description.

The results can also be sorted alphabetically or by release year.

### Get One Song
The API provides an endpoint for getting one song using its ID.

If the ID matches a song, the API returns that song's information.

If there is no matching song, the API returns a 404 error.

### Health Check
The health check endpoint checks whether the API is running.

It returns the current status, service name, API version, and timestamp.

## Search and Sorting
The search function receives a search query and checks it against several parts of the song information.

The search can look for matching text in:

- Artist
- Title
- Album
- Year
- Genre
- Description

The results can also be sorted in two ways.

### Alphabetical Sorting
The `az` option sorts songs alphabetically according to their titles.

### Date Sorting
The `date` option sorts songs by release year, starting with the newest songs.

## Error Handling
The API returns an error when a request cannot be completed.

If the API key is missing or incorrect, the API returns a 401 error.

If a requested song does not exist, the API returns a 404 error with a message that the song was not found.

## Technologies Used

### Python
Python is used to create the backend API and handle the music data and API functions.

### FastAPI
FastAPI is used to build the API.

It handles requests from the other websites and returns the requested music information.

### Pydantic
Pydantic is used to validate the song data and make sure that the information follows the required format.

### CORS
CORS is configured so that the API can receive requests from websites using the API.

## API Version
The current API version is `1.0`.

The API version is included in the health check response and API configuration.