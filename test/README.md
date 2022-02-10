Follow the steps to ensure the application correctly handle format errors and encrypted files.

### Incorrect PDF file

* open [empty.pdf](./empty.pdf) in the application
* the application should raise a pop-up window showing something about `format error` rather than exit

### Incorrect image file

* open [empty.jpg](./empty.jpg) in the application
* the application should raise a pop-up window showing something about `format error` rather than exit

### Encrypted file

* open [pw.pdf](./pw.pdf) in the application
* there should be a pop-up window asking for password
* type `123` into it
* the pop-up window should remain here
* type `1234567890` into it
* the pop-up window should disappear and the file should have been opened in the application