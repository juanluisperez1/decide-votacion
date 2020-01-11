import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption, PoliticalParty
from django.db import IntegrityError
from django.db import transaction
from authentication.models import UserProfile
from datetime import date
from .serializers import  PoliticalPartySerializer


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        q = Question(desc='test question')
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q, tipe='testType')
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)):
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'vote': { 'a': a, 'b': b },
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        for q in v.question.options.all():
            self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse']
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # # STATUS VOTING: not started
        # for action in ['stop', 'tally']:
        #     data = {'action': action}
        #     response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        #     self.assertEqual(response.status_code, 400)
        #     self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        # data = {'action': 'tally'}
        # response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        # self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        # data = {'action': 'tally'}
        # response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        # data = {'action': 'tally'}
        # response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        # self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json(), 'Voting already tallied')

    def test_create_political_party(self):
    
        test=[
             #We create a correct political party
            ['test name','ta','test description','test headquarters','https;//testImage.es',None],
            #We try create the same political party
            ['test name','ta','test description','bad','https;//testImage.es',IntegrityError],
            #We try create the a political party with a bad name
            [None,'ta2','test description','bad','https;//testImage.es',IntegrityError],
            #We try create the a political party with a bad acronym
            ['test name',None,'test description','bad','https;//testImage.es',IntegrityError],
            #We try create the a political party with a bad headquarters
            ['test name',None,'test description',None,'https;//testImage.es',IntegrityError],
            #We try create the a political party with a bad URL
            ['test name',None,'test description',None,'testImage',IntegrityError]
        ]
        
        for value in test:

            try:
                with transaction.atomic():
                    political_party = PoliticalParty(name=value[0], acronym=value[1],description=value[2], headquarters=value[3],image=value[4])
                    political_party.save()
                    political_party_DB = PoliticalParty.objects.get(name=value[0])
            
                self.assertEqual(political_party, political_party_DB)

                if(value[5] != None):
                    self.assertEqual(False, True)

            except value[5]:
                self.assertEqual(True, True)
            except Exception:    
                self.assertEqual(False, True)



    def create_voting_presidential_primaries(self):

        u = User(username='president')
        u.set_password('123')
        u.save()

        q = Question(desc='test question')
        q.save()

        opt = QuestionOption(question=q, option='president')
        opt.save()
        
        political_party = PoliticalParty(name='for president', acronym='test',description='test', headquarters='test')
        political_party.save()

        birthdate= date(2000, 2, 28)
        userProfile = UserProfile(related_political_party=political_party,birthdate=birthdate,sex='F',related_user=u,province='S',employment='B')
        userProfile.save()
        
        v = Voting(name='test voting', question=q, tipe='PP',political_party=political_party)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v     

    def test_update_president_political_party(self):
        
    
        v = self.create_voting_presidential_primaries()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        political_party_DB = PoliticalParty.objects.get(name='for president')
        self.assertEqual('president', political_party_DB.president)


    def create_voting_senate_primaries(self):

        u = User(username='senator')
        u.set_password('123')
        u.save()

        q = Question(desc='test question')
        q.save()

        opt = QuestionOption(question=q, option='senator')
        opt.save()
        
        political_party = PoliticalParty(name='for senator', acronym='test',description='test', headquarters='test')
        political_party.save()

        birthdate= date(2000, 2, 28)
        userProfile = UserProfile(related_political_party=political_party,birthdate=birthdate,sex='F',related_user=u,province='S',employment='B')
        userProfile.save()
        
        v = Voting(name='test voting', question=q, tipe='SP',political_party=political_party)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v


    def test_appoint_senator(self):

        v = self.create_voting_senate_primaries()
        self.create_voters(v)

        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()

        self.store_votes(v)

        self.login()  # set token
        v.tally_votes(self.token)

        tally = v.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}

        user=User.objects.get(username='senator')
        user_profile_DB = UserProfile.objects.get(related_user=user)
        self.assertEqual('S', user_profile_DB.employment)


class VotingsPerUserAPI(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_get_voting_per_user_empty(self):

        response = self.client.get('/voting/user/?id={}'.format(-1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_voting_per_user(self):

        for i in range(2):
            q = Question(desc='test question')
            q.save()
            for j in range(5):
                opt = QuestionOption(question=q, option='option {}'.format(j+1))
                opt.save()
            v = Voting(name='test voting', question=q, tipe='testType')
            v.save()

            a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
            a.save()
            v.auths.add(a)

        u, _ = User.objects.get_or_create(username='voter')
        u.is_active = True
        u.save()

        for v in Voting.objects.all():
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

        response = self.client.get('/voting/user/?id={}'.format(u.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)



class GetAllPoliticalPartyTestAPI(TestCase):
    # Declaramos varios objetos del tipo PArtido Político para popular la base de datos

    def setUp(self):
        PoliticalParty.objects.create(
            name='Partido Selenium', acronym='PSM', description='Una descripcion válida', headquarters='calle inventada', image='http://unaurl.com')
        PoliticalParty.objects.create(
            name='Partido Selenium 2', acronym='PSM2', description='Una descripcion válida2', headquarters='calle inventada2', image='http://unaurl.com2')
        PoliticalParty.objects.create(
            name='Partido Selenium 3', acronym='PSM3', description='Una descripcion válida3', headquarters='calle inventada3', image='http://unaurl.com3')
        PoliticalParty.objects.create(
            name='Partido Selenium 4', acronym='PSM4', description='Una descripcion válida4', headquarters='calle inventada4', image='http://unaurl.com4')

    def test_get_all_puppies(self):
        # get API response
        response = self.client.get(reverse('get_post_politicalparty'))
        # get data from db
        politicalparties = PoliticalParty.objects.all()
        serializer = PoliticalPartySerializer(politicalparties, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePoliticalPartyTest(TestCase):
    # Declaramos varios objetos del tipo PArtido Político para popular la base de datos

    def setUp(self):
        self.psm1 = PoliticalParty.objects.create(
            name='Partido Selenium', acronym='PSM', description='Una descripcion válida', headquarters='calle inventada', image='http://unaurl.com')
        self.psm2 = PoliticalParty.objects.create(
            name='Partido Selenium 1', acronym='PSM 1', description='Una descripcion válida 1', headquarters='calle inventada 1', image='http://unaurl.com1')
        self.psm3 = PoliticalParty.objects.create(
            name='Partido Selenium 2', acronym='PSM 2', description='Una descripcion válida 2', headquarters='calle inventada 2', image='http://unaurl.com2')
        self.psm5 = PoliticalParty.objects.create(
            name='Partido Selenium 3', acronym='PSM 3', description='Una descripcion válida 3', headquarters='calle inventada 3', image='http://unaurl.com3')

    def test_get_valid_single_politicalParty(self):
        response = self.client.get(
            reverse('get_delete_update_politicalparty', kwargs={'pk': self.psm1.pk}))
        politicalparty = PoliticalParty.objects.get(pk=self.psm1.pk)
        serializer = PoliticalPartySerializer(politicalparty)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_politicalParty(self):
        response = self.client.get(
            reverse('get_delete_update_politicalparty', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

