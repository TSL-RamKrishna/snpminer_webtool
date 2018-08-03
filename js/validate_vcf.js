const vcfalert = function (format, msg) {
  alert("The select file does not look " + format + " format.\nPlease upload correct " + format + " format file.\n" + msg)
};

const validate_vcf = function () {
  // Grab a file reference



  var files = $(this)[0].files;
  var isGood = true;

  var current = 0;
  var currentfile="";
  function doNext(){

    if(isGood){

      if(current < files.length){
        currentfile=files[current];
        checkIt(currentfile);
      }
      current++;
    } else {
      notvalid();
    }
  }

  doNext()
  //
  function notvalid() {
    $(this)[0].val("");
    console.error('BAD!');
  }

  function checkIt(file){
    console.log('current file', file);
    // Create a new instance of the LineReader
    const lr = new LineReader();

    lr.on('end', doNext);

    let counter = 0;
    let snpcount = 0;
    let read_header = false;
    let header_array = undefined;
    // Bind to the line event
    lr.on('line', function (line, next) {
      // Do something with line....
      counter += 1;

      if (counter === 1) {
        if (line.startsWith("##") && (line.includes("fileformat=VCF"))) {
          console.log(line);
        }
        else {
          isGood = false;
          vcfalert("VCF", "First line should begin with ##fileformat=VCFv4.x");
          // notvalid();

          lr.abort()
        }
      }
      else if (line.startsWith("##")) {
        console.log(line)
      }
      else if (line.startsWith("#CHROM")) {
        console.log(line);
        header_array = line.split("\t");
        console.log("header array length " + header_array.length);
        if (header_array.length == 10) {  // the header contains 9 columns + one sample = 10
          console.log("Header looks fine");
          read_header = true
        }
        else if (header_array.length > 10){
          multiplesamples_text = document.getElementById('multiplesamples')
          if (multiplesamples_text.style.display === 'none'){
            multiplesamples_text.style.display = 'inherit'
          }
          var multiple_samples=header_array.slice(9)
          // document.getElementById('multiplesample_wrapper').innerHTML=multiple_samples.join(","); // returning the list of sample list to the html page
          console.log("Multiple sample names found: " + multiple_samples.join("_"));

          // var multiplesample_wrapper = document.getElementById('multiplesample_wrapper');
          // if (multiplesample_wrapper.style.display === 'none'){
          //   multiplesample_wrapper.style.display = 'inherit';
          // }

          multiplesamplespara = document.getElementById("input_files_wrap_id");

          var newdiv = document.createElement("div");
          newdiv.id =  "divid_" + multiple_samples.join("_");
          newdiv.name =  "divname_" + multiple_samples.join("_");
          newdiv.style = "background-color:lightblue; display:inherit";

          // var para = document.createElement("p");//create <p>
          var text = document.createTextNode("Please select samples (one or more) of interest to analyse.   ");
          var newline = document.createElement("br");

          newdiv.appendChild(text);//append text to para
          newdiv.appendChild(newline);

          // var elementsToInsert = [];

          // Creation of the input with radio type and the labels
          for(var i = 0; i < multiple_samples.length; i++) {
            var check = document.createElement("input");
            var label = document.createElement('label');
            check.type = "checkbox";
            check.name = "multiplesamples_" + multiple_samples.join("_") + "_filename_" + currentfile;   // this has to be unique for each file, else user can select all samples
            check.value = multiple_samples[i];
            check.width = "32";
            check.height = "32";
            check.class = multiple_samples.join("_");
            check.id = multiple_samples.join("_");

            label.setAttribute("for", multiple_samples[i]); // this is optional, it works without for attribute
            label.innerHTML = multiple_samples[i] ;
            newdiv.appendChild(label);
            newdiv.appendChild(check);

            //  elementsToInsert.push({ label: label, radio: radio });
          }

          // divelement.appendChild(para);// append <p> to <div> and assign to variable
          // question to merge

          var question = "<div id=question_" + multiple_samples.join("_") + " style=\"display: none;\"><label>You have selected multiple samples. Do you want to combine these selected samples as one? <input name=name_question_" + multiple_samples.join("_") + " id=id_question_" + multiple_samples.join("_") + " type=\"checkbox\"></label></div><br><br>"

          document.body.append(newdiv)
          $(newdiv).insertBefore("#select_what_you_want")
          $(question).insertBefore('#select_what_you_want')

          // function to check the length of checkboxes selected and display question
          var d1=$('#' + "divid_" + multiple_samples.join("_"))
          var checkboxes = d1.find('input[type=checkbox]');
          var questionBox = $('#' + 'question_' + multiple_samples.join("_"));

          console.log('#' + "divid_" + multiple_samples.join("_"))
          console.log(d1);
          console.log(checkboxes);
          console.log(questionBox);

          checkboxes.on('change', function () {

              console.log(checkboxes);
              var checkedCount = checkboxes.filter(function () {
                  return this.checked;
              }).length;

              console.log(checkedCount);
              if (checkedCount > 1) {

                  questionBox.show();
              } else {
                  questionBox.hide();
              }


          })

        }

      }
      else if (read_header === true) {
        snpcount += 1;
        const snpline = line.split("\t");
        //console.log("snpline length " + snpline.length)
        if (snpline.length !== header_array.length) {
          //console.log("Correct VCF file format selected")
          alert("A line found that does not match the number of records with the number of column headers. The line is \n" + line);
          // notvalid();
          isGood = false;
        }
        else if (snpcount === 1) {
          console.log("1 line of snps read");
          lr.abort()
        }

      }
      else {
        console.log(line)
      }
      next(); // Call next to resume...
    });

    // Begin reading the file
    lr.read(file);
  }

};

$('input[name="input_vcfs[]"]').on('change', validate_vcf);
