from django.contrib import admin
from django.utils import timezone
from django.conf import settings

from .models import QuestionOption
from .models import Question
from .models import Voting
from .models import PoliticalParty
from mixnet.models import Auth

from .filters import StartedFilter



class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    def start(self, request, queryset):
        for v in queryset.all():
            v.create_pubkey()
            v.start_date = timezone.now()
            v.save()


    def stop(self, request, queryset):
        for v in queryset.all():
            v.end_date = timezone.now()
            v.save()


    def tally(self, request, queryset):
        for v in queryset.filter(end_date__lt=timezone.now()):
            token = request.session.get('auth-token', '')
            tie = v.tally_votes(token)
            if (tie):
                self.message_user(request, "The tally was successful but the voting was INVALID because a tie has occurred (one of the tied options has been given as the winner). Repeat the vote if you want to break the tie.")

    actions = [ start, stop, tally ]


class PoliticalPartyAdmin(admin.ModelAdmin):
    readonly_fields = ('president',)

    def createPresidentialVoting(self, request, queryset):
        question = Question(desc='Who do you want the president of Españistán to be?')
        question.save()

        for i in queryset.all():
            opt = QuestionOption(question=question, option=i.president)
            opt.save()

        v = Voting(name='Presidential Voting', question=question)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})                                   
        a.save()
        v.auths.add(a) 
        v.yes_no_question = 'False'
        v.create_pubkey()

        v.tipe = 'P'
        v.save()
        self.message_user(request, "Presidential election successfully created" )  

    createPresidentialVoting.short_description = "Create new Presidential voting"

    actions = [createPresidentialVoting, ]

admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(PoliticalParty,PoliticalPartyAdmin)