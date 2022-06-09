/**
     * Gets dataURL (base64 data) from the given file or blob.
     * Technically wraps FileReader.readAsDataURL in Promise.
     *
     * @param {Blob|File} file
     * @returns {Promise} resolved with the dataURL, or rejected if the file is
     *  empty or if an error occurs.
     */
function getDataURLFromFile (file) {
    if (!file) {
        return Promise.reject();
    }
    return new Promise(function (resolve, reject) {
        var reader = new FileReader();
        reader.addEventListener('load', function () {
            resolve(reader.result);
        });
        reader.addEventListener('abort', reject);
        reader.addEventListener('error', reject);
        reader.readAsDataURL(file);
    });
}

class FileUploader {
    constructor() {
        this.useFileAPI = !!window.FileReader;
        if (!this.useFileAPI) {
            var self = this;
            this.fileupload_id = 'o_fileupload';
            $(window).on(this.fileupload_id, function () {
                var args = [].slice.call(arguments).slice(1);
                self.on_file_uploaded.apply(self, args);
            });
        }

       this.fileInput = document.getElementById('formFileMultiple');
       this.formButton = document.getElementById('formButton');
       this.messagePar = document.getElementById('message');
       this.fileInput.addEventListener('change', (e) => this.on_file_change(e))
       this.formButton.addEventListener('click', (e) => this.on_submit(e))
       this.files = [];
    }
    on_file_change (e) {
        var self = this;
        var file_node = e.target;
        var file = file_node.files[0];
        if (this.useFileAPI) {
            getDataURLFromFile(file).then(function (data) {
                    data = data.split(',')[1];
                    self.files.push({ size: file.size, name: file.name, type: file.type, data})
                });
        }
    }

    on_submit(e) {
        e.stopPropagation();
        e.preventDefault();
        if (!this.files.length) {
            return;
        }
        self = this;
        self.formButton.disabled = true;
        self.messagePar.innerText = 'Uploading ...'
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: JSON.stringify({ files: this.files }),
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then((result) =>{
            self.messagePar.innerText = 'The files have been sent.';
            self.formButton.disabled = false;
          }
          ).catch((error) => {
            self.messagePar.innerText = 'There was an error during the uploading process.';
          });
    }
}

const fileUploader = new FileUploader();
