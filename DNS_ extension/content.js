var firstHref = $("a[href^='http']").eq(0).attr("href");

console.log(firstHref);
console.log("script running...");

let dnsUrl = window.btoa(window.location.toString());
console.log(dnsUrl);

let headers = new Headers();
headers.append('Access-Control-Allow-Origin', 'https://127.0.0.1:5000/');
headers.append('Access-Control-Allow-Credentials', 'true');

fetch('http://127.0.0.1:5000/' + dnsUrl, { headers: headers}).then(response => response.text())
        .then((response) => {
            console.log(response.toString())
        })
        .catch(err => console.log(err));