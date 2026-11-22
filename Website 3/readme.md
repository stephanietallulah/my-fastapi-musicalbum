# Find Your Music

## About the Website
Find Your Music is a music discovery website that helps users find songs based on their preferences.

Instead of only searching for a specific song, users can choose their mood, situation, and energy level. The website uses these choices to find songs that match their preferences.

Users can also use additional filters such as genre, era, rating and popularity to make the results more specific.

The website gets its music data from a FastAPI backend. The backend provides the song information that the website use to create recommendations.

## Main Functions
The website has the following main functions:

### Music Discovery
The Music Discovery guides the user through four steps

The user first selects their mood, then their situation, and their preferred energy level. After choosing these preferences, the user can review their selections and find recommended music.

The website only allows the user to continue after making a selection for each required preferences.

## How the Website Gets the Music Data
The website connects to a FastAPI backend.

The API address is stored in the JavaScript file and is used to request the available songs

When the website starts, it sends a request to the songs endpoint of the API.

The API returns the music data in JSON format. The website then stores the returned songs and uses them for the different music functions.

## API Configuration and Authentication
The website uses an API key when communicating with the FastAPI backend.

The API key is included in the request headers using the 'x-api-key' field.

The API checks the key when the website requests the music data.

If the request is accepted, the API returns the song information to the website.

The API configuration is stored in the JavaScript file.

## Loading the Music Data
When the website starts, the 'loadSongs()' function runs.

The function sends a request to the API's songs endpoint.

After receiving the response, the website converts the response into JSON format and stores the songs in the 'allSongs' variable.

The website then uses this data for music recommendations, random music, genre options, and era options.

The genre and year options are also created automatically from the available song data.

## Popularity Processing
The popularity level is then classified into three groups:

- Very Popular
- Popular
- Other

A song with at least 100 million streams is classified as Very Popular.

A song with at least 10 million streams is classified as Popular.

Songs below 10 million streams are classified as Other.

The popularity filter uses these levels when displaying recommendation results

## How the Recommendation System Works
The recommendation system compares the user's preferences with the information of each song.

The system gives points when a song matches the user's choices. Mood, situation, and energy have the highest weights, while genre, rating, and era provide additional points.

The scores are added together, and songs with the highest scores are shown first. The website displays up to 10 recommended songs, with the highest-scoring song shown as the Best Match.

## How the Surprise Function Works

The Surprise Me function works differently from the recommendation system.

Instead of calculating scores, it chooses one song randomly from the complete list of songs.

The website generates a random position in the song list and uses that position to select a song.

The selected song is then displayed to the user as a surprise recommendation.

## Technologies Used

### HTML
HTML is used to create the structure of the website.

It contains the different sections, buttons, selections, text, images, and other elements of the webpage.

### CSS
CSS is used to control the appearance and layout of the website.

It controls the design of the music cards, buttons, selections, spacing, fonts, and other visual elements.

### JavaScript
JavaScript controls the main functions of the website.

It handles user selections, API requests, music recommendations, score calculations, filters, random music selection, navigation, and displaying results.

### FastAPI
FastAPI is used as the backend API.

It provides the song data requested by the website.

### Supabase
Supabase is used as the storage service for the music data and related resources used by the API.