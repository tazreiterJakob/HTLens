let idArray = ["addImagesAndVideos", "addTitleAndDescription", "addTags", "overview"];
const input = document.getElementById("imageInput");
input.value = "";
const preview = document.getElementById("addedImages");

input.addEventListener('change', () => {
    preview.innerHTML = '';

    Array.from(input.files).forEach(file => {
      if (!file.type.startsWith('image/')) return;

      const reader = new FileReader();
      reader.onload = e => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = "h-60";
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
});


function checkIfInputIsBlank(){
    if(isNullOrWhitespace(document.getElementById("imageInput").value)) {
        alert("Sie müssen ein Bild hinzufügen! Akzeptierte Dateiformate: .png, .jpg, .jpeg, .mp4")
        return;
    }
    if(isNullOrWhitespace(document.getElementById("titleInput").value)){
        alert("Titel kann nicht leer sein!");
        return;
    }
    document.getElementById("submit_button").click();
}

function checkIfTitleInputIsBlank(){
    
}

function isNullOrWhitespace( input ) {
  return (typeof input === 'undefined' || input == null)
    || input.replace(/\s/g, '').length < 1;
}

function clearData(){
    document.getElementById("titleInput").value = "";
    document.getElementById("descriptionInput").value = "";
    document.getElementById("imageInput").value = "";
    document.getElementById("tagInput").value = "";
}