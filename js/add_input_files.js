var counter = 10;
var limit = 2;
function addInput(name){
    if (counter == limit)  {
        alert("You have reached the limit of adding " + counter + " inputs");
    }
    else {
        var newdiv = document.createElement('div');
        newdiv.innerHTML = "Entry " + (counter + 1) + " <br><input type='file' name='input_vcfs'>";
        document.getElementById(name).appendChild(newdiv);
        counter++;
    }
}
