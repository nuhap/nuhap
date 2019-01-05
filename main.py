# -*- coding: utf-8 -*-
import io
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image, AsyncImage
from kivy.lang.builder import Builder
import threading
import datetime
from kivy.clock import Clock, mainthread
from functools import partial
import mysql.connector

from kivy.core.window import Window
Window.softinput_mode = 'below_target'

kvcode = """
#:import ScrollEffect kivy.effects.scroll.ScrollEffect

<TelaManager>:
	Home:
		name: 'home'
		id: first
	Screen1:
		name: 'screen1'
		id: screen1
	Screen2:
		name: 'screen2'
		id: screen2
	TelaBar:
		id: telabar
		name: 'telabar'
	TelaEvento:
		id: telaevento
		name: 'telaevento'
	CriaEvento:
		name: 'criaevento'
		id: criaevento
	EventosIndie:
		name: 'eventosindie'
		id: eventosindie

<Home>:
	BoxLayout:
		orientation: 'vertical'
		padding: '20dp', '150dp', '20dp', '150dp'
		spacing: '40dp'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
				pos: self.pos
		Button:
			text: 'EVENTOS'
			background_normal: 'Image/BUTTONS/homebutton.png'
			background_down: 'Image/BUTTONS/homebuttondown.png'
			on_release: root.manager.current = 'screen2'
			on_release: root.manager.get_screen('screen2').clear()
			size_hint_y: None
			height: '50dp'
		Button:
			text: 'BARES E RESTAURANTES'
			background_normal: 'Image/BUTTONS/homebutton.png'
			background_down: 'Image/BUTTONS/homebuttondown.png'
			on_release: root.manager.current = 'screen1'
			on_release: root.manager.get_screen('screen1').clear()
			size_hint_y: None
			height: '50dp'
		Label:
			text: 'Contato: nuhapnew@gmail.com'
			color: 1, 1, 1, 1

<Screen1>:
	BoxLayout:
		orientation: 'vertical'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
				pos: self.pos
		ActionBar:
			background_image: ''
			background_color: 1, 1, 1, .2
			ActionView:
				ActionPrevious:
					with_previous: False
					title:  'Bares e Restaurantes'
					color: 0.941, 0.729, 0.078, 1
					app_icon: ''
				ActionButton:
					text: 'Eventos'
					background_down: 'Image/BUTTONS/actionbuttondown.png'
					on_release: root.manager.current = 'screen2'
					on_release: root.manager.get_screen('screen2').clear()
				ActionButton:
					text: 'Home'
					background_down: 'Image/BUTTONS/actionbuttondown.png'
					on_release: root.manager.current = 'home'
		BoxLayout:
			orientation: 'vertical'
			padding: '20dp', '15dp'
			size_hint_y: None
			height: '80dp'
			Label:
				text: 'O que tem pra hoje?'
				size_hint_y: None
				height: '50dp'
		Spinner:
			id: myspinner
			text: 'Selecione uma região'
			size_hint_y: None
			height: '50dp'
			color: 0, 0, 0, 1
			background_normal: ''
			background_down: ''
			background_color: 1, 1, 1, 1
			values: ['Criciúma', 'Tubarão', 'Laguna', 'Garopaba', 'Floripa']
			on_text: root.load(self.text)
		Label:
			size_hint_y: None
			height: '15dp'
		ScrollView:
			id: scroll1
			effect_cls: ScrollEffect
			BoxLayout:
				id: box1
				orientation: 'vertical'
				padding: 0, '40dp', 0, '60dp'
				spacing: '30dp'
				size_hint_y: None
				height: self.minimum_height

<Screen2>:
	BoxLayout:
		orientation: 'vertical'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
		ActionBar:
			background_image: ''
			background_color: 1, 1, 1, .2
			ActionView:
				ActionPrevious:
					with_previous: False
					title:  'Eventos'
					color: 0.941, 0.729, 0.078, 1
					app_icon: ''
				ActionButton:
					text: 'Bares e Restaurantes'
					background_down: 'Image/BUTTONS/actionbuttondown.png'
					on_release: root.manager.current = 'screen1'
					on_release: root.manager.get_screen('screen1').clear()
				ActionButton:
					text: 'Home'
					background_down: 'Image/BUTTONS/actionbuttondown.png'
					on_release: root.manager.current = 'home'
		BoxLayout:
			orientation: 'vertical'
			padding: '20dp', 0, '20dp', '15dp'
			size_hint_y: None
			height: '80dp'
			Button:
				text: 'EVENTOS INDEPENDENTES'
				color: 1, 1, 1, 1
				background_normal: 'Image/BUTTONS/homebutton.png'
				background_down: 'Image/BUTTONS/homebuttondown.png'
				on_release: root.manager.current = 'eventosindie'
				on_release: root.manager.get_screen('screen2').clear()
				on_release: root.manager.get_screen('eventosindie').clear()
				size_hint_y: None
				height: '50dp'
		Spinner:
			id: myspinner
			text: 'Selecione uma região'
			size_hint_y: None
			height: '50dp'
			color: 0, 0, 0, 1
			background_normal: ''
			background_down: ''
			background_color: 1, 1, 1, 1
			values: ['Criciúma', 'Tubarão', 'Laguna', 'Garopaba', 'Floripa']
			on_text: root.load(self.text)
		Label:
			size_hint_y: None
			height: '15dp'
		ScrollView:
			id: scroll1
			effect_cls: ScrollEffect
			BoxLayout:
				orientation: 'vertical'
				id: box1
				padding: 0, '20dp'
				spacing: '30dp'
				size_hint_y: None
				height: self.minimum_height

<TelaBar>:
	BoxLayout:
		orientation: 'vertical'
		spacing: '20dp'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
		ActionBar:
			background_image: ''
			background_color: 1, 1, 1, .2
			ActionView:
				ActionPrevious:
					id: title
					on_release: root.manager.current = 'screen1'
					color: 0.988, 0.553, 0.2, 1
					app_icon: ''
		BoxLayout:
			orientation: 'vertical'
			Label:
				id: lbcidade
				size_hint_y: .1
			Label:
				id: lbendereco
				size_hint_y: .1
			Label:
				id: lbcontato
				size_hint_y: .1
			Label:
				size_hint_y: .1
			ScrollView:
				BoxLayout:
					id: box1
					orientation: 'vertical'
					padding: 0, '20dp', 0, '40dp'
					spacing: '20dp'
					size_hint_y: None
					height: self.minimum_height

<TelaEvento>:
	BoxLayout:
		orientation: 'vertical'
		spacing: '20dp'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
		ActionBar:
			background_image: ''
			background_color: 1, 1, 1, .2
			ActionView:
				ActionPrevious:
					id: title
					on_release: root.manager.current = 'screen2'
					color: 0.988, 0.553, 0.2, 1
					app_icon: ''
		BoxLayout:
			orientation: 'vertical'
			id: box1
			Label:
				id: lbcidade
				size_hint_y: .1
			Label:
				id: lbendereco
				size_hint_y: .1
			BoxLayout:
				orientation: 'vertical'
				padding: '10dp', '60dp'
				ScrollView:
					BoxLayout:
						orientation: 'vertical'
						size_hint_y: None
						height: root.ids.lbdescricao.height
						Label:
							id: lbdescricao
							size: self.texture_size
							text_size: self.width, None
							valign: 'top'
							halign:'center'


<CriaEvento>:
	BoxLayout:
		orientation: 'vertical'
		spacing: '20dp'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
				pos: self.pos
		ActionBar:
			background_image: ''
			background_color: 1, 1, 1, .2
			ActionView:
				ActionPrevious:
					on_release: root.manager.current = 'eventosindie'
					title:  'Criar Evento'
					color: 0.941, 0.729, 0.078, 1
					app_icon: ''
				ActionButton:
					text: 'Home'
					background_down: 'Image/BUTTONS/actionbuttondown.png'
					on_release: root.manager.current = 'home'
		Spinner:
			id: spinnerregiao
			text: 'Selecione uma região'
			size_hint_y: None
			height: '40dp'
			color: 0, 0, 0, 1
			background_normal: ''
			background_down: ''
			background_color: 1, 1, 1, 1
			values: ['Criciúma', 'Tubarão', 'Laguna', 'Garopaba', 'Floripa']
		TextInput:
			size_hint_y: .1
			hint_text: 'Título (inclua a cidade)'
			id: txtnome
			multiline: False
			input_filter: lambda text, from_undo: text[:70 - len(self.text)]
		BoxLayout:
			size_hint_y: .1
			spacing: '10dp'
			Spinner:
				size_hint_x: .3
				id: spinnerdia
				text: 'Dia'
				color: 0, 0, 0, 1
				background_normal: ''
				background_down: ''
				background_color: 1, 1, 1, 1
				values: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
			Spinner:
				id: spinnermes
				text: 'Mês'
				color: 0, 0, 0, 1
				background_normal: ''
				background_down: ''
				background_color: 1, 1, 1, 1
				values: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
			TextInput:
				id: txtano
				size_hint_x: .5
				hint_text: 'Ano'
				text_size: self.size
				padding_y: '15dp'
				halign: 'center'
				valign: 'top'
		TextInput:
			id: txtdescricao
			size_hint_y: .4
			hint_text: 'Descrição (inclua o contato)'
			input_filter: lambda text, from_undo: text[:250 - len(self.text)]
		BoxLayout:
			orientation: 'vertical'
			id: box1
			size_hint_y: None
			height: '80dp'
			padding: '20dp', '20dp'
			Button:
				id: btenvia
				text: 'CRIAR'
				background_normal: 'Image/BUTTONS/homebutton.png'
				background_down: 'Image/BUTTONS/homebuttondown.png'
				on_release: root.cria_evento(root.ids.txtnome.text, root.ids.spinnerregiao.text, root.ids.spinnerdia.text, root.ids.spinnermes.text, root.ids.txtano.text, root.ids.txtdescricao.text)
				size_hint_y: None
				height: '50dp'

<EventosIndie>:
	BoxLayout:
		orientation: 'vertical'
		canvas:
			Color:
				rgba: 0.098, 0.098, 0.098, 1
			Rectangle:
				size: self.size
				pos: self.pos
		BoxLayout:
			orientation: 'vertical'
			spacing: '30dp'
			ActionBar:
				background_image: ''
				background_color: 1, 1, 1, .2
				ActionView:
					ActionPrevious:
						background_down: 'Image/BUTTONS/actionbuttondown.png'
						on_release: root.manager.current = 'screen2'
						title:  'Eventos Independentes'
						color: 0.941, 0.729, 0.078, 1
						app_icon: ''
					ActionButton:
						text: 'Home'
						background_down: 'Image/BUTTONS/actionbuttondown.png'
						on_release: root.manager.current = 'home'
			Spinner:
				id: spinnerregiao
				text: 'Selecione uma região'
				size_hint_y: None
				height: '50dp'
				color: 0, 0, 0, 1
				background_normal: ''
				background_down: ''
				background_color: 1, 1, 1, 1
				values: ['Criciúma', 'Tubarão', 'Laguna', 'Garopaba', 'Floripa']
				on_text: root.manager.ids.eventosindie.load(self.text)
			ScrollView:
				id: scroll1
				effect_cls: ScrollEffect
				BoxLayout:
					id: box1
					orientation: 'vertical'
					padding: '10dp', '20dp', '10dp', '20dp'
					spacing: '20dp'
					size_hint_y: None
					height: self.minimum_height
		BoxLayout:
			orientation: 'vertical'
			size_hint_y: None
			height: '80dp'
			padding: '20dp', '20dp'
			Button:
				text: 'CRIAR UM EVENTO'
				background_normal: 'Image/BUTTONS/homebutton.png'
				background_down: 'Image/BUTTONS/homebuttondown.png'
				on_release: root.manager.current = 'criaevento'
				on_release: root.manager.get_screen('eventosindie').clear()
				size_hint_y: None
				height: '50dp'

<SpinnerOption>:
	background_normal: ''
	background_color: 1, 1, 1, 1
	background_down: ''
	color: 0, 0, 0, 1

<BoxFeedBar>:
	size_hint_y: None
	padding: '3dp', '3dp'
	height: '300dp'
	keep_ratio: False
	allow_stretch: True

<BoxFeedBar2>:
	size_hint_y: None
	padding: '3dp', '3dp'
	height: '300dp'
	keep_ratio: False
	allow_stretch: True

<BoxFeedEvento>:
	size_hint_y: None
	padding: '3dp', '3dp'
	height: '300dp'
	keep_ratio: False
	allow_stretch: True

<BoxFeedEventoIndie>:
	orientation: 'vertical'
	size_hint_y: None
	height: root.ids.descricao.height + dp(70)
	canvas:
		Color:
			rgba: 1, 1, 1, .2
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius: 5, 5, 5, 5
	Label:
		id: descricao
		color: 1, 1, 1, 1
		size_hint_y: None
		size: self.texture_size
		text_size: self.width, None
		pos: self.parent.x, self.parent.y
		padding_x: '10dp'
		padding_y: '15dp'
		halign: 'center'
		valign: 'bottom'
		Label:
			id: titulo
			color: 0.941, 0.729, 0.078, 1
			bold: True
			pos: self.parent.x, self.parent.y + dp(60)
			size_hint: None, None
			size: self.parent.size
			text_size: self.size
			padding_x: '10dp'
			halign: 'center'
			valign: 'top'
		Label:
			id: data
			color: 0.941, 0.729, 0.078, 1
			pos: self.parent.x, self.parent.y + dp(15)
			size_hint: None, None
			size: self.parent.size
			text_size: self.size
			halign: 'center'
			valign: 'top'
"""

