let index = 0;

const style = document.createElement("style");
document.head.appendChild(style);
resetProgressBar();

let idArray = ["addImagesAndVideos", "addTitleAndDescription", "addTags", "overview"];

function clickNext(){
    if(index == 3) return;
    if(index == 0 && checkIfFileInputIsBlank()) return;
    if(index == 1 && checkIfTitleInputIsBlank()) return;
    if(index == 2) fillOverviewElementsWithValue();
        
    index++;
    showNewTemplate();
}

//#region casesForClickNext
function checkIfFileInputIsBlank(){
    if(document.getElementById("imageInput").value == "") {
        alert("You have to add an image! Accepted file endings: .png, .jpg, .jpeg, .mp4")
        return true;
    }
    return false;
}

function checkIfTitleInputIsBlank(){
    if(isNullOrWhitespace(document.getElementById("titleInput").value)){
        alert("Title can't be empty!");
        return true;
    }
    return false;
}


function fillOverviewElementsWithValue(){
    document.getElementById("titleOverview").innerHTML = document.getElementById("titleInput").value;
    document.getElementById("descriptionOverview").innerHTML = document.getElementById("descriptionInput").value;
}

function isNullOrWhitespace( input ) {
  return (typeof input === 'undefined' || input == null)
    || input.replace(/\s/g, '').length < 1;
}
//#endregion

function clickReturn(){
    if(index == 0) return;
    index--;
    showNewTemplate();
}

function updateProgress(){
    resetProgressBar();

    for(let i = 1; i <=index; i++){
        style.sheet.insertRule('#step-'+ (i + 1) + '::after {background-color: green !important;}');
        style.sheet.insertRule('#step-'+ (i + 1) + '::before {background-color: green !important;}');
    }
}

function showNewTemplate(){
    for(let i = 0; i < idArray.length; i++){
        document.getElementById(idArray[i]).className = "hidden";
    }
    document.getElementById(idArray[index]).className = "";
    updateProgress();
}

function resetProgressBar(){
    const sheet = style.sheet;
    while (sheet.cssRules.length > 0) {
        sheet.deleteRule(0);
    }
    style.sheet.insertRule('#step-1::after {background-color: green;}');
    style.sheet.insertRule('#step-2::after {background-color: royalblue;}');
    style.sheet.insertRule('#step-3::after {background-color: royalblue;}');
    style.sheet.insertRule('#step-4::after {background-color: royalblue;}');
    style.sheet.insertRule('#step-2::before {background-color: royalblue;}');
    style.sheet.insertRule('#step-3::before {background-color: royalblue;}');
    style.sheet.insertRule('#step-4::before {background-color: royalblue;}');
}

function clearData(){
    document.getElementById("titleInput").value = "";
    document.getElementById("descriptionInput").value = "";
    document.getElementById("imageInput").value = "";
    document.getElementById("tagInput").value = "";
}