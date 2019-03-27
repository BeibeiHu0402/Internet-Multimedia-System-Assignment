import os
from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog,QLineEdit,QLabel, QMessageBox

def get_video_info(video_path):
	file_name = os.path.basename(video_path)
	file_size = str(os.path.getsize(video_path))
	command = "ffprobe -v error -select_streams v:0 -show_entries stream=Duration,width,height,avg_frame_rate,bit_rate -sexagesimal -of default=nw=1 " + "\'"+video_path+"\' > temp.txt"
	os.system(command)
	content = read_txt_and_remove('temp.txt')

	arr = content.split("\n")
	width = arr[0].split("=")[1]
	height = arr[1].split("=")[1]
	frame_rate = arr[2].split("=")[1]
	duration = arr[3].split("=")[1]
	bit_rate= arr[4].split("=")[1]
	resolution = str(width)+'x'+str(height)
	return file_name, file_size, resolution,frame_rate, duration, bit_rate,width,height #text

def read_txt_and_remove(file_name):
	#read 
	content =  open(file_name, 'r').read()
	#delete
	os.remove(file_name)
	return content

#get_height_by_aspect_ratio
def get_width_by_aspect_ratio(video_path,width, height):
	width = abs(width)
	height = abs(height)
	print("come in")
	ratio = get_aspect_ratio(video_path)
	print(ratio)
	if width==0 and height ==0:
		return int(width),int(height)
	elif width != 0:
		return width, int(width / ratio)
	elif lineEdit_width == 0 and lineEdit_height != 0:
		return int(width * ratio), height

#get_width_by_aspect_ratio
def get_height_by_aspect_ratio(video_path,width, height):
	width = abs(width)
	height = abs(height)
	print("come in")
	ratio = get_aspect_ratio(video_path)
	print(ratio)
	return int(height * ratio), height

def get_aspect_ratio(video_path):
	if video_path == "":
		return 16/9
	command = "ffprobe -v error -select_streams v:0 -show_entries stream=Duration,width,height,avg_frame_rate,bit_rate -sexagesimal -of default=nw=1 " + "\'"+video_path+"\' > temp.txt"
	os.system(command)
	content = read_txt_and_remove('temp.txt')
	arr = content.split("\n")
	original_width =int(arr[0].split("=")[1])
	original_height = int(arr[1].split("=")[1])
	ratio = original_width/original_height
	return ratio

def transcode_using_cbr(width,height,custom_bit_rate,segment_duration,path,output_name):
	gop_len = segment_duration/1000.0
	output_path = path.replace(path.split('/')[-1], output_name)
	command = 'ffmpeg -i \''+ path + '\' -vf scale=' + width +':' +height + ' -force_key_frames \"expr:gte(t,n_forced*'+str(gop_len)+')\"' + ' -c:v libx264 -b:v ' + custom_bit_rate + 'k -minrate '+ custom_bit_rate + 'k -maxrate '+custom_bit_rate + 'k -bufsize '+custom_bit_rate+'k \'' + output_path + '\''

	# /Users/mike/Desktop/input.mp4
	# output name = output.m4
	#  /Users/mike/Desktop/output.m4
	print("CBR transcoding")
	print(command)
	os.system(command)

def transcode_using_vbr(width,height,custom_bit_rate_max,segment_duration,path,output_name):
	gop_len = segment_duration/1000.0
	output_path = path.replace(path.split('/')[-1], output_name)
	command = 'ffmpeg -i \''+ path + '\' -vf scale=' + width +':' +height + ' -force_key_frames \"expr:gte(t,n_forced*'+str(gop_len)+')\"' + ' -c:v libx264 -maxrate ' + custom_bit_rate_max + 'k -bufsize '+custom_bit_rate_max+ 'k \'' + output_path + '\''

	# /Users/mike/Desktop/input.mp4
	# output name = output.m4
	#  /Users/mike/Desktop/output.m4
	print("VBR transcoding")
	print(command)
	os.system(command)

def transcode_using_abr(width,height,custom_bit_rate,segment_duration,path,output_name):
	gop_len = segment_duration/1000.0
	output_path = path.replace(path.split('/')[-1], output_name)
	command_1 = 'ffmpeg -i \''+ path + '\' -vf scale=' + width +':' +height + ' -force_key_frames \"expr:gte(t,n_forced*'+str(gop_len)+')\"' + ' -c:v libx264 -b:v ' + custom_bit_rate + 'k -pass 1 -an -f mp4 /dev/null && \\'
	command_2 = 'ffmpeg -i \''+ path + '\' -vf scale=' + width +':' +height + ' -force_key_frames \"expr:gte(t,n_forced*'+str(gop_len)+')\"' + ' -c:v libx264 -b:v ' + custom_bit_rate + 'k -pass 2 \'' + output_path + '\''
	# /Users/mike/Desktop/input.mp4
	# output name = output.m4
	#  /Users/mike/Desktop/output.m4
	print("ABR transcoding")
	print(command_1)
	print(command_2)
	os.system(command_1 + command_2)

def generate_dash(paths,segment_duration,title):
	prefix = paths[0].replace(os.path.basename(paths[0]),"")
	print(prefix)
	path_str = ""
	for each in paths:
		path_str += '\''+ each + "\' "
	path_str = path_str[:-1]
	command = 'MP4Box -dash '+segment_duration+' -frag '+segment_duration+' -frag-rap -rap -bs-switching inband -profile dashavc264:live -mpd-title \"'+title+'\" -segment-ext null -out \''+prefix+title+'.mpd\' '+path_str
#MP4Box -dash 5000 -frag 5000 -frag-rap -rap -bs-switching inband -profile dashavc264:live -mpd-title "london" -segment-ext null -out london.mpd london_1080p.mp4 london_720p.mp4 london_360p.mp4 london_144p.mp4	
#MP4Box -dash 1000 -frag 1000 -frag-rap -rap -bs-switching inband -profile dashavc264:live -mpd-title "haha" -segment-ext null -out hahampd '/Users/hamulante/Desktop/360_vbr.mp4'
#MP4Box -dash 1000 -frag 1000 -frag-rap -rap -bs-switching inband -profile dashavc264:live -mpd-title "output" -segment-ext null -out '/Users/hamulante/Desktop/test/output.mpd ''/Users/hamulante/Desktop/test/360_abr_800k.mp4' '/Users/hamulante/Desktop/test/360_vbr.mp4'
	print(command)
	os.system(command)
