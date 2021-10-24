from pylsl import StreamInfo, StreamOutlet


class Keyboard:
    def __init__(self, name="my_keyboard"):
        self.name = name
        info_key= StreamInfo(name=self.name, type='Markers', channel_count=1,
                        channel_format='string', source_id='keyPressID')
        self.outlet_key = StreamOutlet(info_key)

    def stream_keypress(self, keyboard_obj):
        if (keyboard_obj.keys):
            self.outlet_key.push_chunk([keyboard_obj.keys])


class Mouse:
    def __init__(self, name="my_mouse", clickable_object = True, position = True, click_type = True):
        self.name = name
    
        if clickable_object:
            info_mouse_click= StreamInfo(name=self.name + "_Click", type='Markers', channel_count=1,
                            channel_format='string', source_id='mouseClickID')
            self.outlet_mouse_click = StreamOutlet(info_mouse_click)

        if position:
            info_mouse_pos= StreamInfo(name=self.name + "_Pos", type='Coordinates', channel_count=2,
                            channel_format='float32', source_id='mousePosID')
            self.outlet_mouse_pos = StreamOutlet(info_mouse_pos)

        if click_type:
            info_mouse_type= StreamInfo(name=self.name + "_Type", type='click', channel_count=1,
                            channel_format='string', source_id='mouseClickTypeID')
            self.outlet_mouse_type = StreamOutlet(info_mouse_type)
    
    def stream_clicktype(self, mouse_obj):
        mouse_click_stream = mouse_obj.getPressed()
        
        list_mouse_type = []
        if mouse_click_stream[0]:
            list_mouse_type.append("Left")
        if mouse_click_stream[1]:
            list_mouse_type.append("Middle")
        if mouse_click_stream[2]:
            list_mouse_type.append("Right")

        mouse_click_stream = ","
        mouse_click_stream = mouse_click_stream.join(list_mouse_type)

        
        self.outlet_mouse_type.push_chunk([mouse_click_stream])

    def stream_click(self, mouse_obj):
        if (mouse_obj.clicked_name):
            self.outlet_mouse_click.push_chunk(mouse_obj.clicked_name)
        else:
            self.outlet_mouse_click.push_chunk([""])

    def stream_pos(self, mouse_obj):
        X=mouse_obj.x[-1]
        Y=mouse_obj.y[-1]

        self.outlet_mouse_pos.push_chunk([X, Y])

class Gamepad:
    def __init__(self, name="my_gamepad"):
        self.name = name
        info_gamepad= StreamInfo(name=self.name, type='Markers', channel_count=1,
                        channel_format='string', source_id='gamepadPressID')
        self.outlet_gamepad = StreamOutlet(info_gamepad)

    def stream_buttonpress(self, gamepad_obj):
        self.outlet_gamepad.push_chunk(gamepad_obj.keys)


class Joystick:
    def __init__(self, name="my_joystick", keypress = True, pos = True):
        self.name = name
    
        if keypress:
            info_joystick_keypress= StreamInfo(name=self.name + "_Keypress", type='Markers', channel_count=1,
                            channel_format='string', source_id='joystickKeypressID')
            self.outlet_joystick_keypress = StreamOutlet(info_joystick_keypress)

        if pos:
            info_joystick_pos= StreamInfo(name=self.name + "_Pos", type='Coordinates', channel_count=2,
                            channel_format='float32', source_id='joystickPosID')
            self.outlet_joystick_pos = StreamOutlet(info_joystick_pos)

    def stream_keypress(self, joystick_obj):

        self.outlet_joystick_keypress.push_chunk(joystick_obj.clicked_name)

    def stream_pos(self, joystick_obj):

        X=joystick_obj.getX()
        Y=joystick_obj.getY()

        self.outlet_joystick_pos.push_chunk([X, Y])
