# File: voter_analytics/views.py
# Author: Ricky Cui (rcui1@bu.edu), 10/29/2026
# Description: Contains the classes for each view. 

from django.shortcuts import render
from django.views.generic import ListView, DetailView
import plotly
import plotly.graph_objs as go
from . models import Voter

# Create your views here.

class VoterListView(ListView):
    '''View to display voter results'''
 
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
 
    def get_queryset(self):
        
        # start with entire queryset
        results = super().get_queryset().order_by('last_name', 'first_name')
 
        # filter results by these field(s):
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation'].strip()
            if party:
                results = results.filter(party_affiliation=party)

        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                results = results.filter(dob__year__gte=min_dob)

        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                results = results.filter(dob__year__lte=max_dob)

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                results = results.filter(voter_score=voter_score)

        if 'v20state' in self.request.GET:
            results = results.filter(v20state=True)
            
        if 'v21town' in self.request.GET:
            results = results.filter(v21town=True)
            
        if 'v21primary' in self.request.GET:
            results = results.filter(v21primary=True)
            
        if 'v22general' in self.request.GET:
            results = results.filter(v22general=True)
            
        if 'v23town' in self.request.GET:
            results = results.filter(v23town=True)
                
        return results

    def get_context_data(self, **kwargs):
        '''Provide context variables for use in template'''
        context = super().get_context_data(**kwargs)
        
        context['parties'] = ['U', 'D', 'R', 'J', 'A', 'CC', 'X', 'L', 'Q', 'S', 'FF', 'G', 'HH', 'T', 'AA', 'GG', 'Z', 'O', 'P', 'E', 'V', 'H', 'Y', 'W', 'EE', 'K']
        context['years'] = range(1910, 2026)
        context['scores'] = range(0, 6)
        
        return context

class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''
 
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'


class VoterGraphsView(VoterListView):
    '''View to display graphs of aggregate voter data'''

    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        '''Provide graph context variables for use in template'''
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # graph 1: distribution by year of birth
        years = [v.dob.year for v in voters]
        fig_years = go.Histogram(x=years)
        title_text = "Voter Distribution by Year of Birth"
        graph_div_years = plotly.offline.plot({"data": [fig_years],  "layout_title_text": title_text,}, auto_open=False, output_type="div")
        context['graph_div_years'] = graph_div_years

        # graph 2: distribution by party affiliation
        party_counts = {}
        for v in voters:
            p = v.party_affiliation
            party_counts[p] = party_counts.get(p, 0) + 1

        fig_party = go.Pie(labels=list(party_counts.keys()), values=list(party_counts.values()))
        title_text = "Voter Distribution by Party Affiliation"
        graph_div_party = plotly.offline.plot({"data": [fig_party], "layout_title_text": title_text,}, auto_open=False, output_type="div")
        context['graph_div_party'] = graph_div_party

        # graph 3: participation in each of the 5 elections
        elections = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        counts = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]
        fig_elections = go.Bar(x=elections, y=counts)
        title_text = "Vote Count by Election"
        graph_div_elections = plotly.offline.plot({"data": [fig_elections], "layout_title_text": title_text,} , auto_open=False, output_type="div")
        context['graph_div_elections'] = graph_div_elections

        return context
