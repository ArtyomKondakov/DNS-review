var firstHref = $("a[href^='http']").eq(0).attr("href");

function f() {

        console.log(firstHref);
        console.log("script running...");


        let dnsUrls = [...document.getElementsByClassName('catalog-product__rating ui-link ui-link_black')].map(el => el.href);
        var myJSON = JSON.stringify(dnsUrls);
        console.log(myJSON);

        let headers = new Headers();
        headers.append('Access-Control-Allow-Origin', 'https://127.0.0.1:5000/');
        headers.append('Access-Control-Allow-Credentials', 'true');

        function unicodeToChar(text) {
            return text.replace(/\\u[\dA-F]{4}/gi,
                function (match) {
                    return String.fromCharCode(
                        parseInt(match.replace(/\\u/g, ''), 16));
                });
        }

        fetch('http://127.0.0.1:5000/' + btoa(myJSON), {headers: headers}).then(response => response.text())
            .then((response) => {

                response = unicodeToChar(response.toString());
                console.log(unicodeToChar(response.toString()));

                var json = JSON.parse(response);

                var product_stat = document.querySelectorAll('div.catalog-product');

                product_stat.forEach(function (userItem, index, array) {

                    if (json.name[index] == "NULL") {
                        userItem.innerHTML = userItem.innerHTML + " <h4>недостаточно отзывов</h4>";
                        return;
                    }

                    userItem.innerHTML = userItem.innerHTML + " <h4>" + json.review[index
                        ] + "</h4>";
                    console.log(index + " | " + userItem.innerHTML + " | Name: " + json.name[index] + " Review: " + json.review[index]);
                });

            })
            .catch(err => console.log(err));
    }


var b = true;
var prevState = null;
var state = null;
document.addEventListener("DOMSubtreeModified", function(event) {
    var first_lot = document.querySelector('.catalog-products > div');
        if (first_lot) {
            state = first_lot.getAttribute('data-product');
        }

    if (state != prevState) {
        b = true;
    }
    prevState = state;
    if (document.getElementsByClassName("div.catalog-product ui-button-widget") && b)  {
        b = false;
        f()
    }
});



