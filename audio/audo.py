import pyaudio
import numpy as np

# Define constants
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Number of audio channels (1 for mono)
RATE = 44100  # Sample rate (samples per second)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def calculate_levels(data, chunk, sample_rate):
    # Convert raw data to numpy array
    data = np.frombuffer(data, dtype=np.int16)
    
    # Apply FFT (Fast Fourier Transform) to get frequency spectrum
    fft_data = np.fft.fft(data)
    
    # Get magnitude of frequencies
    freqs = np.abs(fft_data[:chunk // 2]) * 2 / (128 * chunk)
    
    # Get the frequency index with the highest magnitude
    max_freq = np.argmax(freqs)
    
    # Normalize the frequency index to a range of 0-255 for RGB control
    rgb_value = int((max_freq / (chunk // 2)) * 255)
    
    return rgb_value

try:
    while True:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        
        # Calculate the RGB value based on the audio frequency
        rgb_value = calculate_levels(data, CHUNK, RATE)
        
        # Set the keyboard RGB color based on the calculated value
        # This is a placeholder for the actual code to control your keyboard's RGB
        # Replace this with the appropriate SDK/API call
        print(f"RGB Value: {rgb_value}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()
