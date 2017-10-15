
Dropzone.options.mainDropzone = {
    previewTemplate: '<div class="dz-preview dz-file-preview">' +
'  <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>' +
'  <div class="dz-details">' +
'    <div class="dz-filename">' +
'    <span data-dz-name></span> (<span class="dz-size" data-dz-size></span>)' +
'    </div>' +
'  </div>' +
'  <div class="dz-error-message"><span data-dz-errormessage></span></div>' +
'</div>',
    init: function() {
        this.on('sending', function(file, xhr, formData) {
            xhr.responseType = 'blob';
        });
        this.on("success", function(file, result) {
            // this trick courtesy of http://www.alexhadik.com/blog/2016/7/7/l8ztp8kr5lbctf5qns4l8t3646npqh
            var a = document.createElement("a");
            a.style = 'display: none';
            document.body.appendChild(a);
            // Create a DOMString representing the blob and point the link element towards it
            var url = window.URL.createObjectURL(result);
            a.href = url;
            var extIndex = file.name.lastIndexOf('.')
            a.download = extIndex == -1
                ? file.name + '-notimestamps'
                : file.name.substring(0, extIndex) + '-notimestamps' + file.name.substring(extIndex)
            // programatically click the link to trigger the download
            a.click();
            window.URL.revokeObjectURL(url);
        });
    }
}
