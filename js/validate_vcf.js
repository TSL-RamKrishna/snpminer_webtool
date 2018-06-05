const vcfalert = function (format, msg) {
    alert("The select file does not look " + format + " format.\nPlease upload correct " + format + " format file.\n" + msg)
};

const validate_vcf = function () {
    // Grab a file reference
    const file = $('#upload')[0].files[0];

    // Create a new instance of the LineReader
    const lr = new LineReader();

    let counter = 0;
    let snpcount = 0;
    let read_header = false;
    let header_array = undefined;
    // Bind to the line event
    lr.on('line', function (line, next) {
        // Do something with line....
        counter += 1;

        function notvalid() {
            $('#upload').val("");
        }

        if (counter === 1) {
            if (line.startsWith("##") && (line.includes("fileformat=VCF"))) {
                console.log(line);
            }
            else {
                vcfalert("VCF", "First line should begin with ##fileformat=VCFv4.x");
                notvalid();
            }
        }
        else if (line.startsWith("##")) {
            console.log(line)
        }
        else if (line.startsWith("#CHROM")) {
            console.log(line);
            header_array = line.split("\t");
            console.log("header array length " + header_array.length);
            if (header_array.length >= 10) {
                console.log("Header looks fine");
                read_header = true

            }
            else {
                vcfalert("VCF", "");
                notvalid();
            }
        }
        else if (read_header === true) {
            snpcount += 1;
            const snpline = line.split("\t");
            //console.log("snpline length " + snpline.length)
            if (snpline.length !== header_array.length) {
                //console.log("Correct VCF file format selected")
                alert("A line found that does not match the number of records with the number of column headers. The line is \n" + line);
                notvalid();
            }
            else if (snpcount === 5) {
                console.log("5 lines of snps read");
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


};

$("#upload").on('change', validate_vcf);
