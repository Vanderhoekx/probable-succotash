#Real time clock uses tkinter master.after() command and a recusive function call
#Alarm Clock, allows URL links + custom title for URL, opens default webbrowser to set URL at the set time

#Written by Kelly Schmidt

from tkinter import *
from tkinter import ttk
import webbrowser
import time
import pickle

#Class for the main clock display
class MainDisplay(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.grid()
        
#Sets theme for all comboboxes
        self.tk_setPalette(background = 'bisque4', foreground = 'black')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TCombobox', fieldbackground = 'green', background = 'bisque4', foreground = 'white')

#Initialize and call any methods/attributes that need to be started on program startup
        self.hour_list = ['{:02d}'.format(num) for num in range(1, 13)]
        self.minute_list = ['{:02d}'.format(num) for num in range(60)]
        self.hours = int(time.ctime()[11:13])
        self.minutes = int(time.ctime()[14:16])
        self.seconds = int(time.ctime()[17:19])
        
        self.clock = Canvas(self)
        self.display = self.clock.create_rectangle(0, 0, 400, 500, fill = 'black')
        self.clock_time = self.clock.create_text(175, 150, fill = 'orange', font = ('Verdana', 30))
        self.date_display = self.clock.create_text(172, 100, fill = 'orange', font = ('Verdana', 30))
        self.clock.grid(row = 0, column = 0, padx = 1, pady = 5, rowspan = 10)
        
        self.alarm_widgets()
        self.main_display()
        
    def main_display(self):
        self.date_text = '{}{}'.format(time.ctime()[:8], int(time.ctime()[8:10]))
        if self.hours < 12:
            self.clock_text = '{}:{:02d}:{:02d}AM'.format(self.hours, self.minutes, self.seconds)
        else:
            self.clock_text = '{}:{:02d}:{:02d}PM'.format(self.hours, self.minutes, self.seconds)
        
        self.clock.itemconfigure(self.clock_time, text = self.clock_text)
        self.clock.itemconfigure(self.date_display, text = self.date_text )
        self.master.after(1000, self._ticker)

#updates clock for main display
    def _ticker(self):
        self.hours = int(time.ctime()[11:13])
        self.minutes = int(time.ctime()[14:16])
        self.seconds = int(time.ctime()[17:19])
        self.main_display()

#Class for the GUI widgets 
class AlarmWidgets(MainDisplay):
    def alarm_widgets(self):
        alarm_frame = Frame(self)
        alarm_frame.grid(row = 0, column = 1, columnspan = 3)
        
        self.hour_set = ttk.Combobox(alarm_frame, values = self.hour_list, width = 10)
        self.hour_set.set('Set Hour')
        self.hour_set.grid(row = 0, column =  0, padx = 2, pady = 2, sticky = 'N')
        
        self.minute_set = ttk.Combobox(alarm_frame, values = self.minute_list, width = 10)
        self.minute_set.set('Set Min.')
        self.minute_set.grid(row = 0, column = 1, padx = 2, pady = 2, sticky = 'N')
        
        self.am_pm = ttk.Combobox(alarm_frame, values = ['AM', 'PM'], width = 5)
        self.am_pm.set('AM')
        self.am_pm.grid(row = 0, column = 3, padx = 2, pady = 2, sticky = 'N' )

        self.set_alarm_btn = Button(self)
        self.set_alarm_btn['text'] = 'Set Alarm'
        self.set_alarm_btn['command'] = self.add_alarm
        self.set_alarm_btn['bg'] = 'orange'
        self.set_alarm_btn.grid(row = 1, column = 2, pady = 2, sticky = 'N')

        self.song_list = ttk.Combobox(self)
        self.song_list['width'] = 30
        self.song_list.set('Song List')
        
        try:
            with open(r'AlarmClock\alarmclock.pkl', 'rb') as songadder:
                song_adder = pickle.load(songadder)
                self.song_list['values'] = [key for key in song_adder.keys()]
        except FileNotFoundError:
            pass
        
        self.song_list.grid(row = 2, column = 1, pady = 2, columnspan = 3, sticky = 'N')

        self.add_song_btn = Button(self)
        self.add_song_btn['text'] = 'Add URL'
        self.add_song_btn['command'] = self.add_url
        self.add_song_btn['bg'] = 'orange'
        self.add_song_btn.grid(row = 6, column = 2, sticky = 'N')
        
        self.add_song_entry = Entry(self)
        self.add_song_entry['width'] = 30
        self.add_song_entry.insert(1, 'Enter URL')
        self.add_song_entry.grid(row = 5, column = 1, columnspan = 3, padx = 2, sticky = 'N')

        self.add_title_entry = Entry(self)
        self.add_title_entry['width'] = 30
        self.add_title_entry.insert(1, 'Enter URL Title')
        self.add_title_entry.grid(row = 4, column = 1, columnspan = 3, padx = 2)
        
        remove_song_btn = Button(self)
        remove_song_btn['text'] = 'Remove Song'
        remove_song_btn['command'] = self.remove_song
        remove_song_btn['bg'] = 'orange'
        remove_song_btn.grid(row = 3, column = 2, sticky = 'N')

#Class that sets/clears and adds URLS to the alarm feature
class AlarmSet(AlarmWidgets):
    def add_alarm(self):
        self.clock.delete('alarmtext')
        self.clock.delete('titletext')
        alarm_hours = int(self.hour_set.get())
        alarm_minutes = int(self.minute_set.get())
        alarm_ampm = self.am_pm.get()
        
        self.title_text = self.song_list.get()[:25]
        self.alarm_text = 'Alarm: {}:{:02d}:00{}'.format(alarm_hours, alarm_minutes, alarm_ampm)
        self.title_display = self.clock.create_text(89 + len(self.title_text), 230, fill = 'cyan', font = ('Verdana', 12), tag = 'titletext')
        self.alarm_display = self.clock.create_text(105, 250, fill = 'cyan', font = ('Verdana', 15), tag = 'alarmtext')
        self.clock.itemconfigure(self.title_display, text = self.title_text)
        self.clock.itemconfigure(self.alarm_display, text = self.alarm_text)
        
        if alarm_ampm == 'PM' and alarm_hours != 12:
            alarm_hours += 12
        
        alarm_time = abs(((alarm_hours * 360 + alarm_minutes * 60) - (self.hours * 360 + self.minutes * 60) - self.seconds) * 1000)
        
        self.master.after(alarm_time, self._start_alarm)
        self.set_alarm_btn['text'] = 'Clear Alarm'
        self.set_alarm_btn['command'] = self.clear_alarm
        
    def _start_alarm(self):
        with open(r'AlarmClock\alarmclock.pkl', 'rb') as alarmurl:
            alarm_url = pickle.load(alarmurl)

#Checks if there is any text on the Canvas, if so it engages the alarm, if not (alarm was cleared) it doesnt engage the alarm            
        if self.clock.find_withtag('titletext'):
            song_url = alarm_url[self.song_list.get()]
            webbrowser.open(url = song_url, autoraise = True)          
    
    def clear_alarm(self):
        self.clock.delete("alarmtext")    
        self.clock.delete('titletext')
        self.hour_set.set('Set Hour')
        self.minute_set.set('Set Min.')
        self.am_pm.set('AM')
        self.song_list.set('Song List')
        
        self.set_alarm_btn['text'] = 'Add Alarm'
        self.set_alarm_btn['command'] = self.add_alarm

    def add_url(self):
        title_song_dict = {}
        add_url = self.add_song_entry.get()
        add_title = self.add_title_entry.get()
        title_song_dict.setdefault(add_title, add_url)
    
        try:
            with open(r'AlarmClock\alarmclock.pkl', 'rb') as songadder:
                song_adder = pickle.load(songadder)
        
            for key, value in song_adder.items():
                title_song_dict.setdefault(key, value)
        except FileNotFoundError:
            pass    

        with open(r'AlarmClock\alarmclock.pkl', 'wb') as songadder:
            pickle.dump(title_song_dict, songadder, pickle.HIGHEST_PROTOCOL)
            
        with open(r'AlarmClock\alarmclock.pkl', 'rb') as songadder:
            song_adder = pickle.load(songadder)

            self.song_list['values'] = [key for key in song_adder.keys()]
        
        self.add_song_btn['text'] = 'Clear Url'
        self.add_song_btn['command'] = self.clear_url

    def clear_url(self):
        self.add_song_entry.delete(0, END)
        self.add_title_entry.delete(0, END)
        self.add_song_entry.insert(1, 'Enter Url')
        self.add_title_entry.insert(1, 'Enter Title')
        self.add_song_btn['text'] = 'Add Url'
        self.add_song_btn['command'] = self.add_url

    def remove_song(self):
        song_selection = self.song_list.get()
        
        with open(r'AlarmClock\alarmclock.pkl', 'rb') as reader:
            reader_lines = pickle.load(reader)
            if song_selection in reader_lines:
                del reader_lines[song_selection]
        
        with open(r'AlarmClock\alarmclock.pkl', 'wb') as reader:
            pickle.dump(reader_lines, reader, pickle.HIGHEST_PROTOCOL)    
            
        self.song_list['values'] = list(reader_lines.keys())
        self.song_list.set('Song List')

root = Tk()
bailey = AlarmSet(master = root)
root.mainloop()
