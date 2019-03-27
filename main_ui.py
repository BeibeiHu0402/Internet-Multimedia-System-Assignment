from PyQt5.QtWidgets import QApplication, QWidget,QFileDialog,QLineEdit,QLabel, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_setter import Ui_mainWindow
from ffmpeg_util import *
import os

class MainUI():

	def on_click_open_souce_file(self):
		
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		video_path, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","MP4 Files (*.mp4);;mkv files (*.mkv)", options=options)
		if video_path:
			self.main.label_path.setText(video_path)

			file_name, file_size, resolution,frame_rate, duration, bit_rate,width,height = get_video_info(video_path)

			self.main.label_file_name.setText(file_name)
			self.main.label_file_size.setText(file_size)
			self.main.label_file_duration.setText(duration)
			self.main.label_file_resolution.setText(resolution)
			self.main.label_file_frame_rate.setText(frame_rate)
			self.main.label_file_bit_rate.setText(bit_rate)
			self.path = video_path
			self.width = int(width)
			self.height = int(height)
			self.main.lineEdit_width.setText(width)
			self.main.lineEdit_height.setText(height)
			self.main.lineEdit_cbr.setText(str(int(int(bit_rate)/1000)))
			self.main.lineEdit_abr.setText(str(int(int(bit_rate)/1000)))

	def on_check_keep_aspect_ratio(self):
		print(self.path)
		if self.main.checkbox_aspect_ratio.isChecked():
			w = 0
			h = 0
			if self.main.lineEdit_width.text() != "":
				w = int(self.main.lineEdit_width.text())
			if self.main.lineEdit_height.text() != "":
				h = int(self.main.lineEdit_height.text())
			if self.main.lineEdit_width.text() =="" and self.main.lineEdit_height.text() == "":
				w = self.width
				h = self.height
			print(w,h)
			width, height = get_width_by_aspect_ratio(self.path,w,h)
			self.main.lineEdit_width.setText(str(width))
			self.main.lineEdit_height.setText(str(height))
		else:
			print("not checked")

	def on_width_edit_change(self):
		if self.main.lineEdit_width.text() != "":
			self.on_check_keep_aspect_ratio()

	def on_click_start_transcoding(self):

		if not self.main.radiobutton_vbr.isChecked() and not self.main.radiobutton_cbr.isChecked() and not self.main.radiobutton_abr.isChecked():
			QMessageBox.about(self.main_window, "message", "At least choose one!")
			return

		#segment duration
		if self.main.checkBox_custom_segment_duration.isChecked():
			print("custom segment duration")
			if self.main.lineEdit_segment_duration.text() == "":
				self.segment_duration= 1000#ms
			elif self.main.lineEdit_segment_duration.text()!= "":
				self.segment_duration = int(self.main.lineEdit_segment_duration.text())
			print(self.segment_duration)
		else:	
			self.segment_duration = 1000	
			print("default sgement duration")

		#saved name
		if self.main.lineEdit_saved_name.text() == "":
			self.saved_name = 'output.mp4'
			self.main.lineEdit_saved_name.setText(self.saved_name)
		elif self.main.lineEdit_saved_name.text() != "":
			self.saved_name = self.main.lineEdit_saved_name.text()
		print(self.saved_name)

		#bit rate type
		self.custom_bit_rate = int(self.main.label_file_bit_rate.text())
		print('default',self.custom_bit_rate)
		if self.main.radiobutton_cbr.isChecked():
			print('choose cbr')
			if self.main.lineEdit_cbr.text() == "":
				self.custom_bit_rate = int(self.main.label_file_bit_rate.text())
			elif self.main.lineEdit_cbr.text() != "":
				self.custom_bit_rate = int(self.main.lineEdit_cbr.text())
			print("b=",self.custom_bit_rate)	
			self.main.lineEdit_cbr.setText(str(self.custom_bit_rate))
			transcode_using_cbr(self.main.lineEdit_width.text(),
								self.main.lineEdit_height.text(),
								str(self.custom_bit_rate),
								self.segment_duration,
								self.path,
								self.saved_name)
			QMessageBox.about(self.main_window, "message", "Conversion complete!")

		elif self.main.radiobutton_vbr.isChecked():
			print('choose vbr')
			
			if self.main.lineEdit_vbr_max.text() == "":
				self.custom_bit_rate_max = 5000
			elif self.main.lineEdit_vbr_max.text() != "":
				self.custom_bit_rate_max = int(self.main.lineEdit_vbr_max.text())
			
			print('b max=',self.custom_bit_rate_max)
			
			self.main.lineEdit_vbr_max.setText(str(self.custom_bit_rate_max))

			transcode_using_vbr(self.main.lineEdit_width.text(),
								self.main.lineEdit_height.text(),
								str(self.custom_bit_rate_max),
								self.segment_duration,
								self.path,
								self.saved_name)
			QMessageBox.about(self.main_window, "message", "Conversion complete!")

		elif self.main.radiobutton_abr.isChecked():
			print('choose abr')
			if self.main.lineEdit_abr.text() == "":
				self.custom_bit_rate = int(self.main.label_file_bit_rate.text())
			elif self.main.lineEdit_abr.text() != "":
				self.custom_bit_rate= int(self.main.lineEdit_abr.text())	
			print("b=",self.custom_bit_rate)
			self.main.lineEdit_abr.setText(str(self.custom_bit_rate))
			transcode_using_abr(self.main.lineEdit_width.text(),
								self.main.lineEdit_height.text(),
								str(self.custom_bit_rate),
								self.segment_duration,
								self.path,
								self.saved_name)
			QMessageBox.about(self.main_window, "message", "Conversion complete!")

	def get_file_names(self, paths):
		names_label = ""
		for each in paths:
			names_label = names_label + each.split('/')[-1] + "; "
		return names_label

	def on_click_browse_file(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.paths, _ = QFileDialog.getOpenFileNames(None,"QFileDialog.getOpenFileName()", "","MP4 Files (*.mp4)", options=options)
		self.main.label_path_dash.setText(self.get_file_names(self.paths))

	def on_click_generating_DASH(self):
		#get title
		if self.main.lineEdit_dash_title == "":
			title = 'output'
		else:
			title = self.main.lineEdit_dash_title.text()
		self.segment_duration = 1000
		generate_dash(self.paths,str(self.segment_duration),title)

	def reg_comp_event(self):
			#reg click event for pushbutton_opensource
		self.main.pushbutton_opensource.clicked.connect(self.on_click_open_souce_file)
		self.main.checkbox_aspect_ratio.stateChanged.connect(self.on_check_keep_aspect_ratio)
		self.main.lineEdit_width.textChanged.connect(self.on_width_edit_change)
		self.main.pushButton_start_transcoding.clicked.connect(self.on_click_start_transcoding)
		self.main.pushbutton_browse_file.clicked.connect(self.on_click_browse_file)
		self.main.pushButton_start_generating_DASH_MPD.clicked.connect(self.on_click_generating_DASH)

	def start(self):
		self.app = QApplication([])
		self.main_window = QtWidgets.QMainWindow()

		self.main = Ui_mainWindow()
		self.main.setupUi(self.main_window)

		self.path = ""
		self.reg_comp_event()
		self.main_window.show()
		self.app.exec_()

ui = MainUI()
ui.start()









