let index = 0;
let idArray = ["addImagesAndVideos", "addTitleAndDescription", "addTags", "overview"];
const input = document.getElementById("imageInput");
const preview = document.getElementById("addedImages");
const style = document.createElement("style");
document.head.appendChild(style);
resetProgressBar();

let yearSelection = null;

  document.addEventListener('DOMContentLoaded', () => {
    const dropdownItems = document.querySelectorAll('#yearSelection li a');

    dropdownItems.forEach(item => {
      item.addEventListener('click', (event) => {
        const selectedText = event.target.textContent.trim();
        document.getElementById("tagsField").innerHTML += '<a class="badge flex badge-info items-center"><img class="h-5" src="images/hashtag.svg"><div class="hover:cursor-pointer">' + selectedText + '</div></a>'
        yearSelection = selectedText;
    });
    });
  });

let fractionSelection = null;
  document.addEventListener('DOMContentLoaded', () => {
    const dropdownItems = document.querySelectorAll('#fractionSelection li a');

    dropdownItems.forEach(item => {
      item.addEventListener('click', (event) => {
        const selectedText = event.target.textContent.trim();
        document.getElementById("tagsField").innerHTML += '<a class="badge flex badge-info items-center"><img class="h-5" src="images/hashtag.svg"><div class="hover:cursor-pointer">' + selectedText + '</div></a>'
        fractionSelection = selectedText;
      });
    });
  });

  let classSelection = null;

  document.addEventListener('DOMContentLoaded', () => {
    const dropdownItems = document.querySelectorAll('#classSelection li a');

    dropdownItems.forEach(item => {
      item.addEventListener('click', (event) => {
        const selectedText = event.target.textContent.trim();
            document.getElementById("tagsField").innerHTML += '<a class="badge flex badge-info items-center"><img class="h-5" src="images/hashtag.svg"><div class="hover:cursor-pointer">' + selectedText + '</div></a>'

            classSelection = selectedText;
      });
    });
  });

input.addEventListener('change', () => {
    preview.innerHTML = '';

    Array.from(input.files).forEach(file => {
      if (!file.type.startsWith('image/')) return;

      const reader = new FileReader();
      reader.onload = e => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = "h-60";
        img.addEventListener('click', () => {
          preview.removeChild(img);
          if(preview.innerHTML == ""){
            input.innerHTML = "";
            input.value = "";
          }
        });
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
});

function clickNext(){
    if(index == 3) 
    {
      sendData();
        return;
    }
    if(index == 0 && checkIfFileInputIsBlank()) return;
    if(index == 1 && checkIfTitleInputIsBlank()) return;
    if(index == 2){
        if(yearSelection == null || classSelection == null || fractionSelection == null) {
            alert("Achtung! Es müssen Schuljahr, Abteilung und Klassen angegeben werden!");
            return;
        }
    }
    if(index == 2) fillOverviewElementsWithValue();
    
    index++;
    showNewTemplate();
}

//#region casesForClickNext
function checkIfFileInputIsBlank(){
    if(document.getElementById("imageInput").value == "") {
        alert("Sie müssen ein Bild hinzufügen! Akzeptierte Dateiformate: .png, .jpg, .jpeg, .mp4")
        return true;
    }
    return false;
}

function checkIfTitleInputIsBlank(){
    if(isNullOrWhitespace(document.getElementById("titleInput").value)){
        alert("Titel kann nicht leer sein!");
        return true;
    }
    return false;
}


function fillOverviewElementsWithValue(){
    document.getElementById("titleOverview").innerHTML = document.getElementById("titleInput").value;
    document.getElementById("descriptionOverview").innerHTML = document.getElementById("descriptionInput").value;
    document.getElementById("addedImagesOverview").innerHTML = document.getElementById("addedImages").innerHTML;
    document.getElementById("tagsFieldOverview").innerHTML = document.getElementById("tagsField").innerHTML;
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

function addTag(){
    let text = document.getElementById("tagInput").value;
    document.getElementById("tagsField").innerHTML += '<a class="badge flex badge-info items-center" onclick="deleteTag(event)"><img class="h-5" src="images/hashtag.svg"><div class="hover:line-through hover:cursor-pointer">' + text + '</div></a>'
    document.getElementById("tagInput").value = "";
}

function deleteTag(event){
    event.currentTarget.remove();
}

function sendData(){
 // Create the form element
const form = document.createElement('form');
form.method = 'post';
form.className = 'm-100';
form.action = "/create";
form.enctype = 'multipart/form-data';

// Create input for title
const titleInput = document.createElement('input');
titleInput.value = document.getElementById('titleInput');
titleInput.name = 'title';
titleInput.type = 'text';
titleInput.placeholder = 'TITEL';
form.appendChild(titleInput);

// Create input for description
const descriptionInput = document.createElement('input');
descriptionInput.value = document.getElementById('descriptionInput');
descriptionInput.name = 'description';
descriptionInput.type = 'text';
descriptionInput.placeholder = 'beschr';
form.appendChild(descriptionInput);

// Create input for tags
const tagsInput = document.createElement('input');
let tags = document.getElementById("tagsField").innerHTML;
let split = tags.split('>');
let splitsplit = [];
for(let i = 0; i < split.length; i++){
  splitsplit.push(split[i].split('<'));
}
let tagsArray = [];
for(let i = 0; i < splitsplit.length; i++){
  if(i == 3 ||i % 5 == 3){
    tagsArray.push(splitsplit[i][0])
  }
}
let s = "";
for(let i = 0; i < tagsArray.length; i++){
  if(i != tagsArray.length-1) s = s + tagsArray[i] + ";";
  else s = s + tagsArray[i];
}
tagsInput.value = s;
tagsInput.name = 'tags';
tagsInput.type = 'text';
tagsInput.placeholder = 'hash';
form.appendChild(tagsInput);

// Create file input
const fileInput = document.createElement('input');
fileInput.value = document.getElementById('imageInput').value;
console.log(fileInput.value);
fileInput.type = 'file';
fileInput.name = 'images';
fileInput.multiple = true;
submitButton.type = 'submit';
const submitButton = document.createElement('button');
submitButton.click();
}