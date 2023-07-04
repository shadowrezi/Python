document.querySelector('#send-data').onclick = myDataClick;


function myDataClick () {
    var data = document.getElementById('data').value;
    console.log('Data: ' + data);

}


document.querySelector('#send-password').onclick = myPasswordClick;


function myPasswordClick () {
    var password = document.getElementById('password').value;

console.log('Password: ' + password);
    if (password == 'shadowraze') {
        document.querySelector('#paragraph').innerHTML = 'Password is correct!';
        document.querySelector('#paragraph').style.color = '#13ec48';

        document.querySelector('#send-data').removeAttribute('disabled');
    }
    if (password != 'shadowraze') {
        document.querySelector('#paragraph').innerHTML = 'Password is incorrect!';
        document.querySelector('#paragraph').style.color = '#e22b14';

        document.querySelector('#send-data').setAttribute('disabled', 'true');
    }

}