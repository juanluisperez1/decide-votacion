from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting
from .models import PoliticalParty

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

admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(PoliticalParty,PoliticalPartyAdmin )