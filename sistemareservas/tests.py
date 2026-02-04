from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import CategoriaEvento, Evento, Inscricao
from .forms import SignUpForm, CategoriaEventoForm


class ModelsTest(TestCase):
	def setUp(self):
		self.organizador = User.objects.create_user(username='org', password='pass')
		self.participante = User.objects.create_user(username='part', password='pass')
		self.categoria = CategoriaEvento.objects.create(nome='Palestra')
		self.evento = Evento.objects.create(
			titulo='Meu Evento',
			descricao='Descricao',
			data=timezone.now(),
			local='Sala 1',
			categoria=self.categoria,
			organizador=self.organizador,
		)

	def test_categoria_str(self):
		self.assertEqual(str(self.categoria), 'Palestra')

	def test_evento_str(self):
		self.assertEqual(str(self.evento), 'Meu Evento')

	def test_usuario_inscrito(self):
		# inicialmente não inscrito
		self.assertFalse(self.evento.usuario_inscrito(self.participante))
		# criar inscrição e verificar
		Inscricao.objects.create(participante=self.participante, evento=self.evento)
		self.assertTrue(self.evento.usuario_inscrito(self.participante))

	def test_inscricao_unique_constraint(self):
		Inscricao.objects.create(participante=self.participante, evento=self.evento)
		with self.assertRaises(IntegrityError):
			Inscricao.objects.create(participante=self.participante, evento=self.evento)


class FormsTest(TestCase):
	def test_categoriaevento_form_valid(self):
		form = CategoriaEventoForm({'nome': 'Workshop'})
		self.assertTrue(form.is_valid())
		obj = form.save()
		self.assertEqual(obj.nome, 'Workshop')

	def test_signup_form_duplicate_email(self):
		User.objects.create_user(username='exists', email='a@b.com', password='pass')
		form = SignUpForm({
			'username': 'novo',
			'email': 'a@b.com',
			'password1': 'pass12345',
			'password2': 'pass12345',
		})
		self.assertFalse(form.is_valid())
		self.assertIn('email', form.errors)

	def test_signup_form_save_creates_user(self):
		form = SignUpForm({
			'username': 'novo2',
			'email': 'novo2@ex.com',
			'password1': 'pass12345',
			'password2': 'pass12345',
		})
		self.assertTrue(form.is_valid())
		user = form.save()
		self.assertEqual(user.email, 'novo2@ex.com')


class ViewsTest(TestCase):
	def setUp(self):
		self.org = User.objects.create_user(username='org2', password='pass')
		self.part = User.objects.create_user(username='part2', password='pass')
		self.cat = CategoriaEvento.objects.create(nome='C')
		self.evento = Evento.objects.create(
			titulo='Ev', descricao='D', data=timezone.now(), local='L', categoria=self.cat, organizador=self.org
		)

	def test_home_view(self):
		resp = self.client.get(reverse('home'))
		self.assertEqual(resp.status_code, 200)

	def test_evento_list_requires_login(self):
		resp = self.client.get(reverse('evento_list'))
		self.assertEqual(resp.status_code, 302)

	def test_signup_and_login_flow(self):
		data = {
			'username': 'flowuser',
			'email': 'flow@ex.com',
			'password1': 'complexpass123',
			'password2': 'complexpass123',
		}
		resp = self.client.post(reverse('signup'), data)
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(User.objects.filter(username='flowuser').exists())

	def test_inscricao_criar(self):
		# sem login -> redirect
		resp = self.client.get(reverse('inscricao_criar', args=[self.evento.pk]))
		self.assertEqual(resp.status_code, 302)

		# com login -> cria inscrição
		self.client.login(username='part2', password='pass')
		resp2 = self.client.get(reverse('inscricao_criar', args=[self.evento.pk]))
		self.assertEqual(resp2.status_code, 302)
		self.assertTrue(Inscricao.objects.filter(participante=self.part, evento=self.evento).exists())

