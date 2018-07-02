const vcfalert = function (format, msg) {
  alert("The select file does not look " + format + " format.\nPlease upload correct " + format + " format file.\n" + msg)
};

const validate_vcf = function () {
  // Grab a file reference



  var files = $(this)[0].files;
  var isGood = true;

  var current = 0;

  function doNext(){

    if(isGood){

      if(current < files.length){
        checkIt(files[current]);
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
          multiple_samples=header_array.slice(9)
          document.getElementById('multiplesamplesid').innerHTML=multiple_samples.join(","); // returning the list of sample list to the html page
          console.log("Multiple sample names found: " + multiple_samples.join(","))
        }        
        //   if (window.confirm("Multiple samples detected in a VCF file. Do you want to split the vcf file to one VCF per sample?")){
        //     userpressed = "User pressed ok"
        //     alert("You have confirmed to split the vcf records by sample" + header_array.slice(9).join(","))
        //
        //
        //       //  function createRadioButtonFromArray(array) {
        //       //     var len = array.length;
        //       //     var form = document.getElementById("form1");
        //       //     for (var i = 0; i < len; i++){
        //       //         var radio = document.createElement("input");
        //       //             radio.type = "radio";
        //       //             radio.name = "samplechoices";
        //       //             radio.class = "radioButtons";
        //       //             radio.value = i;
        //       //             radio.id = "choice" + i;
        //       //             //radio.id = array[i]
        //       //         var radioText = document.createElement("div");
        //       //             radioText.id = "c" + i;
        //       //             radioText.class = "choiceText";
        //       //             radioText.innerHTML = array[i];
        //       //
        //       //         form.appendChild(radio);
        //       //         radio.appendChild(radioText);
        //       //
        //       //         document.getElementById("c" + i).innerHTML=array[i];
        //       //
        //       //
        //       //     }
        //       // }
        //       // createRadioButtonFromArray(multiple_samples)
        //
        //     var sample = prompt("Samples found are " + header_array.slice(9).join(",") + ". Enter the sample name to split out from the multisample VCF.")
        //     // Loop until the user gives a valid sample name
        //     while ((sample == null || sample == "") || !(header_array.slice(9).includes(sample))){
        //       alert("Invalid or null sample name entered.")
        //       sample = prompt("Enter the sample name to split out from the multisample VCF.")
        //     }
        //
        //     //split specific sample, user defined
        //
        //     alert("User selected sample name " + sample + ". Click OK to continue.")
        //
        //   }
        //   else {
        //     //userpressed = "user pressed cancel"
        //     console.log("User canceled to split the multisample vcf.")
        //     alert("You canceled to split multisample vcf by sample. This webtool will now consider only the first sample in the vcf file for processing.");
        //   }
        // }
        //
        // else {
        //   isGood = false;
        //   vcfalert("VCF", "");
        //   // notvalid();
        //
        // }
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
