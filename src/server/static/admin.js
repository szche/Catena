
let blockstream_url = 'https://blockstream.info/testnet/'

$("#submitHashVerify").click(function () {
    let hash = document.getElementById("verifyHashInput").value;
    //Skip if length of provided hash is not correct
    if (hash.length != 64) return;

    let url = '/verify?file='+hash;
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            if(JSON.stringify(data) == "[]" ) {
                $("#verifyResut").text( "Could not find proof" );
            }
            else {
                $("#verifyResut").text( btoa(JSON.stringify(data)) );
            }
            $("#verifyResut").fadeIn();
        });


});

setInterval(watchForRootChange, 1000);

function watchForRootChange() {
    let address = document.getElementById("CatenaAddress").innerText;
    fetch('/watch-for-update')
    .then((response) => response.json())
    .then((data) => {
        if(data['status'] == "ALERT") {
            let tx_url = blockstream_url+data['txid']
            let message = `⚠️ Change in merkle root detected!<br>OP_RETURN: ${data['op_return']}<br>Txid: <a href="${tx_url}" target="_blank">${data['txid']}</a>`
            document.getElementById("newOpReturnAlerter").innerHTML = message;
            $("#newOpReturnAlerter").fadeIn();
        }
    });
}