import os
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class predictor():
	def __init__(self):
		self.path = ''
		self.list_index = [n for n in range(22)]
		self.categories = ['Affenpinscher', 'Afghan hound', 'Airedale terrier', 'Akbash', 'Akita', 'Alaskan klee kai', 'Alaskan malamute', 'Australian Sheperd', 'Belgian Malinois', 'Bull Terrier', 'Chow Chow', 'Cocker Spaniel', 'Dachshund', 'Dalmatian', 'Doberman Pinscher', 'French Bulldog', 'German Shepherd Dog', 'Golden Retriever', 'Great Dane', 'Labrador Retriever', 'Pomeranian', 'Pug']
		self.P = []

	def predict(self, path):
		self.path = path
		model = load_model('vgg16.h5')
		img = image.load_img(self.path, target_size = (100, 100))
		img = np.expand_dims(img, axis = 0)
		pred = model.predict(img)

		self.P = pred
		for i in range(22):
			for j in range(22):
				if self.P[0][self.list_index[i]] > self.P[0][self.list_index[j]]:
					temp = self.list_index[i]
					self.list_index[i] = self.list_index[j]
					self.list_index[j] = temp

x = predictor()

class aux():
	def __init__(self):
		self.path = ''
		self.last = ''

	def setpath(self, path):
		self.path = path

	def setlast(self, last):
		self.last = last

y = aux()

class main(Screen):
	def take_photo(self, *args):
		directory = os.getcwd()
		path = os.path.join(directory, 'fotos')
		if not os.path.exists(path):
			print('xd')
			os.makedirs(path)
		files = os.listdir(path)
		path_ = os.path.join(path, 'foto' + str(len(files)) + '.png')
		print(path_)
		self.cam.export_to_png(path_)
		y.setlast('main')	
		y.setpath(path_)
		screen = visualize(name = 'visualization')
		sm.add_widget(screen)
		sm.current = 'visualization'

class explorer(Screen):
	def selected(self, filename):
		y.setlast('explorer')
		y.setpath(filename[0])
		screen = visualize(name = 'visualization')
		sm.add_widget(screen)

class visualize(Screen):
	def __init__(self, **k):
		super().__init__(**k)

		self.layout = GridLayout()
		self.layout.cols = 1

		self.viz_img = Image(source = y.path)
		self.layout.add_widget(self.viz_img)

		self.botones = GridLayout()
		self.botones.cols = 2

		self.go_back = Button(text = 'back')
		self.go_back.bind(on_press = self.goback)
		self.botones.add_widget(self.go_back)

		self.go_pred = Button(text = 'predict')
		self.go_pred.bind(on_press = self.gopred)
		self.botones.add_widget(self.go_pred)

		self.layout.add_widget(self.botones)

		self.add_widget(self.layout)

	def goback(self, *a):
		sm.remove_widget(sm.screens[-1])
		sm.current = y.last

	def gopred(self, *a):
		x.predict(y.path)
		sm.remove_widget(sm.screens[-1])
		screen = prediction(name = 'prediction')
		sm.add_widget(screen)
		sm.current = 'prediction'
		

class prediction(Screen):
	def __init__(self, **k):
		super().__init__(**k)

		self.layout = GridLayout()
		self.layout.cols = 1

		self.imagen = Image(source = y.path)
		self.layout.add_widget(self.imagen)

		self.labels = GridLayout()
		self.labels.cols = 2
		for i in range(5):
			self.labels.add_widget(Button(text = x.categories[x.list_index[i]]))
			self.labels.add_widget(Button(text = str(x.P[0][x.list_index[i]]*100)[:5]))

		self.layout.add_widget(self.labels)

		self.back = Button(text = 'main')
		self.back.bind(on_press = self.go_main)

		self.layout.add_widget(self.back)

		self.add_widget(self.layout)

	def go_main(self, *k):
		sm.remove_widget(sm.screens[-1])
		sm.current = 'main'



kv = Builder.load_file('dog.kv')
sm = ScreenManager()
sm.add_widget(main(name = 'main'))
sm.add_widget(explorer(name = 'explorer'))

class dog(App):
	def build(self):
		return sm

if __name__ == '__main__':
	app = dog()
	app.run()