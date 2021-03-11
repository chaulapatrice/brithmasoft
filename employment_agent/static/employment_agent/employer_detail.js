//After the page finishes loading
document.addEventListener("DOMContentLoaded", (e) => {
    //1. Update the statuses of the employers
    let statusView = document.querySelector('#status');
    let statusViewText = statusView.innerText;

    if (statusViewText === "False") {
        statusView.innerText = "Still looking"
    } else {
        statusView.innerText = "Found"
    }

})