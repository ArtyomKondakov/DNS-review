var firstHref = $("a[href^='http']").eq(0).attr("href");

var b = true;
document.addEventListener("DOMSubtreeModified", function(event) {
    if (document.getElementsByClassName("div.catalog-product ui-button-widget") && b) {
        b = false;
            console.log(firstHref);
console.log("script running...");

let dnsUrl = window.btoa(window.location.toString());
console.log(dnsUrl);

let headers = new Headers();
headers.append('Access-Control-Allow-Origin', 'https://127.0.0.1:5000/');
headers.append('Access-Control-Allow-Credentials', 'true');

function unicodeToChar (text) {
    return text.replace(/\\u[\dA-F]{4}/gi,
        function (match) {
            return String.fromCharCode(
                parseInt(match.replace(/\\u/g, ''), 16));
        });
}

fetch('http://127.0.0.1:5000/' + dnsUrl, { headers: headers}).then(response => response.text())
        .then((response) => {

            response = unicodeToChar(response.toString());
            console.log(unicodeToChar(response.toString()));


            var json = JSON.parse(response);

            var product_stat = document.querySelectorAll('div.catalog-product');

            product_stat.forEach(function(userItem, index, array) {

                if (json.name[index] == "NULL") {
                    userItem.innerHTML = userItem.innerHTML + " <h2>недостаточно отзывов</h2>";
                    return;
                }

                userItem.innerHTML = userItem.innerHTML + " <h2>" + json.review[index] + "</h2>";
                console.log(index + " | " + userItem.innerHTML + " | Name: " + json.name[index] + " Review: " + json.review[index]);
            });




        })
        .catch(err => console.log(err));

    }
});




document.addEventListener("DOMSubtreeModified", function(event) {
    if (document.getElementsByClassName("ul.pagination-widget__pages")) {


        var pageSelector = document.querySelectorAll('ul.pagination-widget__pages');
pageSelector[0].onclick = function() {
    console.log(firstHref);
console.log("script running...");

let dnsUrl = window.btoa(window.location.toString());
console.log(dnsUrl);

let headers = new Headers();
headers.append('Access-Control-Allow-Origin', 'https://127.0.0.1:5000/');
headers.append('Access-Control-Allow-Credentials', 'true');

function unicodeToChar (text) {
    return text.replace(/\\u[\dA-F]{4}/gi,
        function (match) {
            return String.fromCharCode(
                parseInt(match.replace(/\\u/g, ''), 16));
        });
}

fetch('http://127.0.0.1:5000/' + dnsUrl, { headers: headers}).then(response => response.text())
        .then((response) => {

            response = unicodeToChar(response.toString());
            console.log(unicodeToChar(response.toString()));


            var json = JSON.parse(response);

            var product_stat = document.querySelectorAll('div.catalog-product');

            product_stat.forEach(function(userItem, index, array) {

                if (json.name[index] == "NULL") {
                    userItem.innerHTML = userItem.innerHTML + " <h2>недостаточно отзывов</h2>";
                    return;
                }

                userItem.innerHTML = userItem.innerHTML + " <h2>" + json.review[index] + "</h2>";
                console.log(index + " | " + userItem.innerHTML + " | Name: " + json.name[index] + " Review: " + json.review[index]);
            });




        })
        .catch(err => console.log(err));

};






    }
});



