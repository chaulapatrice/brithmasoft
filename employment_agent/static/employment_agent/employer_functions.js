//Function to view employer data
const hostname = "localhost:8000";
viewEmployer = (id) => {
        window.location = `http://${hostname}/employers/${id}`;
    }
    //Function to edit employer data
editEmployer = (id) => {
        window.location = `http://${hostname}/employers/${id}/update`;
    }
    //Function to delete employer data
deleteEmployer = (id) => {
    window.location = `http://${hostname}/employers/${id}/delete`;
}