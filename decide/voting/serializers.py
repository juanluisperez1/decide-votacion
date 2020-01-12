from rest_framework import serializers

from .models import Question, QuestionOption, Voting, PoliticalParty
from base.serializers import Key, AuthSerializer

class KeySerializer(serializers.HyperlinkedModelSerializer):
    p = serializers.CharField()
    g = serializers.CharField()
    y = serializers.CharField()

    class Meta:
        model = Key
        fields = ('p', 'g', 'y')

class PoliticalPartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PoliticalParty
        fields = ('name', 'acronym', 'description', 'headquarters', 'image', 
                    'president')

class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    political_party = PoliticalPartySerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc', 
                  'tipe', 'province', 'political_party')       



class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')
