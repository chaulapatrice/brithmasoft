//After the page finishes loading 
document.addEventListener("DOMContentLoaded", (e) =>{
    //1. Update the statuses of the employers
    let status = document.querySelectorAll('.status');
    for(const statusView of status){
        let statusViewText = statusView.innerText;
        statusViewText = statusViewText.trim();
        if(statusViewText === "False"){
            statusView.innerText = "Still looking"
        } else{
            statusView.innerText = "Found"
        }
    }
})
//Function to view employer data
viewEmployer = (id) => {
    console.log(id);
}
//Function to edit employer data
editEmployer = (id) => {
    console.log(id);
}
//Function to delete employer data
deleteEmployer = (id) => {
    console.log(id);
}