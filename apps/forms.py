from django import forms

class SearchApp(forms.Form):
    q = forms.CharField(max_length=30)
    def clean(self):
        cleaned_data = super(SearchApp, self).clean()
        q = cleaned_data.get('q')