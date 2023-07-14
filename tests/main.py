from os import getenv
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = getenv('OPENAI_TOKEN')

context = [
    {'role': 'user', 'content': '''

use std::fs;
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::thread;
use std::env;

fn search_files(directory: &str, search_term: Arc<String>) -> Vec<PathBuf> {
    let paths = Arc::new(Mutex::new(Vec::new()));
    let search_term_inner = search_term.clone();

    let walker = fs::read_dir(directory).expect("Failed to read directory");

    let handles: Vec<_> = walker
        .filter_map(|entry| {
            let entry = entry.ok()?;
            let path = entry.path();
            if path.is_dir() {
                return Some(thread::spawn(move || search_files(&path.to_string_lossy(), search_term_inner.clone())));
            }
            if path.is_file() {
                let term = search_term_inner.clone();
                let paths_clone = paths.clone();
                Some(thread::spawn(move || {
                    if fs::read_to_string(&path)
                        .unwrap()
                        .to_lowercase()
                        .contains(&term.to_lowercase())
                    {
                        paths_clone.lock().unwrap().push(path.clone());
                    }
                    paths_clone
                }) as thread::JoinHandle<_>)
            } else {
                None

 }
        })
        .collect();

    let mut results = Vec::new();
    for handle in handles {
        let result = handle.join().expect("Failed to join thread");
        results.extend(result.lock().unwrap().clone());
    }

    results
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() < 2 {
        println!("Usage: ./file_search <directory> <search_term>");
        return;
    }
    let search_directory = &args[0];
    let search_term = Arc::new(args[1].to_owned());
    let found_files = search_files(search_directory, search_term.clone());
    println!("Found {} file(s):", found_files.len());
    for file in found_files {
        println!("{}", file.display());
    }
}

error[E0599]: no method named `lock` found for struct `Vec<PathBuf>` in the current scope
  --> src\main.rs:44:31
   |
44 |         results.extend(result.lock().unwrap().clone());
   |                               ^^^^ method not found in `Vec<PathBuf>`

error[E0605]: non-primitive cast: `JoinHandle<Arc<Mutex<Vec<PathBuf>>>>` as `JoinHandle<Vec<PathBuf>>`
  --> src\main.rs:24:22
   |
24 |                   Some(thread::spawn(move || {
   |  ______________________^
25 | |                     if fs::read_to_string(&path)
26 | |                         .unwrap()
27 | |                         .to_lowercase()
...  |
32 | |                     paths_clone
33 | |                 }) as thread::JoinHandle<_>)
   | |___________________________________________^ an `as` expression can only be used to convert between primitive types or to coerce to a specific trait object

готовый код, без описания
'''}
]

print(
    openai.ChatCompletion.create(
        n=1,
        temperature=0,
        model='gpt-3.5-turbo',
        messages=context
    )
)
