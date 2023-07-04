// parse send-data button
document.querySelector('#send-data').onclick = myDataClick;

function myDataClick () {
	var data = document.getElementById('data').value

	if (data != '') {
		console.log('Data: ' + data)
	}
	if (data == '') {
		console.log('Please, enter data!')
	}
}

// parse send-password button
document.querySelector('#send-password').onclick = myPasswordClick;

var paragraph = document.getElementById('p');


function myPasswordClick () {
	var password = document.getElementById('password').value;

	if (password == 'shadowraze') {
		console.log('Password: ' + password)

		paragraph.innerHTML = 'Correct password!';
		paragraph.style.color = '#50ED31'

		document.querySelector('#send-data').removeAttribute('disabled')

		document.getElementById('password').value = '';
	}
if (password != 'shadowraze') {
		console.log('Please, enter correct password!')

		paragraph.innerHTML = 'Incorrect password!';
		paragraph.style.color = '#EC2222';

		document.querySelector('#send-data').setAttribute('disabled', 'true');
	}
}

// bind 'Enter' to enter data and password 
var dataInput = document.getElementById('data');

dataInput.addEventListener('keypress', function(event) {
	if (event.key == 'Enter') {
		event.preventDefault();

		document.getElementById('send-data').click();
	}
})

var passwordInput = document.getElementById('password');

passwordInput.addEventListener('keypress', function(event) {
	if (event.key == 'Enter') {
		event.preventDefault();
		document.getElementById('send-password').click();
	}
});
