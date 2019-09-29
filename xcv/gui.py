import os
import random
import string
from pathlib import Path
import numpy as np

# _________________ Local
import xcv.base64_icons as b64
from xcv.version import XCV_VERSION
from xcv.stats import GameSession, FifaSession, FifaMatch
from xcv.event_loop import EventLoop
# from xcv.gui_layout import GUILayout

# _________________ `pip install` _________________
import PySimpleGUIQt as sg
import cv2
from loguru import logger

def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


class GUILayout:
    def __init__(self):
        # Style settings
        self.FONT = "Helvetica 8"
        self.TEXT_COLOR = "#A6A4AF"
        self.BKG_COLOR = "#0a0a0f"
        self.GREEN = "#4e8827"
        self.YELLOW = "#a68c27"
        self.RED = "#7e2c2c"
        self.GREY = "#a6a6a6"
        self.GREY2 = "#2b2b2e"

        self.button_a = {
            "key": "_a_",
            "name": "A",
            "on_image": b64.BTN_A_ON,
            "off_image": b64.BTN_A_OFF,
        }
        self.button_b = {
            "key": "_b_",
            "name": "B",
            "on_image": b64.BTN_B_ON,
            "off_image": b64.BTN_B_OFF,
        }
        self.button_x = {
            "key": "_x_",
            "name": "X",
            "on_image": b64.BTN_X_ON,
            "off_image": b64.BTN_X_OFF,
        }
        self.button_y = {
            "key": "_y_",
            "name": "Y",
            "on_image": b64.BTN_Y_ON,
            "off_image": b64.BTN_Y_OFF,
        }
        self.button_start = {
            "key": "_start_",
            "name": "Start",
            "on_image": b64.START_ON,
            "off_image": b64.START_OFF,
        }
        self.button_select = {
            "key": "_select_",
            "key": "_select_",
            "name": "Select",
            "on_image": b64.SELECT_ON,
            "off_image": b64.SELECT_OFF,
        }
        self.button_lb = {
            "key": "_lb_",
            "name": "L Bumper",
            "on_image": b64.BTN_LB_ON,
            "off_image": b64.BTN_LB_OFF,
        }
        self.button_lt = {
            "key": "_lt_",
            "name": "L Trigger",
            "on_image": b64.BTN_LT_ON,
            "off_image": b64.BTN_LT_OFF,
        }
        self.button_rb = {
            "key": "_rb_",
            "name": "R Bumper",
            "on_image": b64.BTN_RB_ON,
            "off_image": b64.BTN_RB_OFF,
        }
        self.button_rt = {
            "key": "_rt_",
            "name": "R Trigger",
            "on_image": b64.BTN_RT_ON,
            "off_image": b64.BTN_RT_OFF,
        }
        self._all_buttons = [
            self.button_a,
            self.button_b,
            self.button_x,
            self.button_y,
            self.button_select,
            self.button_start,
            self.button_lb,
            self.button_lt,
            self.button_rb,
            self.button_rt,
        ]

    def _output_console(self):
        return [
            sg.Output(size=(640, 100), background_color="#16161F", text_color="#A6A4AF", key="_output_console_",
                      visible=False),
        ]

    def _top_status(self):
        _gui_display_info = [

            # [
            #     sg.Text("Elapsed: "),
            #     sg.Text("", key="_game_session_clock_")
            # ],
            # [
            #     sg.Text("FIFA Sess: "),
            #     sg.Text("", key="_fifa_session_clock_")
            # ],
            # [
            #     sg.Text("Match: "),
            #     sg.Text("", key="_fifa_match_clock_")
            # ],
            # [
            #     sg.Text("Countdown: "),
            #     sg.Text("", key="_command_countdown_")
            # ],
            # [
            #     sg.Text("", key="_elapsed_", pad=(0, 0), tooltip="Elapsed"),
            # ],
            # [
            #     sg.Text("Clock:"),
            #     sg.Image(filename="", key="_output_frame_"),
            #     sg.Image(filename="", key="_output_frame2_"),
            #     sg.Image(filename="", key="_output_frame3_"),
            #     sg.Image(filename="", key="_output_frame4_"),
            # ],
            # [
            #     sg.Text("Score:"),
            #     sg.Image(filename="", key="_output_frame5_"),
            #     sg.Image(filename="", key="_output_frame6_"),
            # ],
        ]

        _serial_connection_info = [[]]

        return [
            sg.Column(_serial_connection_info),
            sg.Column(_gui_display_info),
        ]

    def _video_frame(self):
        return [sg.Image(filename="", key="_video_frame_")]

    def _detected_state(self):
        return [sg.Text(" ",
                        key="_detected_state_",
                        font="Helvetica 16",
                        justification="center", )
                ]

    def _detected_substate(self):
        return [
            sg.Column([[sg.Image(data_base64=b64.FILM_GREY, key="_fps_icon_",
                                 tooltip="FPS")],
                       [sg.Text("", key="_opencv_fps_", visible=False, justification="left", tooltip="FPS")]]),
            sg.Text(
                "No Connection",
                key="_gamepad_usb_port_",
                pad=(0, 0),
                text_color=self.TEXT_COLOR,
                justification="left",
            ),
            sg.Text(" ", key="_screen_side_"),
            sg.Text("", key="_home_away_"),
        ]

    def _vert_spacer(self):
        return [sg.Image(data_base64=b64.VERT_SPACER)]

    def _gui_work_area(self):
        _gui_menu = [
            [sg.Image(data_base64=b64.MENU_OFF, key="_menu_icon_", tooltip="Show/Hide Menu", visible=True,
                      pad=((0, 5), 2), enable_events=True)],
            [sg.Image(data_base64=b64.POWER_ON, key="_use_cv_", visible=False, pad=((0, 5), 2),
                      enable_events=True, tooltip="OpenCV On/Off")],
            [sg.Image(data_base64=b64.CONTROLLER_OFF, key="_gamepad_connection_status_", visible=False,
                      pad=((0, 5), 2), enable_events=True, tooltip="Controller IO")],
            [sg.Image(data_base64=b64.TROPHY_OFF, key="_trophy_icon_", visible=False, pad=((0, 5), 2),
                      enable_events=True, tooltip="Game Stats")],
            [sg.Image(data_base64=b64.PIE_CHART_OFF, key="_pie_chart_icon_", visible=False, pad=((0, 5), 2),
                      enable_events=True, tooltip="Data Analysis (Long-Term)")],
            [sg.Image(data_base64=b64.CCTV_ON, key="_cctv_", visible=False, pad=((0, 5), 2),
                      enable_events=True, tooltip="Show/Hide Video")],
            [sg.Image(data_base64=b64.INFO_OFF, key="_info_icon_", visible=False, pad=((0, 5), 2),
                      tooltip="XCV Info", enable_events=True)],
            [sg.Image(data_base64=b64.EXIT_OFF, key="_EXIT_", visible=False, pad=(0, 0), enable_events=True,
                      tooltip="Close XCV")],
        ]

        _xcontroller_action_buttons = [
            [
                sg.Image(
                    data_base64=self.button_y["off_image"],
                    key="_y_",
                    enable_events=True,
                    pad=(35, 0, 0, 0),
                    visible=False,
                )
            ],
            [
                sg.Image(
                    data_base64=self.button_x["off_image"],
                    key="_x_",
                    enable_events=True,
                    pad=(5, 0, 0, 0),
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_b["off_image"],
                    key="_b_",
                    enable_events=True,
                    pad=(0, 0, 0, 0),
                    visible=False,
                ),
            ],
            [
                sg.Image(
                    data_base64=self.button_a["off_image"],
                    key="_a_",
                    enable_events=True,
                    pad=(35, 0, 0, 0),
                    visible=False,
                )
            ],
        ]

        _xcontroller_dpad = [
            [
                sg.Image(
                    data_base64=b64.DU_WHITE,
                    key="_du_",
                    enable_events=True,
                    pad=(80, 0, 0, 0),
                    visible=False,
                )
            ],
            [
                sg.Image(
                    data_base64=b64.DL_WHITE,
                    key="_dl_",
                    enable_events=True,
                    pad=(50, 0, 0, 0),
                    visible=False,
                ),
                sg.Image(
                    data_base64=b64.DR_WHITE,
                    key="_dr_",
                    enable_events=True,
                    pad=(0, 0, 0, 0),
                    visible=False,
                ),
            ],
            [
                sg.Image(
                    data_base64=b64.DU_WHITE,
                    key="_dd_",
                    enable_events=True,
                    pad=(80, 0, 0, 0),
                    visible=False,
                )
            ],
        ]

        _xcontroller_other = [
            [
                sg.Image(
                    data_base64=self.button_lt["off_image"],
                    key="_lt_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=b64.XBOX_LOADING,
                    key="_xbox_",
                    enable_events=True,
                    pad=(16, 16, 0, 0),
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_rt["off_image"],
                    key="_rt_",
                    enable_events=True,
                    visible=False,
                ),
            ],
            [
                sg.Image(
                    data_base64=self.button_lb["off_image"],
                    key="_lb_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_start["off_image"],
                    key="_start_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_select["off_image"],
                    key="_select_",
                    enable_events=True,
                    visible=False,
                ),
                sg.Image(
                    data_base64=self.button_rb["off_image"],
                    key="_rb_",
                    enable_events=True,
                    visible=False,
                ),
            ],
        ]

        return [sg.Column(_gui_menu),

                # sg.Column(_gui_display_info),
                sg.Column(_xcontroller_dpad),
                sg.Column(_xcontroller_other),
                sg.Column(_xcontroller_action_buttons),
                ]

    def _layout(self):
        # define the window layout
        _full_layout = [
            self._vert_spacer(),
            self._detected_state(),
            self._detected_substate(),
            self._video_frame(),
            self._gui_work_area(),
            self._output_console(),
            self._vert_spacer(),
        ]
        return _full_layout

    def full_layout(self):
        return self._layout()


