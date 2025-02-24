let currentUrl = window.location.href;
let lastSlashIndex = currentUrl.lastIndexOf('/');
let numberAfterSlash = currentUrl.substring(lastSlashIndex + 1);

var buyButton = document.getElementById('buy-button');
buyButton.addEventListener('click', function() {
    fetch(redirect_url + numberAfterSlash, {method: 'GET'})
    .then(response => response.json())
    .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
});