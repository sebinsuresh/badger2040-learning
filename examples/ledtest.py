import badger2040
import time

badger = badger2040.Badger2040()

# Gamma-adjusted brightness - applied on top of adjustments made by library.
gamma = 2.2
def set_adjusted_led(val):
    clamp(val, 0, 255)
    badger.led(255 * ((val / 255) ** gamma))
    return val
    #badger.led(val)
    #return val

# Clamp values between given min_ and max_ values
def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val

# Button handling 

some_btn_pressed = False

# This has to run first
def set_btn_status_start():
    global some_btn_pressed
    if not badger.pressed_any():
        some_btn_pressed = False

# This has to run last
def set_btn_status_end():
    global some_btn_pressed
    if badger.pressed_any():
        some_btn_pressed = True

def process_btn_check(specific_pressed_result):
    global some_btn_pressed
    return_val = (not some_btn_pressed) and specific_pressed_result
    return return_val

def is_a_pressed():
    return process_btn_check(badger.pressed(badger2040.BUTTON_A))

def is_b_pressed():
    return process_btn_check(badger.pressed(badger2040.BUTTON_B))

def is_c_pressed():
    return process_btn_check(badger.pressed(badger2040.BUTTON_C))

def is_up_pressed():
    return process_btn_check(badger.pressed(badger2040.BUTTON_UP))

def is_down_pressed():
    return process_btn_check(badger.pressed(badger2040.BUTTON_DOWN))

# Increase/decrease brightness using buttons

brightness = 127
set_adjusted_led(brightness)

# used elsewhere
ui_updated = True
needs_full_ui_update = True

def process_led_adjustments():
    global brightness
    global ui_updated
    global ui_updated_region
    
    prev_brightness = brightness
    
    if is_a_pressed():
        brightness = brightness - 50
    elif is_c_pressed():
        brightness = brightness + 50
    elif is_up_pressed():
        brightness = brightness + 10
    elif is_down_pressed():
        brightness = brightness - 10
    brightness = clamp(brightness, 0, 255)
    
    if brightness != prev_brightness:
        brightness = set_adjusted_led(brightness)
        print("brightness: " + str(brightness))
        ui_updated = True
    else:
        ui_updated = False

def update_ui():
    global ui_updated
    global needs_full_ui_update

    if not needs_full_ui_update and ui_updated:
        badger.set_update_speed(badger2040.UPDATE_TURBO)
        badger.set_pen(15)
        badger.clear()
        badger.set_pen(0)
        badger.set_font("bitmap8")
        badger.text(str(brightness), 8, 56, scale=2)
        badger.partial_update(8, 56, 32, 24)

    if needs_full_ui_update:
        badger.set_update_speed(badger2040.UPDATE_MEDIUM)
        
        # clear screen
        badger.set_pen(15)
        badger.clear()
        
        # write text
        badger.set_pen(0)
        badger.set_font("bitmap8")
        badger.text("Hello badger!", 8, 8, scale=2)
        badger.text("Current LED brightness:", 8, 32, scale=2)
        badger.text(str(brightness), 8, 56, scale=2)
        
        # create button labels
        badger.set_font("bitmap6")
        badger.text("decrease", 20, badger2040.HEIGHT - 24, scale=1)
        badger.text("50", 20 + 16, badger2040.HEIGHT - 16, scale=1)
        badger.triangle(35, badger2040.HEIGHT - 8, 45, badger2040.HEIGHT - 8, 40, badger2040.HEIGHT)
        
        badger.text("refresh", 130, badger2040.HEIGHT - 16, scale=1)
        badger.triangle(142, badger2040.HEIGHT - 8, 152, badger2040.HEIGHT - 8, 147, badger2040.HEIGHT)
        
        badger.text("increase", 230, badger2040.HEIGHT - 24, scale=1)
        badger.text("50", 230 + 18, badger2040.HEIGHT - 16, scale=1)
        badger.triangle(248, badger2040.HEIGHT - 8, 258, badger2040.HEIGHT - 8, 253, badger2040.HEIGHT)
        
        badger.text("increase", badger2040.WIDTH - 52, 20, scale=1)
        badger.text("10", badger2040.WIDTH - 20, 30, scale=1)
        badger.triangle(badger2040.WIDTH - 10, 25, badger2040.WIDTH - 10, 35, badger2040.WIDTH, 30)
        
        badger.text("decrease", badger2040.WIDTH - 54, 85, scale=1)
        badger.text("10", badger2040.WIDTH - 20, 95, scale=1)
        badger.triangle(badger2040.WIDTH - 10, 90,badger2040.WIDTH - 10, 100, badger2040.WIDTH, 95)
        
        # refresh
        badger.update()
        needs_full_ui_update = False

# Add code here
def loop():
    global needs_full_ui_update
    
    process_led_adjustments()

    if is_b_pressed():
        needs_full_ui_update = True
    

# handle input, ui
while True:
    set_btn_status_start()
    loop()
    update_ui()
    set_btn_status_end()
    time.sleep(0.1)

