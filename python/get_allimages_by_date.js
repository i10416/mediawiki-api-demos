//This file is autogenerated

let URL = "https://en.wikipedia.org/w/api.php"; 

const params = {
    action: "query",
    format: "json",
    list: "allimages",
    aisort: "timestamp",
    aistart: "2010-01-01T18:05:46Z"
}

URL = URL + "?origin=*";
Object.keys(params).forEach(key => URL = URL + "&" + key + "=" + params[key]);

fetch(URL)
    .then(response => response.json())
    .then(response => console.log(response))
    .catch(error=>console.log(error))
