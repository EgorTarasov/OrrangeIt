from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE
from tempus_dominus.widgets import DateTimePicker
from .models import EventInfo, ImagesGen
import datetime


class CreateImagesGen(forms.ModelForm):
    class Meta:
        model = ImagesGen
        fields = ['image']


class CreateEventForm(forms.ModelForm):
    event_name = forms.CharField(
        max_length=128,
        required=True,
        label='Event name',
        error_messages={
            'max_length': 'The maximum length of a possible event name is 128.',
            'required': 'Event name is required.'
        },
        widget=forms.TextInput(
            attrs={
                'id': 'event_name',
                'placeholder': 'Event name',
                'autofocus': True,
                'class': "form-control form-control-lg field_input",

            }
        )
    )

    event_description = forms.CharField(
        max_length=16384,
        required=True,
        label='Event description',
        error_messages={
            'max_length': 'The maximum length of a description is 512.',
            'required': 'Description is required.'
        },
        widget=TinyMCE(
            attrs={
                'size': '50',
                'autofocus': True,
                'class': "form-control ",
                'placeholder': 'Event description',
                'id': 'event_description',
                'cols': 80,
                'rows': 20,
            }
        )
    )

    event_begin = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={
                'format': 'Y-M-D H:m',
                'minDate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                'date': (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'),
                #'inline': False,
                'sideBySide': True,

            },
            attrs={
                'input_toggle': True,
                #'style': 'visibility: hidden',
                'id': 'event_begin'
            }
        ),
    )

    event_end = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(
            options={
                'format': 'Y-M-D H:m',
                'minDate': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                'date': (datetime.datetime.now() + datetime.timedelta(hours=2, days=1)).strftime('%Y-%m-%d %H:%M'),
                #'inline': False,
                'sideBySide': True,
            },
            attrs={
                'input_toggle': True,
                #'style': 'visibility: hidden',
                'id': 'event_end'
            }
        ),
    )

    event_people_needed = forms.IntegerField(
        label='Needed amount of people',
        required=False,
        min_value=1,
        max_value=35000,
        error_messages={
            'min_value': 'Don`t you need somebody to looove?',
            'max_value': 'Too many, sorry'
        },

        widget=forms.NumberInput(
            attrs={
                'placeholder': '12 *optional',
                'autofocus': True,
                'class': "form-control field_input",

            }
        )
    )

    event_address = forms.CharField(
        max_length=128,
        required=True,
        label='Address',
        error_messages={
            'max_length': 'The maximum length of a possible event name is 128.',
            'required': 'Address is required.'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Baker street, 221b',
                'autofocus': True,
                'class': "form-control field_input",
                'id': 'address_suggest',
            }
        )
    )

    event_tags = forms.CharField(max_length=1024, required=True, widget=forms.HiddenInput(
        attrs={
            'id': 'tagsField',
            'data-tags-input-name': 'tag',
            'class': 'field_input'
        }
    ),
        error_messages={
            'max_length': 'Too many tags',
            'requered': 'Input at least 1 tag'
        }
    )

    telegram_group_link = forms.CharField(max_length=64, required=False, widget=forms.HiddenInput(
        attrs={
            'id': 'telegramGroupLinkField',
        }
    ),
    )

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(
            attrs={
                'id': 'event_image',
                'class': 'image_field '
            }
        )
    )

    gallery_images = forms.ImageField(
        required=False,
        max_length=64,
        widget=forms.FileInput(
            attrs={
                'multiple': True,
                'id': 'gallery_images',
                'class': 'image_field'
            }
        )
    )

    class Meta:
        model = EventInfo
        fields = ['event_name', 'event_tags',
                  'event_description', 'event_begin',
                  'event_end', 'event_address',
                  'event_people_needed', 'image',
                  ]


class CommentForm(forms.Form):
    text = forms.CharField(
        label='Write a comment',
        max_length=100000,
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'style': 'background-color: #3a3434; color: white',
                'id': 'comment-input'
            }
        )
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=128, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }
    ))
    name = forms.CharField(max_length=128,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Name (John Doe, Gorky Park)'
                               }
                           ))
    username = forms.CharField(max_length=64, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ))

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password confirmation'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password1', 'password2')


class LogInForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'This field is required'}, required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Username'
                                   }
                               ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ))

    class Meta:
        fields = ('username', 'password')


#  class="form-control mt-3 changable" type="text" value="{{ user.first_name|title }}" readonly
class UserEditForm(forms.Form):
    first_name = forms.CharField(
        required=False, label='Name', max_length=128,
        widget=forms.TextInput(
                attrs={
                    'class': 'form-control mt-3 changable',
                    'type': 'text',
                }
        )
    )
    email = forms.EmailField(
        required=False, label='Email', max_length=128,
        widget=forms.EmailInput(
                attrs={
                    'class': 'form-control mt-3 changable',
                    'type': 'text',
                }
        )
    )
    user_avatar = forms.ImageField(
        label='Profile picture',
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name',  'email', 'user_avatar')
