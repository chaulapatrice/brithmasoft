//Function to retrieve cookie values
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//function to update table after a search has completed
function updateTableAndControls(result) {
    data = JSON.parse(result.data);
    console.log(result)
    console.log(data);
    //now reconstruct the table
    let visibleDataRows = document.querySelectorAll('.data-row');
    let tableRef = document.querySelector('#employers-table').getElementsByTagName('tbody')[0]
    for (const row of visibleDataRows)
        row.remove();
    //now create new rows
    for (const employer of data) {
        //update the date and status
        let status = "";
        if (employer.fields.status == false) {
            status = "Still looking"
        } else {
            status = "Found"
        }

        //now the date
        let dateString = employer.fields.date_needed;
        //create a new date object
        let date = new Date(dateString);
        //first create a new table row
        const row = tableRef.insertRow();
        row.className = 'data-row';

        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            // true for mobile device
            row.innerHTML = `<td><strong>Firstname:</strong> ${employer.fields.firstname}</td>` +
                `<td><strong>Lastname:</strong> ${employer.fields.lastname}</td>` +
                `<td><strong>Job title:</strong> ${employer.fields.job_title}</td>` +
                `<td><strong>Status:</strong> ${status}</td>` +
                `<td><strong>Date needed:</strong> ${date.toDateString()}</td>` +
                `<td id="controls">` +
                `<button style="display:inline-block; margin: 0 10px;" onclick="viewEmployer(${employer.pk})">View</button>` +
                `<button style="display:inline-block; margin: 0 10px;" onclick="editEmployer(${employer.pk})">Edit</button>` +
                `<button style="display:inline-block; margin: 0 10px;" onclick="deleteEmployer(${employer.pk})">Delete</button>` +
                `</td>`;
        } else {
            // false for not mobile device
            row.innerHTML = `<td>${employer.fields.firstname}</td>` +
                `<td>${employer.fields.lastname}</td>` +
                `<td>${employer.fields.job_title}</td>` +
                `<td>${status}</td>` +
                `<td>${date.toDateString()}</td>` +
                `<td id="controls">` +
                `<button style="display:inline-block; margin: 0 10px;" onclick="viewEmployer(${employer.pk})">View</button>` +
                `<button style="display:inline-block; margin: 0 10px;" onclick="editEmployer(${employer.pk})">Edit</button>` +
                `<button style="display:inline-block; margin: 0 10px;" onclick="deleteEmployer(${employer.pk})">Delete</button>` +
                `</td>`;
        }

    }
    //now update the controller user interface
    //if a next page exists
    if (result.next_page) {
        //reset the next-ref
        let nextRef = document.querySelector("#next-ref");
        //remove the child element
        let link = document.querySelector("#next-ref a");
        if (link != null) {
            link.remove();
            nextRef.innerHTML =
                `<button onclick="getEmployerData(${result.next_page})">next &raquo;</button>`
        } else {
            //try a button
            let button = document.querySelector("#next-ref button");
            button.remove();
            //now create a new updated button
            nextRef.innerHTML =
                `<button onclick="getEmployerData(${result.next_page})">next &raquo;</button>`
        }
    } else {
        //remove the content inside next slot
        let link = document.querySelector("#next-ref a");
        if (link != null) {
            link.remove();
        } else {
            let button = document.querySelector("#next-ref button");
            if (button != null)
                button.remove();
        }
    }
    //same applies if a previous page exists
    if (result.previous_page) {
        //reset the next-ref
        let previousRef = document.querySelector("#previous-ref");
        //remove the child element
        let link = document.querySelector("#previous-ref a");
        if (link != null) {
            link.remove();
            previousRef.innerHTML =
                `<button onclick="getEmployerData(${result.previous_page})"> &laquo; previous</button>`
        } else {
            //try a button
            let button = document.querySelector("#previous-ref button");
            if (button != null)
                button.remove();
            //now create a new updated button
            previousRef.innerHTML =
                `<button onclick="getEmployerData(${result.previous_page})"> &laquo; previous</button>`
        }
    } else {
        //remove the content inside next slot
        let link = document.querySelector("#previous-ref a");
        if (link != null) {
            link.remove();
        } else {
            let button = document.querySelector("#previous-ref button");
            if (button != null)
                button.remove();
        }
    }
    //update the current page indicator
    let currentPageSlot = document.querySelector("#current-page");
    if (currentPageSlot)
        currentPageSlot.innerText = result.current_page;
    //update the total pages
    let totalPagesSlot = document.querySelector("#total-pages");
    if (totalPagesSlot)
        totalPagesSlot.innerText = result.total_pages;
}

function getEmployerData(page) {
    $.ajax({
        url: `http://localhost:8000/employers/search/${page}/`,
        type: 'GET',
        success: function(result) {
            updateTableAndControls(result);
        }
    })
}

document.addEventListener('DOMContentLoaded', (e) => {
    let searchForm = document.querySelector("#search-form");
    //Add an event handler so that when a form is submitted an AJAX request is fired
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        let employersTable = document.querySelector('#employers-table');
        //make an ajax request to the backend
        let status = parseInt(document.querySelector('#status').value);
        let jobTitle = document.querySelector('#job-title').value;
        //Construct the data object
        let data = {
            'status': status,
            'job_title': jobTitle
        }
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            url: 'http://localhost:8000/employers/search/1/',
            type: 'POST',
            data: JSON.stringify(data),
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            success: function(result) {
                updateTableAndControls(result);
            },

        });
    })
})