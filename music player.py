import re, requests, subprocess, urllib.parse, urllib.request
from bs4 import BeautifulSoup
import vlc
import pafy
import time
from tkinter import *
import tkinter.ttk as ttk
import mysql.connector
from mysql.connector import Error

global songstatus
songstatus=0

#initialize tkinter
root = Tk()
root.title('Music Player')
root.iconbitmap('D:\Syll\Python\mp icons\home.png')
root.geometry("600x600")

# Create Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# creating sql connection
def create_server_connection(host_name, user_name, user_password):
    #connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        #print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def openNewWindow1(): 
	
	# Toplevel object which will 
	# be treated as a new window 
	newWindow1 = Toplevel(root) 
	
	# sets the title of the 
	# Toplevel widget 
	newWindow1.title("Select Playlist") 

	# sets the geometry of toplevel 
	newWindow1.geometry("400x400") 
	 
	#pl_box=Listbox(newWindow,bg="grey14",fg="white",width=60)
	#pl_box.pack(pady=20)
	v = StringVar(root, "1")

	connection = create_server_connection("localhost", "root", "mansi")
	cursor = connection.cursor()
	def sp():
		selection = v.get()
		s1 = "use Music_Player;"
		s2="select * from "+selection+";"
		#connection = create_server_connection("localhost", "root", "mansi")
		song_box.delete(0,END)
		cursor = connection.cursor()
		cursor.execute(s1)
		cursor.execute(s2)
		for (s2) in cursor:
			song_box.insert(END,(s2[0]))
		newWindow1.destroy()

	def delete():
		selection = v.get()
		s = "drop table "+ selection+";"
		cursor.execute(s)
		#databases = ("show tables")
		#cursor.execute(databases)
		newWindow1.destroy()


	s1 = ("Use Music_Player;")
	s2 = ("show tables;")
	cursor.execute(s1)
	cursor.execute(s2)
	for (tables) in cursor:
	     #p1_box.insert(databases[0])
	    Radiobutton(newWindow1, text = (tables[0]), variable = v,  
	        value = (tables[0])).pack(fill = X, ipady = 5) 

	btn = Button(newWindow1, text ="open", command = sp) 
	btn.pack(pady = 10)
	btn = Button(newWindow1, text ="delete", command = delete) 
	btn.pack(pady = 10)

	cursor.close()
	connection.close()

btn = Button(root, 
			text ="Show playlists", 
			command = openNewWindow1) 
btn.pack(pady = 10)


def openNewWindow2(): 
	
	# Toplevel object which will 
	# be treated as a new window 
	newWindow2 = Toplevel(root) 

	
	# sets the title of the 
	# Toplevel widget 
	newWindow2.title("Save Playlist") 

	# sets the geometry of toplevel 
	newWindow2.geometry("200x200") 
	


	# A Label widget to show in toplevel 
	Label(newWindow2, 
		text ="Enter playlist name").pack() 
	pname=Entry(newWindow2)
	pname.pack()

	connection = create_server_connection("localhost", "root", "mansi")
	cursor = connection.cursor()
	q = "CREATE DATABASE IF NOT EXISTS Music_Player;"
	cursor.execute(q)

	def save():
		all_items = song_box.get(0,END)
		
		q1="Use Music_Player"
		q2="CREATE TABLE "+pname.get()+"(song varchar(100));"
		cursor.execute(q1)
		cursor.execute(q2)
		#cursor.execute(q3)
		for i in all_items:
			q3="insert into "+ pname.get()+" values('"+ i +"');"
			cursor.execute(q3)
			connection.commit()
		newWindow2.destroy()

	save_button=Button(newWindow2,text="Save",command=save)
	save_button.pack()

	cursor.close()
	connection.close()

btn = Button(root, 
			text ="Save Playlist", 
			command = openNewWindow2) 
btn.pack(pady = 10)




def main(music_name,query):
	query_string = urllib.parse.urlencode({"search_query": music_name})
	formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
	search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
	clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
	clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
	print(clip2)
	inspect = BeautifulSoup(clip.content, "html.parser")
	yt_title = inspect.find_all("meta", property="og:title")

	for concatMusic1 in yt_title:
		pass
	song=concatMusic1['content']
	if query =="add":
		return song
	elif query == "play":
		return clip2


def add():
	music_name = song_name.get()
	song=main(music_name,"add")
	song_box.insert(END,song)	



def search(event):
	global songstatus
	if songstatus==1:
		search.player.stop()
	else:
		pass

	music_name = song_box.get(song_box.curselection())
	url=main(music_name,"play")
	video=pafy.new(url)
	best=video.getbestaudio()
	playurl=best.url
	instance=vlc.Instance()
	search.player=instance.media_player_new()
	media=instance.media_new(playurl)
	media.get_mrl
	search.player.set_media(media)
	search.player.play()
	songstatus=1
	

#search box
Label(master_frame,text="Song Name :").grid(row=0)
song_name=Entry(master_frame)
song_name.grid(row=0,column=1)
add_song_button=Button(master_frame,text="Add Song",command=add)
add_song_button.grid(row=0,column=2)

def playsong():
    search.player.play()
    songstatus=1

def pausesong():
    search.player.pause()
    songstatus=0
def stopsong():
    search.player.stop()
    songstatus=0

def nextsong():
	search.player.stop()
	# Get the current song tuple number
	next_one = song_box.curselection() 
	# Add one to the current song number
	next_one = next_one[0]+1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None) 
	search(ACTIVE)  
def prevsong():
	search.player.stop()
	# Get the current song tuple number
	prev_one = song_box.curselection() 
	# Add one to the current song number
	prev_one = prev_one[0]-1
	#Grab song title from playlist
	song = song_box.get(prev_one)
	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(prev_one)

	# Set Active Bar to Next Song
	song_box.selection_set(prev_one, last=None) 
	search(ACTIVE)  


#Creating list box
song_box=Listbox(root,bg="grey14",fg="white",width=60)
song_box.pack(pady=20)

song_box.bind('<<ListboxSelect>>',search)


#define player buttons
back_btn_img = PhotoImage(file='D:\Syll\Python\mp icons\previous.png')
forward_btn_img =  PhotoImage(file='D:\Syll\Python\mp icons\pp.png')
play_btn_img =  PhotoImage(file='D:\Syll\Python\mp icons\play.png')
pause_btn_img =  PhotoImage(file='D:\Syll\Python\mp icons\pause.png')
stop_btn_img =  PhotoImage(file='D:\Syll\Python\mp icons\home.png')


# Create Player Control Frame
controls_frame = Frame(root)
controls_frame.pack()

#create player control buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0,command=prevsong)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0,command=nextsong)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=playsong)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=pausesong)
stop_button =  Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stopsong)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)    
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

root.mainloop()