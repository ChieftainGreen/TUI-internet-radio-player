"""
Internet radio player with Textual interface.  
To edit the radiostation list, modify STATIONLIST below.  
Not all stream types are working, unfortunately.  
pls/m3u/etc playlists not supported. Only mp3 streams accepted.  

HOW TO RUN:  
run "pip install requriements.txt" (miniaudio, textual)  
run "python main.py"  

recommended Windows Terminal  

TODO - remove 'STATIC' text, make screenshot with actual song  
TODO - next and previous buttons  

TODO - histogram for the audio stream. Don't know how to start  
seems miniaudio has no such option? or something like  DecodedSoundFile?  
maybe from the system volume/mixer?  
for display, maybe sparkines?  

TODO - while no histogram, make 'press/event' indicator there  

"""

import miniaudio
import os

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, HorizontalScroll, ScrollableContainer, Binding

from textual.widgets import Footer, Header, Static, Button, ListView, ListItem, Label, Log
import time
import threading #do miniaudio really needs that? I forgot.

NAME = "TUI-internet-radio-player"
VERSION = "0.7"
STATIONLIST = ["http://stream.syntheticfm.com:8040/live",
               "https://stream.nightride.fm/nightride.mp3",
               #"http://85.234.59.191:8000/stream",
               "http://www.partyviberadio.com:8010/listen.stream",
               "http://uk6.internet-radio.com:8428/stream",
               "http://uk4.internet-radio.com:8049/stream",
               "https://my.radioprocessor.com:8100/best_trance-320.mp3",
               "https://listen10.myradio24.com/atmo"
               ]
#stop_flag = False
playing_flag = False
device = None
stream = None
source = None

def compose_id_strings(STATIONLIST):
    id_string_list = []
    for count,_ in enumerate(STATIONLIST):
        id_string_list.append("ID"+str(count))
    return id_string_list

class Panel(VerticalScroll):
    """panel with buttons and play timer"""
    def compose(self) -> ComposeResult:
        yield HorizontalScroll(
            Button("Previous(B)", id="prev", variant="success"),
            Button("Play(P)", id="start", variant="success"),
            Button("Next(N)", id="next", variant="success"),
            Button("Stop(S)", id="stop", variant="error"),
            id="buttonbar",
            )
        with Horizontal(id = "top4_bottom_text_etc"):
            yield Static("STATIC", id="display")
            yield Static("reserved for HISTOGRAM / check Sparkline", id="histogram")


class ListOfUrls(Container):
    def compose(self) -> ComposeResult:
        global STATIONLIST  # probably not the right thing TODO need to think it in the morning
                            # how to pass variable to Textual compose method???
        global id_strings_list
        self.styles.height = len(STATIONLIST) #height of Container Widget
                                            #why there is 'ListOfUrls'Container around ListView?
                                            #don't know|remember.
        list_of_items = []
        for count,station in enumerate(STATIONLIST):
            list_of_items.append(ListItem(Static(station, id = "ID"+str(count))))
            #id = ID0, ID1, etc. Can't start with number.
        yield ListView(*list_of_items, id = "listofurls")

class Player(App):
    CSS_PATH = "main.tcss"
    TITLE = NAME
    BINDINGS = [
        #("e", "edit_list", "Edit playlist"), #TODO REMOVE
        Binding("p", "play", "Play"),
        Binding("q", "quit", "Quit"),
        Binding("s", "stop", "Stop"),
        #enter is not shown in the footer, so display substitute with random alt-ctrl-f3
        Binding("alt-ctrl-F3", "dummy", "Play/Stop", show = True,
                key_display="ENTER"),
        Binding("enter", "enter_key", "Play/Stop", show = True,
                priority=True,
                key_display="ENTER"),
    ]

    def play_radio(self,selected_station_url):
        #global stop_flag
        global playing_flag
        global device
        global stream
        global source

        #stop_flag = False
        playing_flag = True

        source = miniaudio.IceCastClient(selected_station_url)
        time.sleep(1)
        self.print_stream_info_strings(source)
        stream = miniaudio.stream_any(source)#, source.audio_format)

        device = miniaudio.PlaybackDevice()
        device.start(stream)
        while stop_flag == False:
            time.sleep(2)
            self.print_stream_info_strings(source)

    def print_stream_info_strings(self, source):
        """takes stream from miniaudio->play_radio and makes a string with text info"""

        s1 = "Audio format: " + str(source.audio_format.name)
        s2 = "Station name: " + str(source.station_name)
        s3 = "Station genre: " + str(source.station_genre)
        s4 = "Song title: " + str(source.stream_title)
        display_title = "\n".join((s1, s2, s3, s4))

        diplay_update = self.query_one("#display")
        diplay_update.update(renderable = display_title)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "start":
            self.action_play()
        elif button_id == "stop":
            self.action_stop()
            self.logm('stop button pressed')
        elif button_id == "reset":
            pass

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        yield Header()
        with Container(id = "app-grid"):
            yield ListOfUrls(id = "top1_list_of_urls")
            with Horizontal(id="control"):
                #yield Static("HERE BE CONTROLS")
                yield ScrollableContainer(Panel(id="panel"))
        yield Footer()

    def action_play(self): #-> None:
        """Called in response to key binding."""
        # if stream is already playing - stop it
        self.action_stop()
        time.sleep(0.2)

        # check which station is selected and play it
        number_of_station = self.query_one('#listofurls').index
        selected_station_url = self.query_one("#ID"+str(number_of_station)).renderable

        #uncomment with yield Log() for debug MARK1
        self.logm(str(number_of_station) + " " + str(selected_station_url))

        audio_thread = threading.Thread(target=self.play_radio, args=(selected_station_url,))
        audio_thread.start()

    def action_quit(self):
        """Called in response to key binding."""
        self.action_stop()
        #time.sleep(0.3)
        #print ("bye bye")
        self.app.exit()
        #print ("bye bye2")

    def action_stop(self):
        self.logm("STOP pressed somehow")
        """Called in response to key binding OR button"""
        #global stop_flag
        global playing_flag
        global device
        global stream
        global source

        if device != None:
            device.close()
        if stream != None:
            stream.close()
        if source != None:
            source.close()

        #stop_flag = True
        playing_flag = False


    def action_next(self):
        """Called in response to key binding."""
        pass

    def action_previous(self):
        """Called in response to key binding."""
        pass

    def dummy(self):
        """Called in response to key binding."""
        pass

    def action_enter_key(self):
        global playing_flag
        """Called in response to key binding."""
        #if playing - stop
        if playing_flag == False:
            self.action_play()
        #if mute - play
        elif playing_flag == True:
            self.action_stop()
            #pass
        self.logm("Enter pressed" + str(playing_flag))
        #pass

    def logm(self, message):
        """log function to have one small string instead of two. Works with 'yield Log()"""
        #log = self.query_one(Log)
        #log.write_line(message)
        pass
        #log.write(message)

if __name__ == "__main__":
    id_strings_list = compose_id_strings(STATIONLIST) #make tags like #ID1 for radiostation URLs
    Player().run()
    os._exit(0) #seems brutal, but it's the only way to terminate some streams
