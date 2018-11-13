import time
import audioio
import board
import digitalio

# list all samples here
short_sample = audioio.WaveFile(open("kick.wav", "rb"))
long_sample = audioio.WaveFile(open("pad3mini.wav", "rb"))

# list all input buttons here
button = digitalio.DigitalInOut(board.D3)

# initialize speaker output pin
audio_pin = audioio.AudioOut(board.A0)
   
# initialize all buttons in the list   
button.switch_to_input(pull=digitalio.Pull.UP)

# test all buttons
print("Test Buttons")

print("Push the button.")
while button.value:
    pass
    
print("All buttons work.")

# create mixer object with the number of voices required
mixer = audioio.Mixer(voice_count=2,
                      sample_rate=22050,
                      channel_count=1,
                      bits_per_sample=16,
                      samples_signed=True)

# start outputing the mixer to the DAC
audio_pin.play(mixer)

pad_length = 8.00
start_time = time.monotonic()
mixer.play(long_sample, voice=0)
    
# main body loop
# check buttons and play sample in mixer
while True:
    if time.monotonic() > (start_time + pad_length):
        start_time = time.monotonic()
        mixer.play(long_sample, voice=0) 
       

    if not button.value:
        mixer.play(short_sample, voice=1)
        print("Playing sample.")
    else:
        print("Silence")
        
    # debounce delay
    time.sleep(0.1)
    