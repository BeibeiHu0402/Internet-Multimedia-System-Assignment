# Internet-Multimedia-System-Assignment
IMS Assignment: Research and Development on HTTP Video Streaming

All installations and operations are on Linux or Mac OS system.

## Install FFmpeg
To download FFmpeg package, it is recommended to retrieve the source code through Git by using the command:

```
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
```
If sudo access is granted, it can be also installed by typing command in the terminal:
```
sudo apt-get install ffmpeg
```
A pre-compiled Linux FFmpeg binary is available [here](http://www.ee.ucl.ac.uk/~iandreop/ffmpeg\_static\_with\_VMAF.zip). 

For Mac OS users, install FFmpeg in terminal; for Linux users, download the pre-compiled version and install FFmpeg in the termial to make sure all libraries are installed. 

## Install MP4Box
To download MP4Box with Make, type following commands in terminal to first install git, gcc, make and libpthread-dev on your system.
```
git clone https://github.com/gpac/gpac.git
cd gpac
./configure --static-mp4box --use-zlib=no
make -j4
```

By now, MP4Box is executable at: bin/gcc/MP4Box. Then, MP4Box can be installed now by typing:
```
sudo make install mp4box
```
The MP4Box is now installed at the default folder /usr/local/bin/MP4Box.

## Shaka Player
To install Shaka Player, there is a useful official tutorial web page posted available at [its offcial website](https://shaka-player-demo.appspot.com/docs/api/tutorial-welcome.html). Type following commands in terminal:
```
git clone https://github.com/google/shaka-player.git
sudo install npm
cd shaka-player
python build/all.py
```
There are two files required to run the library available [here](https://shaka-player-demo.appspot.com/docs/api/tutorial-basic-usage.html). Create a HTML file and a JavaScript file using codes provided.

## Trans-coding and Playing

To trans-code, download a.ui, ui_setter.py, ffmpeg_util.py and main_ui.py, and put them under the same directory. Execute main_ui.py with Python. Video trans-coding and DASH segment generation can be done with this toolbox.
To play DASH videos, users must make sure they have a server on their system, and Apache is used here. For Linux, Apache2 is recommended; for Mac OS, Apachectl is recommended. 
To install Apache2 and execute on Linux, type following commands in terminal:
```
sudo apt-get install apache2
sudo service apache2 start
```
To install Apachectl and execute on Mac OS, type following commands in terminal:
```
sudo apt-get install apachectl
sudo service apachectl start
```
Drag the Shaka Player install folder, HTML file and .js file into the folder where Apache is installed. For Linux, it is under /var/www/html/; for Mac OS, it is under /Library/WebServer/Documents. To execute specific dash contents given multiple dash segments have been generated from different original videos, drag the folder with all DASH contents to Aapche folder, and the name of specific .mpd file must be written correctly at the beginning of 'myapp.js'. To play the specific video content, simply type 'localhost' in your browser.

That's it!
