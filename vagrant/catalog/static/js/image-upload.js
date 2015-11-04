$(function() {
  //adopted via http://stackoverflow.com/questions/13437446/how-to-display-selected-item-in-bootstrap-button-dropdown-title
  $('.dropdown-menu li a').click(function(){
    var html = '<span class="glyphicon glyphicon-folder-open pull-left" aria-hidden="true"></span>'
    html = html + $(this).text()
    $('.dropdown-toggle').html(html);

    $('#category_id').val($(this).data('category-id'));
  });

  //via http://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
  function readPreviewImage(input) {
    if(input) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#picture').attr('src', e.target.result);
      }
      reader.readAsDataURL(input);
    }
  }
  //adopted via http://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously
  $('#picture').attr('style', 'cursor:pointer;').click(function(event) {
    $('#file').click();
  });

  $('#file').change(function(){
    var file = this.files[0];
    var name = file.name;
    var size = file.size;
    var type = file.type;
    console.log('Staged file "' + name + '"');
    readPreviewImage(file);
    //Your validation
  });
});
