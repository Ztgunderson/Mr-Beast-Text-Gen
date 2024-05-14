from google.cloud import speech_v1p1beta1 as speech
import os
import io

def transcribe_audio_file_with_timestamps(file_path):
    client = speech.SpeechClient()

    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        with open('transcript.txt', 'w') as f:
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time

                print(
                    f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
                )
                f.write(f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}\n")


def convert_transcript_to_srt(transcript_file, srt_file):
    with open(transcript_file, "r") as f, open(srt_file, "w") as out:
        i = 1
        for line in f:
            # Extract word and timestamps
            word_info = line.strip().split(", ")
            word = word_info[0].split(": ")[1]
            start_time = float(word_info[1].split(": ")[1])
            end_time = float(word_info[2].split(": ")[1])

            # Convert timestamps to SRT format
            start_time_srt = convert_to_srt_time(start_time)
            end_time_srt = convert_to_srt_time(end_time)

            # Write to output file
            out.write(f"{i}\n{start_time_srt} --> {end_time_srt}\n{word}\n\n")
            i += 1

def convert_to_srt_time(time_in_seconds):
    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int((seconds - int(seconds))*1000):03}"

# specify the path to your audio file
transcribe_audio_file_with_timestamps("/Mr Beast Text Gen/input.wav")

# use the function
convert_transcript_to_srt("/Mr Beast Text Gen/transcript.txt", "/Mr Beast Text Gen/script.srt")
