# boot.py - adapted for "not mounting drive unless ESC is held at plug-in"
import board
import digitalio
import supervisor
import storage
import usb_cdc
import usb_hid
import usb_midi
import microcontroller

# Optional stack limit for deep recursion or extra memory, if needed
# supervisor.set_next_stack_limit(4096 + 4096)

# Set a custom USB identification (as you did in your original code)
supervisor.set_usb_identification("Pog", "Pog Keyboard")

# Enable both console & data on USB_CDC by default
# (We will *disable* them if the key is NOT held, below.)
usb_cdc.enable(console=True, data=True)

# ------------------------------------------------------------------------
# Key-matrix pins: COL1 = board.GP28, ROW1 = board.GP0
# We drive ROW low and read COL; if the key is pressed, COL goes LOW.
# Pressed key => COL.value == False
# Not pressed => True
# ------------------------------------------------------------------------
COL = digitalio.DigitalInOut(board.GP28)
COL.switch_to_input(pull=digitalio.Pull.UP)

ROW = digitalio.DigitalInOut(board.GP0)
ROW.switch_to_output(value=False, drive_mode=digitalio.DriveMode.PUSH_PULL)

# If the key is *not* pressed (COL==True), we disable the drive & CDC.
# That way, you only get a USB HID device (keyboard), no REPL or drive.
# Pressing the key at startup means the drive is available for dev work.
if COL.value:
    storage.disable_usb_drive()      # Hide the CircuitPython drive
    usb_cdc.disable()                # Disable the CDC REPL & data ports
    usb_midi.disable()               # Disable MIDI if you don't need it
    usb_hid.enable(boot_device=1)    # Enable HID only

# Clean up the pins
COL.deinit()
ROW.deinit()

