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
    title = forms.Charfield(max_length=128, help_text="Please enter the page name.")
    url = forms.URLField(max_length=200, help_text="Please enter the page URL.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # We can do it by either listing the fields we want to include
        # (like with did about with fields=())
        # or we can tell it which fields _not_ to include, using...
        exclude = ('category', )