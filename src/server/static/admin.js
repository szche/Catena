

$("#publishNewDigest").click(function() {
    fetch('/push-new-root', {
        credentials: 'include'
    });
});