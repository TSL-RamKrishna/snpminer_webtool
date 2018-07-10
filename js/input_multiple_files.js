var max_fields      = 20;
var wrapper         = $(".input_files_wrap");
var add_button      = $(".add_field_button");
var remove_button   = $(".remove_field_button");

var total_fields;

$(add_button).click(function(e){
    e.preventDefault();
    total_fields = wrapper[0].childNodes.length;
    if(total_fields < max_fields){
      var newVCFInput = '<input type="file" name="input_vcfs[]" required multiple>';

      var $vcf = $(newVCFInput)
      $($vcf).on('change', validate_vcf);
      $(wrapper).append($vcf);
      $(wrapper).append('<br>');
      console.log("wrapper childnode length " + total_fields);
    }
});
$(remove_button).click(function(e){
    // e.preventDefault();
    total_fields = wrapper[0].childNodes.length;
    if(total_fields>1){
        wrapper[0].childNodes[total_fields-1].remove();
    }
    console.log("wrapper childnode length " + total_fields);
});
