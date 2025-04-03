// Function to download array as a text file
function downloadArrayAsText(array, filename) {
  const content = array.join('\n');
  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  
  document.body.appendChild(link);
  link.click();
  
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Array to store all song paths
var allSongPaths = [];

// Total number of songs to fetch
const TOTAL_SONGS = 500; 
const BATCH_SIZE = 50;

// Generate a random starting page number to vary results each run
const RANDOM_OFFSET = Math.floor(Math.random() * 1000); 

function fetchBatch(i) {
  fetch("https://www.udio.com/api/songs/search", {
    "body": `{"searchQuery":{"sort":"cache_trending_score","searchTerm":""},"pageSize":50,"pageParam":${i + RANDOM_OFFSET},"trendingId":"da3044d0-d92b-4041-8fd3-bdfb309ebdf0","readOnly":true}`,
    "method": "POST",
    "mode": "cors"
  })
  .then(response => response.json())
  .then(data => {
    // Extract song paths and add to array
    var songPaths = data.data.map(song => song.song_path);
    allSongPaths.push(...songPaths);
    
    console.log(`Fetched batch ${(i / BATCH_SIZE) + 1}. Total songs so far: ${allSongPaths.length}`);
    
    // Continue fetching if we haven't reached total limit
    if (i + BATCH_SIZE < TOTAL_SONGS) {
      fetchBatch(i + BATCH_SIZE);
    } else {
      // All batches completed, download the results
      console.log("All song paths collected:", allSongPaths);
      console.log(`Total songs collected: ${allSongPaths.length}`);
      downloadArrayAsText(allSongPaths, 'song_paths.txt');
    }
  })
  .catch(error => {
    console.error("Error fetching batch at index", i, error);
  });
}

// Start fetching with a random offset
fetchBatch(0);
