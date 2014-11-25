from django import forms
from rango.models import Page, Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # this will provide additional info about the form
    class Meta:
        # provide association btwn ModelForm and a model
        # this is really, really necessary.
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the page name.")
    url = forms.URLField(max_length=200, help_text="Please enter the page URL.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    category = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # We can do it by either listing the fields we want to include
        # (like with did about with fields=())
        # or we can tell it which fields _not_ to include, using...
        # exclude = ('category', 'views')
        ## TODO I THINK I FIXED THIS. NEED TO MIGRATE AND TRY THE add_page() again.
        # and in dj 1.7 it's necessary to say which fields are included using...
        fields = ('title', 'url')

    def clean(self):
        cleaned_data = self.cleaned_data
        # cleaned_data is a ModelForm dictionary attribute.
        url = cleaned_data.get('url')
        # we use the dictionary.get() method to get the form's value for url

        # if url isn't empty and doesn't start with http://
        if url and not url.startswith('http://'):
            url = 'http://' + url
            # we reassign the value in the dictionary with our new, clean url
            cleaned_data['url'] = url
        # we always have to end the clean() method by returning the cleaned_data dictionary.
        # always, always, always, always, always.
        return cleaned_data