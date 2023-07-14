use std::thread;
use std::time::Duration;
use hound::{WavReader, Error};
use kira::{
    manager::{
        AudioManager, AudioManagerSettings,
        backend::DefaultBackend,
    },
    sound::static_sound::{StaticSoundData, StaticSoundSettings},
};


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let wav_file_path = "test_kira.wav";

    let mut manager = AudioManager::<DefaultBackend>::new(AudioManagerSettings::default())?;
    let sound_data = StaticSoundData::from_file(&wav_file_path, StaticSoundSettings::default())?;

    manager.play(sound_data.clone())?;
    manager.play(sound_data.clone())?;

    match get_wav_duration(wav_file_path) {
        Ok(duration) => {
            println!("{}", duration);
            thread::sleep(Duration::from_secs(duration as u64));
        }
        Err(err) => println!("{}", err)
    }

    Ok(())
    
}


fn get_wav_duration(file_path: &str) -> Result<f32, Error> {
    let wav_reader = WavReader::open(file_path)?;
    let duration = wav_reader.duration() as f32 / wav_reader.spec().sample_rate as f32;
    Ok(duration)
}
