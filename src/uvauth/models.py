from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

CAMPI = (
    ('ndf', 'Não definido'),
    ('aca', 'Acaraú'),
    ('aco', 'Acopiara'),
    ('ara', 'Aracati'),
    ('bat', 'Baturité'),
    ('boa', 'Boa Viagem'),
    ('cam', 'Camocim'),
    ('caj', 'Canindé'),
    ('cau', 'Caucaia'),
    ('ced', 'Cedro'),
    ('cra', 'Crateús'),
    ('cro', 'Crato'),
    ('for', 'Fortaleza'),
    ('gua', 'Guaramiranga'),
    ('hor', 'Horizonte'),
    ('igu', 'Iguatu'),
    ('ita', 'Itapipoca'),
    ('jag', 'Jaguaribe'),
    ('jau', 'Jaguaruana'),
    ('juz', 'Juazeiro do Norte'),
    ('lim', 'Limoeiro do Norte'),
    ('mar', 'Maracanaú'),
    ('man', 'Maranguape'),
    ('mom', 'Mombaça'),
    ('mor', 'Morada Nova'),
    ('par', 'Paracuru'),
    ('pec', 'Pecém'),
    ('pol', 'Polo de Inovação'),
    ('qui', 'Quixadá'),
    ('rei', 'Reitoria'),
    ('sob', 'Sobral'),
    ('tab', 'Tabuleiro do Norte'),
    ('tau', 'Tauá'),
    ('tia', 'Tianguá'),
    ('uba', 'Ubajara'),
    ('umi', 'Umirim'),
)

VINCULOS = (
    ('doc', 'Docente'),
    ('dis', 'Discente'),
    ('tae', 'Técnico Administrativo'),
    ('des', 'Desconhecido'),
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, vinculo, password=None):
        if not email:
            raise ValidationError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email),
            vinculo=vinculo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, vinculo, password=None):
        user: User = self.create_user(
            email,
            vinculo=vinculo,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


def email_do_ifce_valitation(value):
    if not (value.endswith('@ifce.edu.br') or value.endswith('@aluno.ifce.edu.br')):
        raise ValidationError(
            _(
                'Users must have email address '
                'ending with @ifce.edu.br or @aluno.ifce.edu.br'
            )
        )


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[email_do_ifce_valitation])
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    campus = models.CharField(max_length=3, choices=CAMPI, default='ndf')

    vinculo = models.CharField(
        'vínculo', max_length=3, choices=VINCULOS, default=VINCULOS[0][0]
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['vinculo']

    objects = MyUserManager()

    def __str__(self):
        return self.email
