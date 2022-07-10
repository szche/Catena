

$("#publishNewDigest").click(function() {
    console.log("XD");
    fetch('/push-new-root', {
        credentials: 'include'
    });
});