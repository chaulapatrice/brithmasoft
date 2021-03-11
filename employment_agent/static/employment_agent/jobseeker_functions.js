// Function to view employer data
const hostname = "localhost:8000";
viewJobSeeker = (id) => {
        window.location = `http://${hostname}/job_seekers/${id}`;
    }
    // Function to edit employer data
editJobSeeker = (id) => {
        window.location = `http://${hostname}/job_seekers/${id}/update`;
    }
    // Function to delete employer data
deleteJobSeeker = (id) => {
    window.location = `http://${hostname}/job_seekers/${id}/delete`;
}