from django import forms



class CommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'cols': 15, 'rows': 2}
        )
    )
