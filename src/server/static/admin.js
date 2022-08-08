
$("#submitHashVerify").click(function () {
    let hash = document.getElementById("verifyHashInput").value;
    //Skip if length of provided hash is not correct
    if (hash.length != 64) return;

    let url = '/verify?file='+hash;
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            $("#verifyResut").text( JSON.stringify(data) );
            $("#verifyResut").fadeIn();
        });


});