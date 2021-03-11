document.addEventListener("DOMContentLoaded", (e) => {
    //1. Update the statuses of the employers
    let statusView = document.querySelector('#status');
    let statusViewText = statusView.innerText;

    if (statusViewText === "False") {
        statusView.innerText = "Unemployed"
    } else {
        statusView.innerText = "Employed"
    }

})