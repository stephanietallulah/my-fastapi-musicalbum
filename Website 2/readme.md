# Music Statistics

## About the Website
Music Statistics is a music data website that allows users to explore and understand information about songs. 

The website displays statistics about the available music data, including the total number of songs, total artists, average rating, and total streams.

Users can also view the top songs, songs by year, genre distribution, and detailed information about songs in a selected genre.

The website gets its music data from a FastAPI backend. The backend provides the song information that the website uses to create the different statistics and analyses.

## Main Functions
The website has the following main functions:

### Music Statistics
The website calculates and displays several statistics from the available song data.

These include:

- Total number of songs
- Total number of artists
- Average song rating
- Total number of streams

The statistics are calculated automatically when the music data is loaded.

## How the Website Gets the Music Data
The website connects to a FastAPI backend.

The API address is stored in the JavaScript file and is used to request the available songs.

When the website starts, it sends a request to the songs endpoint of the API.

The API returns the music data in JSON format. The website then stores the returned songs in the `allSongs` variable.

The website uses this data to create the statistics, rankings, charts, and genre analysis.

## API Configuration and Authentication
The website uses an API key when communicating with the FastAPI backend.

The API key is included in the request headers using the `x-api-key` field.

The API checks the key when the website requests the music data.

If the request is accepted, the API returns the song information to the website.

The API configuration is stored in the JavaScript file.

## Loading the Music Data
When the website starts, the `loadSongs()` function runs.

The function sends a request to the API's songs endpoint.

After receiving the response, the website converts the response into JSON format and stores the songs in the `allSongs` variable.

The website then uses this data to display the statistics, top songs, songs by year, genre distribution, and genre options.

## Music Statistics
The website calculates four main statistics from the song data.

### Total Songs
The website counts all the songs in the music data.

### Total Artists
The website counts the different artists in the music data. Artists with the same name are counted only once.

### Average Rating
The website calculates the average rating of all songs that have a valid rating.

### Total Streams
The website calculates the total number of streams from the popularity information of the songs.

## Popularity Processing
The website converts the popularity information into numbers so that the songs can be compared.

Popularity values that use thousand, million, or billion are converted into their actual numerical values.

The website can then use these values to calculate total streams and determine the most popular songs.

The total stream value is displayed using shorter formats such as K, M, and B when needed.

## Top Songs
The website displays the top five songs based on their number of streams.

The songs are sorted from the highest number of streams to the lowest number of streams.

Each top song displays its ranking, image, title, artist, and number of streams.

## Songs by Year
The website groups the songs according to their release year.

It counts how many songs belong to each year and displays the results using a visual bar chart.

Each year shows the number of songs released during that year.

The bars are sized based on the number of songs for each year.

## Genre Distribution
The website groups songs according to their genre.

Some similar or combined genres are grouped into larger categories before the distribution is displayed.

The website counts the number of songs in each genre category and sorts the genres from the largest number of songs to the smallest.

The results are displayed using bars that show the number of songs in each genre.

## Genre Analysis
The website allows the user to select a genre from a dropdown menu.

After selecting a genre, the website displays information about that genre.

The genre analysis includes:

- Genre name
- Number of songs
- Number of artists
- Percentage of all songs

The website also displays a list of songs that belong to the selected genre.

## Song Details
Users can select a song from the genre song list to view more information.

The selected song can display:

- Song title
- Artist
- Featured artist
- Album
- Year
- Genre
- Language
- Duration
- Writers
- Producers
- Rating
- Popularity
- Description

If an audio link is available, the website also provides a Listen button that opens the available audio link.


## Technologies Used

### HTML
HTML is used to create the structure of the website.

It contains the different sections, statistics, lists, buttons, dropdowns, images, and other elements of the webpage.

### CSS
CSS is used to control the appearance and layout of the website.

It controls the design of the statistics, music cards, charts, buttons, dropdowns, spacing, fonts, and other visual elements.

### JavaScript
JavaScript controls the main functions of the website.

It handles API requests, data processing, calculations, sorting, grouping, statistics, charts, genre analysis, and displaying song information.

### FastAPI
FastAPI is used as the backend API.

It provides the song data requested by the website.

### Supabase
Supabase is used as the storage service for the music data and related resources used by the API.