@logger.catch()
class GUI:
    
    def __init__(self, gui=True):
        self.game_session = GameSession()

        path = Path(__file__).resolve().parent
        self.clock_image_path = path / "output/scoreboard/clock"
        self.score_image_path = path / "output/scoreboard/score"

        # Style settings
        self.FONT = "Helvetica 8"
        self.TEXT_COLOR = "#A6A4AF"
        self.BKG_COLOR = "#0a0a0f"

        if gui:
            sg.SetOptions(
                scrollbar_color=None,
                text_color=self.TEXT_COLOR,
                font=self.FONT,
                element_padding=(0, 0),
                background_color=self.BKG_COLOR,
                message_box_line_width=0,
                text_justification="left",
                margins=(0, 0),
                border_width=0,
            )

            _gui_layout = GUILayout()

            self.window = sg.Window(
                f"XCV - {XCV_VERSION}",
                layout=_gui_layout.full_layout(),
                location=(600, 200),
                icon=b64.Microsoft_Xbox_Emoji_Icon,
                border_depth=0,
            )

        EventLoop().event_loop(gui_window=self.window)

    # def scoreboard_processor(self, gray_frame, save=False):
    #     _clock_y1 = 92
    #     _clock_y2 = 100

    #     _digit1_x1 = 36
    #     _digit1_x2 = 41
    #     _digit2_x1 = 41
    #     _digit2_x2 = 46
    #     _digit3_x1 = 49
    #     _digit3_x2 = 54
    #     _digit4_x1 = 54
    #     _digit4_x2 = 59

    #     _score_y1 = 92
    #     _score_y2 = 101

    #     _score1_x1 = 117
    #     _score1_x2 = 123

    #     _score2_x1 = 128
    #     _score2_x2 = 134
    #     roi_game_clock_digit1 = gray_frame[_clock_y1:_clock_y2, _digit1_x1:_digit1_x2]

    #     roi_game_clock_digit2 = gray_frame[_clock_y1:_clock_y2, _digit2_x1:_digit2_x2]

    #     roi_game_clock_digit3 = gray_frame[_clock_y1:_clock_y2, _digit3_x1:_digit3_x2]
    #     roi_game_clock_digit4 = gray_frame[_clock_y1:_clock_y2, _digit4_x1:_digit4_x2]

    #     roi_game_score1_digit1 = gray_frame[_score_y1:_score_y2, _score1_x1:_score1_x2]
    #     roi_game_score2_digit1 = gray_frame[_score_y1:_score_y2, _score2_x1:_score2_x2]

    #     if save:
    #         filename = random_string() + ".png"

    #         cv2.imwrite(
    #             os.path.join(self.clock_image_path, filename), roi_game_clock_digit1
    #         )
    #         cv2.imwrite(
    #             os.path.join(self.clock_image_path, filename), roi_game_clock_digit2
    #         )
    #         cv2.imwrite(
    #             os.path.join(self.clock_image_path, filename), roi_game_clock_digit3
    #         )
    #         cv2.imwrite(
    #             os.path.join(self.clock_image_path, filename), roi_game_clock_digit4
    #         )

    #         cv2.imwrite(
    #             os.path.join(self.score_image_path, filename), roi_game_score1_digit1
    #         )
    #         cv2.imwrite(
    #             os.path.join(self.score_image_path, filename), roi_game_score2_digit1
    #         )
        #
        # cropped_imgbytes = cv2.imencode(".png", roi_game_clock_digit1)[1].tobytes()
        # cropped_imgbytes2 = cv2.imencode(".png", roi_game_clock_digit2)[1].tobytes()
        # cropped_imgbytes3 = cv2.imencode(".png", roi_game_clock_digit3)[1].tobytes()
        # cropped_imgbytes4 = cv2.imencode(".png", roi_game_clock_digit4)[1].tobytes()
        # cropped_imgbytes5 = cv2.imencode(".png", roi_game_score1_digit1)[1].tobytes()
        # cropped_imgbytes6 = cv2.imencode(".png", roi_game_score2_digit1)[1].tobytes()
        #
        # self.window.Element("_output_frame_").Update(data=cropped_imgbytes)
        # self.window.Element("_output_frame2_").Update(data=cropped_imgbytes2)
        # self.window.Element("_output_frame3_").Update(data=cropped_imgbytes3)
        # self.window.Element("_output_frame4_").Update(data=cropped_imgbytes4)
        # self.window.Element("_output_frame5_").Update(data=cropped_imgbytes5)
        # self.window.Element("_output_frame6_").Update(data=cropped_imgbytes6)


if __name__ == "__main__":
    gui = GUI()
