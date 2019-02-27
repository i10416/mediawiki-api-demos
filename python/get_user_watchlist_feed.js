//This file is autogenerated

let URL = "https://en.wikipedia.org/w/api.php"; 

const params = {
    action: "feedwatchlist",
    wlowner: "sample_user",
    wltoken: "sample_watchlist_token"
}

URL = URL + "?origin=*";
Object.keys(params).forEach(key => URL = URL + "&" + key + "=" + params[key]);

fetch(URL)
    .then(response => response.json())
    .then(response => console.log(response))
    .catch(error=>console.log(error))
