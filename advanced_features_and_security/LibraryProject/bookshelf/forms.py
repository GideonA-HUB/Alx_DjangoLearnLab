from django import forms

class BookSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)