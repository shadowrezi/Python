// *time of program

use std::time::Instant;

let start = Instant::now();

	*Body*

let duration = start.elapsed();


// *generate fully security password
fn generate_password(length: usize) -> String {
	let chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	let mut rng = rand::thread_rng();
	let password: String = (0..length).map(|_| {
		let idx = rng.gen_range(0..chars.len());
		chars.chars().nth(idx).unwrap()
	}).collect();
	
	return password;
}

// *write in file
use std::io::Write;

let mut file = std::fs::File::create("number.txt").expect("Error: 5");

file.write_all(<Object>.as_bytes()).expect("Error: 37");
