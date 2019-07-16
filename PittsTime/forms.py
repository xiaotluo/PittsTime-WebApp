from django import forms
from django.contrib.auth import authenticate
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from PittsTime.models import *
import bleach
# from django_bleach.forms import BleachField

MAX_UPLOAD_SIZE = 2500000

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())
    email = forms.CharField(max_length=50,
                            widget=forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        username = cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        email = cleaned_data.get('email')
        if User.objects.filter(email__exact = email):
            raise forms.ValidationError("Email is already taken.")
        return cleaned_data

 
        # We must return the cleaned data we got from our parent.
    # Customizes form validation for the username field.
    # def clean_username(self):
    #     # Confirms that the username is not already present in the
    #     # User model database.
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username__exact=username):
    #         raise forms.ValidationError("Username is already taken.")
    #     # email = self.cleaned_data.get('email')
    #     # if User.objects.filter(email__exact=email):
    #     #     raise forms.ValidationError("This email is already used for another account.")
    #     # We must return the cleaned data we got from the cleaned_data
    #     # dictionary
    #     return username
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email__exact = email):
    #         raise forms.ValidationError("Email is already taken.")

class BlogForm(forms.ModelForm):
    Blog_content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = ('title','Blog_content','tags')

    def clean(self):
        data = self.cleaned_data
        tags = self.cleaned_data['tags']
        #print(tags)
        # Blog_content=data.get("Blog_content")
        # data['Blog_content'] = bleach.clean(Blog_content)
        return data

    def clean_tags(self):
        tags = self['tags'].data
        print(tags)
        if ',' not in tags:
            # new_tag = []
            # one_tag = ""
            # print(tags)
            # for i,e in list(enumerate(tags)):
            #     one_tag += e
            #     if i != len(tags) - 1:
            #         one_tag += ' '
            # #print(one_tag)
            # new_tag.append(one_tag)
            # tags = new_tag
            # print(tags)
            tags += ','
        cleaned_tag = [t.strip() for t in tags.split(',') if t != '']
        
        print(cleaned_tag)
        return cleaned_tag


    # def clean_Blog_content(self):
    #     content = self.cleaned_data.get('Blog_content')
    #     content = bleach.clean(content)
    #     return content
        # cleaned_data['Blog_content'] = bleach.clean(Blog_content)

    #     super(LogCollectorParamsForm, self)._clean_fields()
    #     for name, value in self.cleaned_data.items():
    #         self.cleaned_data[name] = bleach.clean(value)

class ProfileForm(forms.ModelForm):
    bio_text = forms.CharField( widget=forms.Textarea() )
    class Meta:
        model = Profile
        fields =('bio_picture','bio_text',)

    def clean_picture(self):
        picture = self.cleaned_data['bio_picture']
        if not hasattr(picture,'content_type'):
            # raise forms.ValidationError('You must upload a picture')
            return  'You must upload a picture!'
        if not picture.content_type or not picture.content_type.startswith('image'):
            # raise forms.ValidationError('File type is not image')
            return 'File type is not image!'
        if picture.size > MAX_UPLOAD_SIZE:
            # raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
            return 'File too big!'
        return picture