Builder.load_string(kvcode)

try:
	class TelaManager(ScreenManager):
		def __init__(self, **kwargs):
			super(TelaManager, self).__init__(**kwargs)
			Window.bind(on_keyboard=self.android_back_click)

			self.transition = FadeTransition()

		def android_back_click(self, window, key, *args):
			if key == 27:
				if self.current == 'screen1':
					self.current = 'home'
					return True

				elif self.current == 'screen2':
					self.current = 'home'
					return True

				elif self.current == 'eventosindie':
					self.current = 'screen2'

					return True

				elif self.current == 'telabar':
					self.current = 'screen1'
					return True

				elif self.current == 'telaevento':
					self.current = 'screen2'
					return True

				elif self.current == 'criaevento':
					self.current = 'eventosindie'
					return True

	class Home(Screen):
		pass

	class GiftScreen(Screen):
		pass

	class Screen1(Screen):
		load_count = 0

		def __init__(self, **kwargs):
			super(Screen1, self).__init__(**kwargs)

		def load(self, cidade):
			self.ids.box1.clear_widgets()
			if cidade != 'Selecione uma região':
				threading.Thread(target = self.mostra_carregando).start()
				threading.Thread(target = self.mostra_dados, args=(cidade,)).start()

		def load2(self, cidade, *args):
			threading.Thread(target = self.mostra_carregando2).start()
			threading.Thread(target = self.mostra_dados2, args=(cidade,)).start()

		def mostra_dados(self, cidade, *args):
			bares_nomes = []
			telabar = self.manager.ids.telabar
			id_cidade = None

			if cidade == 'Tubarão':
				id_cidade = 1
			elif cidade == 'Criciúma':
				id_cidade = 2
			elif cidade == 'Laguna':
				id_cidade = 3
			elif cidade == 'Garopaba':
				id_cidade = 4
			elif cidade == 'Floripa':
				id_cidade = 5

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')

			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM r_bares WHERE id_cidade=%d LIMIT 0, 4'%(id_cidade))
			bares_nomes = cursor.fetchall()
			bares_desc1 = []

			for i in range(len(bares_nomes)):
				current_date = datetime.date.today()
				cursor.execute("SELECT * FROM r_descricoes WHERE id_bar=%d AND data LIKE '%s'"%(bares_nomes[i]['id'], current_date))
				bares_desc = cursor.fetchall()
				if bares_desc != []:
					bares_desc1.append(bares_desc)

			if bares_desc1 == []:
				self.ids.box1.clear_widgets()
				self.ids.box1.add_widget(Label(text='Nada na região de %s por enquanto'%(cidade)))
			else:
				self.ids.box1.clear_widgets()
				for i in range(len(bares_desc1)):
					self.ids.box1.add_widget(BoxFeedBar(telabar, bares_nomes[i]['id'], bares_desc1[i][0]['link_imagem'], bares_nomes[i]['nome'], bares_nomes[i]['cidade'], bares_nomes[i]['contato'], bares_nomes[i]['endereco']))
				self.ids.box1.add_widget(LoadButton(self.manager.ids.screen1, cidade, text='mais', size_hint_y=None, height='50dp', background_normal='', background_color=[0, 0, 0, .5]))
				self.load_count += 4

		def mostra_dados2(self, cidade, *args):
			bares_nomes = []
			telabar = self.manager.ids.telabar
			id_cidade = None

			if cidade == 'Tubarão':
				id_cidade = 1
			elif cidade == 'Criciúma':
				id_cidade = 2
			elif cidade == 'Laguna':
				id_cidade = 3
			elif cidade == 'Garopaba':
				id_cidade = 4
			elif cidade == 'Floripa':
				id_cidade = 5

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')

			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM r_bares WHERE id_cidade=%d ORDER BY nome LIMIT %d, %d'%(id_cidade, self.load_count, 4))
			bares_nomes = cursor.fetchall()
			bares_desc1 = []

			self.ids.box1.remove_widget(self.ids.box1.children[0])
			for i in range(len(bares_nomes)):
				current_date = datetime.date.today()
				cursor.execute("SELECT * FROM r_descricoes WHERE id_bar=%d AND data LIKE '%s'"%(bares_nomes[i]['id'], current_date))
				bares_desc = cursor.fetchall()
				if bares_desc != []:
					bares_desc1.append(bares_desc)

			if bares_desc1 != []:
				for i in range(len(bares_desc1)):
					self.ids.box1.add_widget(BoxFeedBar(telabar, bares_nomes[i]['id'], bares_desc1[i][0]['link_imagem'], bares_nomes[i]['nome'], bares_nomes[i]['cidade'], bares_nomes[i]['contato'], bares_nomes[i]['endereco']))
				self.ids.box1.add_widget(LoadButton(self.manager.ids.screen1, cidade, text='mais', size_hint_y=None, height='50dp', background_normal='', background_color=[0, 0, 0, .5]))
				self.ids.scroll1.scroll_to(self.ids.box1.children[4])
				self.load_count += 4

		@mainthread
		def mostra_carregando(self):
			self.ids.box1.add_widget(Label(text='Carregando...', color=[1, 1, 1, 1]))

		@mainthread
		def mostra_carregando2(self):
			self.ids.box1.remove_widget(self.ids.box1.children[0])
			self.ids.box1.add_widget(Label(text='Carregando...', size_hint_y=None, height='50dp', color=[1, 1, 1, 1]))

		def clear(self):
			self.ids.myspinner.text = 'Selecione uma região'

	class Screen2(Screen):
		load_count = 0
		def __init__(self, **kwargs):
			super(Screen2, self).__init__(**kwargs)

		def load(self, cidade):
			self.ids.box1.clear_widgets()
			if cidade != 'Selecione uma região':
				threading.Thread(target = self.mostra_carregando).start()
				threading.Thread(target = self.mostra_dados, args=(cidade,)).start()

		def load2(self, cidade, *args):
			threading.Thread(target = self.mostra_carregando2).start()
			threading.Thread(target = self.mostra_dados2, args=(cidade,)).start()

		def mostra_dados(self, cidade, *args):
			telaevento = self.manager.ids.telaevento
			eventos = []
			id_cidade = 1

			if cidade == 'Tubarão':
				id_cidade = 1
			elif cidade == 'Criciúma':
				id_cidade = 2
			elif cidade == 'Laguna':
				id_cidade = 3
			elif cidade == 'Garopaba':
				id_cidade = 4
			elif cidade == 'Floripa':
				id_cidade = 5

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')

			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM r_eventos WHERE id_cidade=%d ORDER BY data LIMIT 0, 4'%(id_cidade))
			eventos = cursor.fetchall()

			if eventos == []:
				self.ids.box1.clear_widgets()
				self.ids.box1.add_widget(Label(text='Nada na região de %s por enquanto'%(cidade)))

			else:
				self.ids.box1.clear_widgets()
				for i in range(len(eventos)):
					self.ids.box1.add_widget(BoxFeedEvento(telaevento, eventos[i]['link_imagem'], eventos[i]['nome'], eventos[i]['cidade'], eventos[i]['descricao'], eventos[i]['endereco']))
					self.load_count += 1
				self.ids.box1.add_widget(LoadButton(self.manager.ids.screen2, cidade, text='mais', size_hint_y=None, height='50dp', background_normal='', background_color=[0, 0, 0, .5]))

		def mostra_dados2(self, cidade, *args):
			telaevento = self.manager.ids.telaevento
			eventos = []
			id_cidade = None

			if cidade == 'Tubarão':
				id_cidade = 1
			elif cidade == 'Criciúma':
				id_cidade = 2
			elif cidade == 'Laguna':
				id_cidade = 3
			elif cidade == 'Garopaba':
				id_cidade = 4
			elif cidade == 'Floripa':
				id_cidade = 5

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')

			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM r_eventos WHERE id_cidade=%d ORDER BY data LIMIT %d, %d'%(id_cidade, self.load_count, 4))
			eventos = cursor.fetchall()

			self.ids.box1.remove_widget(self.ids.box1.children[0])
			if eventos != []:
				for i in range(len(eventos)):
					self.ids.box1.add_widget(BoxFeedEvento(telaevento, eventos[i]['link_imagem'], eventos[i]['nome'], eventos[i]['cidade'], eventos[i]['descricao'], eventos[i]['endereco']))
				self.ids.box1.add_widget(LoadButton(self.manager.ids.screen2, cidade, text='mais', size_hint_y=None, height='50dp', background_normal='', background_color=[0, 0, 0, .5]))
				self.ids.scroll1.scroll_to(self.ids.box1.children[4])
				self.load_count += 4

		@mainthread
		def mostra_carregando(self):
			self.ids.box1.add_widget(Label(text='Carregando...', color=[1, 1, 1, 1]))

		@mainthread
		def mostra_carregando2(self):
			self.ids.box1.remove_widget(self.ids.box1.children[0])
			self.ids.box1.add_widget(Label(text='Carregando...', size_hint_y=None, height='50dp', color=[1, 1, 1, 1]))

		def clear(self):
			self.ids.myspinner.text = 'Selecione uma região'

	class TelaBar(Screen):
		def __init__(self, **kwargs):
			super(TelaBar, self).__init__(**kwargs)

		def load(self, key, imagem, nome, cidade, endereco, contato, tela_anterior, *args):
			self.ids.box1.clear_widgets()
			self.manager.current = 'telabar'
			self.ids.title.title = nome
			self.ids.lbcidade.text = cidade
			self.ids.lbendereco.text = endereco
			self.ids.lbcontato.text = contato

			threading.Thread(target = self.mostra_carregando).start()
			threading.Thread(target = self.mostra_dados, args = (key,)).start()

		@mainthread
		def mostra_carregando(self):
			self.ids.box1.add_widget(Label(size_hint_y=None, height='50dp'))
			self.ids.box1.add_widget(Label(text='Carregando...', color = [1, 1, 1, 1]))

		def mostra_dados(self, key, *args):

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')
			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * from r_descricoes WHERE id_bar=%d ORDER BY data'%(key))
			bar_desc = cursor.fetchall()
			self.ids.box1.clear_widgets()
			for i in range(len(bar_desc)):
				self.ids.box1.add_widget(BoxFeedBar2(bar_desc[i]['link_imagem']))

	class TelaEvento(Screen):
		def __init__(self, **kwargs):
			super(TelaEvento, self).__init__(**kwargs)

		def load(self, nome, cidade, endereco, descricao, *args):
			self.manager.current = 'telaevento'
			self.ids.title.title = nome
			self.ids.lbcidade.text = cidade
			self.ids.lbendereco.text = endereco
			self.ids.lbdescricao.text = descricao

	class CriaEvento(Screen):

		def cria_evento(self, txtnome, spinnerregiao, spinnerdia, spinnermes, txtano, txtdescricao, *args):
			if self.ids.spinnerregiao.text != 'Selecione a região' and self.ids.txtnome.text != '' and self.ids.spinnerdia.text != 'Dia' and self.ids.spinnermes.text != 'Mês' and self.ids.txtano.text != '' and self.ids.txtdescricao.text != '':
				threading.Thread(target = self.mostra_criando).start()
				threading.Thread(target = self.registra_dados, args=(txtnome, spinnerregiao, spinnerdia, spinnermes, txtano, txtdescricao,)).start()

		@mainthread
		def mostra_criando(self):
			self.ids.btenvia.text = 'CRIANDO...'

		def registra_dados(self, txtnome, spinnerregiao, spinnerdia, spinnermes, txtano, txtdescricao, *args):

			id_cidade = None

			if spinnerregiao == 'Tubarão':
				id_cidade = 1
			elif spinnerregiao == 'Criciúma':
				id_cidade = 2
			elif spinnerregiao == 'Laguna':
				id_cidade = 3
			elif spinnerregiao == 'Garopaba':
				id_cidade = 4
			elif spinnerregiao == 'Floripa':
				id_cidade = 5

			if spinnermes == 'Janeiro':
				spinnermes = '01'
			elif spinnermes == 'Fevereiro':
				spinnermes = '02'
			elif spinnermes == 'Março':
				spinnermes = '03'
			elif spinnermes == 'Abril':
				spinnermes = '04'
			elif spinnermes == 'Maio':
				spinnermes = '05'
			elif spinnermes == 'Junho':
				spinnermes = '06'
			elif spinnermes == 'Julho':
				spinnermes = '07'
			elif spinnermes == 'Agosto':
				spinnermes = '08'
			elif spinnermes == 'Setembro':
				spinnermes = '09'
			elif spinnermes == 'Outubro':
				spinnermes = '10'
			elif spinnermes == 'Novembro':
				spinnermes = '11'
			elif spinnermes == 'Dezembro':
				spinnermes = '12'

			data = '%s-%s-%s'%(txtano, spinnermes, spinnerdia)

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')
			cursor = connection.cursor(dictionary=True)

			cursor.execute("INSERT INTO r_eventos_indie(id_cidade, nome, descricao, data) VALUES(%s, %s, %s, %s)", [id_cidade, txtnome, txtdescricao, data])
			connection.commit()
			Clock.schedule_once(self.muda_tela)

		def muda_tela(self, dt):
			self.manager.current = 'eventosindie'
			self.ids.txtnome.text = ''
			self.ids.txtano.text = ''
			self.ids.txtdescricao.text = ''
			self.ids.spinnerregiao.text = 'Selecione uma região'
			self.ids.spinnerdia.text = 'Dia'
			self.ids.spinnermes.text = 'Mês'
			self.ids.btenvia.text = 'CRIAR'

	class EventosIndie(Screen):
		load_count = 0
		def __init__(self, **kwargs):
			super(EventosIndie, self).__init__(**kwargs)

		def load(self, cidade):
			self.ids.box1.clear_widgets()
			if cidade != 'Selecione uma região':
				threading.Thread(target = self.mostra_carregando).start()
				threading.Thread(target = self.mostra_dados, args=(cidade,)).start()

		def load2(self, cidade, *args):
			threading.Thread(target = self.mostra_carregando2).start()
			threading.Thread(target = self.mostra_dados2, args=(cidade,)).start()

		def mostra_dados(self, cidade, *args):
			eventos = []
			id_cidade = 1

			if cidade == 'Tubarão':
				id_cidade = 1
			elif cidade == 'Criciúma':
				id_cidade = 2
			elif cidade == 'Laguna':
				id_cidade = 3
			elif cidade == 'Garopaba':
				id_cidade = 4
			elif cidade == 'Floripa':
				id_cidade = 5

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')

			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM r_eventos_indie WHERE id_cidade=%d ORDER BY data LIMIT 0, 4'%(id_cidade))
			eventos = cursor.fetchall()

			if eventos == []:
				self.ids.box1.clear_widgets()
				self.ids.box1.add_widget(Label(text='Nada na região de %s por enquanto'%(cidade)))

			else:
				self.ids.box1.clear_widgets()
				for i in range(len(eventos)):
					self.ids.box1.add_widget(BoxFeedEventoIndie(eventos[i]['nome'], eventos[i]['data'], eventos[i]['descricao']))
					self.load_count += 1
				self.ids.box1.add_widget(LoadButton(self.manager.ids.eventosindie, cidade, text='mais', size_hint_y=None, height='50dp', background_normal='', background_color=[0, 0, 0, .5]))

		def mostra_dados2(self, cidade, *args):
			telaevento = self.manager.ids.telaevento
			eventos = []
			id_cidade = None

			if cidade == 'Tubarão':
				id_cidade = 1
			elif cidade == 'Criciúma':
				id_cidade = 2
			elif cidade == 'Laguna':
				id_cidade = 3
			elif cidade == 'Garopaba':
				id_cidade = 4
			elif cidade == 'Floripa':
				id_cidade = 5

			connection = mysql.connector.connect(host='vitorproductions.com.br', user='vitor730_jonas', password='JonasVoceMeTraiu', db='vitor730_jonas', charset='utf8')

			cursor = connection.cursor(dictionary=True)
			cursor.execute('SELECT * FROM r_eventos_indie WHERE id_cidade=%d ORDER BY data LIMIT %d, %d'%(id_cidade, self.load_count, 4))
			eventos = cursor.fetchall()

			self.ids.box1.remove_widget(self.ids.box1.children[0])
			if eventos != []:
				for i in range(len(eventos)):
					self.ids.box1.add_widget(BoxFeedEventoIndie(eventos[i]['nome'], eventos[i]['data'], eventos[i]['descricao']))
				self.ids.box1.add_widget(LoadButton(self.manager.ids.eventosindie, cidade, text='mais', size_hint_y=None, height='50dp', background_normal='', background_color=[0, 0, 0, .5]))
				self.ids.scroll1.scroll_to(self.ids.box1.children[4])
				self.load_count += 4

		@mainthread
		def mostra_carregando(self):
			self.ids.box1.add_widget(Label(text='Carregando...', color=[1, 1, 1, 1]))

		@mainthread
		def mostra_carregando2(self):
			self.ids.box1.remove_widget(self.ids.box1.children[0])
			self.ids.box1.add_widget(Label(text='Carregando...', size_hint_y=None, height='50dp', color=[1, 1, 1, 1]))

		def clear(self):
			self.ids.spinnerregiao.text = 'Selecione uma região'
			self.ids.box1.clear_widgets()

	class BoxFeedBar(ButtonBehavior, AsyncImage):
		def __init__(self, telabar, key, imagem, nome, cidade, contato, endereco, **kwargs):
			super(BoxFeedBar, self).__init__(**kwargs)
			self.key = key
			self.source = imagem
			self.contato = contato
			self.endereco = endereco
			self.telabar = telabar
			self.nome = nome
			self.cidade = cidade

			self.bind(on_press = partial(self.telabar.load, self.key, self.source, self.nome, self.cidade, self.endereco, self.contato))

	class BoxFeedBar2(ButtonBehavior, AsyncImage):
		def __init__(self, imagem, **kwargs):
			super(BoxFeedBar2, self).__init__(**kwargs)

			self.source = imagem

	class BoxFeedEvento(ButtonBehavior, AsyncImage):
		def __init__(self, telaevento, link_imagem, nome, cidade, descricao, endereco, **kwargs):
			super(BoxFeedEvento, self).__init__(**kwargs)

			self.nome = nome.upper()
			self.descricao = descricao
			self.cidade = cidade
			self.source = link_imagem
			self.endereco = endereco
			self.telaevento = telaevento

			self.bind(on_press = partial(self.telaevento.load, self.nome, self.cidade, self.endereco, self.descricao))

	class BoxFeedEventoIndie(BoxLayout):
		def __init__(self, nome, data, descricao, **kwargs):
			super(BoxFeedEventoIndie, self).__init__(**kwargs)

			self.ids.titulo.text = nome.upper()
			self.data = str(data)
			self.ids.data.text = '%s%s/%s%s'%(self.data[8], self.data[9], self.data[5], self.data[6])
			self.ids.descricao.text = descricao

	class LoadButton(Button):
		def __init__(self, screen, cidade, **kwargs):
			super(LoadButton, self).__init__(**kwargs)

			self.cidade = cidade
			self.screen = screen
			self.bind(on_press = partial(self.screen.load2, self.cidade))

	class MyApp(App):
		def build(self):
			#Builder.load_string(io.open("nuhap.kv", encoding="utf-8").read())
			return TelaManager()

	MyApp().run()

except Exception as e:
	import kivy
	from kivy.app import App
	from kivy.uix.label import Label

	class MyApp(App):
		def build(self):
			return Label(text=str(e))

	MyApp().run()
