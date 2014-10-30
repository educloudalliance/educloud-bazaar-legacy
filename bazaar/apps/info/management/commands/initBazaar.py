from django.core.management.base import BaseCommand, CommandError
from oscar.core.loading import get_class, get_model
from django.template.defaultfilters import slugify


Language = get_model('catalogue', 'Language')
ProductType = get_model('catalogue', 'ProductClass')
ProductFormat = get_model('catalogue', 'ProductFormat')
Subject = get_model('catalogue', 'Category')

languages = [
'aa', #	Afar
'ab', # Abkhazian
'af', #	Afrikaans
'am', #	Amharic
'ar', #	Arabic
'as', #	Assamese
'ay', # Aymara
'az', #	Azerbaijani
'ba', # Bashkir
'be', #	Byelorussian
'bg', #	Bulgarian
'bh', #	Bihari
'bi', #	Bislama
'bn', #	Bengali
'bo', #	Tibetan
'br', #	Breton
'ca', # Catalan
'co', #	Corsican
'cs', #	Czech
'cy', #	Welch
'da', #	Danish
'de', #	German
'dz', #	Bhutani
'el', #	Greek
'en', #	English
'eo', #	Esperanto
'es', #	Spanish
'et', #	Estonian
'eu', #	Basque
'fa', #	Persian
'fi', #	Finnish
'fj', #	Fiji
'fo', #	Faeroese
'fr', #	French
'fy', #	Frisian
'ga', #	Irish
'gd', #	Scots Gaelic
'gl', #	Galician
'gn', #	Guarani
'gu', #	Gujarati
'ha', #	Hausa
'hi', #	Hindi
'he', #	Hebrew
'hr', #	Croatian
'hu', #	Hungarian
'hy', #	Armenian
'ia', #	Interlingua
'id', #	Indonesian
'ie', #	Interlingue
'ik', #	Inupiak
'in', #	former Indonesian
'is', #	Icelandic
'it', #	Italian
'iu', #	Inuktitut (Eskimo)
'iw', #	former Hebrew
'ja', #	Japanese
'ji', #	former Yiddish
'jw', #	Javanese
'ka', #	Georgian
'kk', #	Kazakh
'kl', #	Greenlandic
'km', #	Cambodian
'kn', #	Kannada
'ko', #	Korean
'ks', #	Kashmiri
'ku', #	Kurdish
'ky', #	Kirghiz
'la', #	Latin
'ln', #	Lingala
'lo', #	Laothian
'lt', #	Lithuanian
'lv', #	Latvian, Lettish
'mg', #	Malagasy
'mi', #	Maori
'mk', #	Macedonian
'ml', #	Malayalam
'mn', #	Mongolian
'mo', #	Moldavian
'mr', #	Marathi
'ms', #	Malay
'mt', #	Maltese
'my', #	Burmese
'na', #	Nauru
'ne', #	Nepali
'nl', #	Dutch
'no', #	Norwegian
'oc', #	Occitan
'om', #	(Afan) Oromo
'or', #	Oriya
'pa', #	Punjabi
'pl', #	Polish
'ps', #	Pashto, Pushto
'pt', #	Portuguese
'qu', #	Quechua
'rm', #	Rhaeto-Romance
'rn', #	Kirundi
'ro', #	Romanian
'ru', #	Russian
'rw', #	Kinyarwanda
'sa', #	Sanskrit
'sd', #	Sindhi
'sg', #	Sangro
'sh', #	Serbo-Croatian
'si', #	Singhalese
'sk', #	Slovak
'sl', #	Slovenian
'sm', #	Samoan
'sn', #	Shona
'so', #	Somali
'sq', #	Albanian
'sr', #	Serbian
'ss', #	Siswati
'st', #	Sesotho
'su', #	Sudanese
'sv', #	Swedish
'sw', #	Swahili
'ta', #	Tamil
'te', #	Tegulu
'tg', #	Tajik
'th', #	Thai
'ti', #	Tigrinya
'tk', #	Turkmen
'tl', #	Tagalog
'tn', #	Setswana
'to', #	Tonga
'tr', #	Turkish
'ts', #	Tsonga
'tt', #	Tatar
'tw', #	Twi
'ug', #	Uigur
'uk', #	Ukrainian
'ur', #	Urdu
'uz', #	Uzbek
'vi', #	Vietnamese
'vo', #	Volapuk
'wo', #	Wolof
'xh', #	Xhosa
'yi', #	Yiddish
'yo', #	Yoruba
'za', #	Zhuang
'zh', #	Chinese
'zu', #	Zulu
]

producttypes = [
    'Photo',
    'Video',
    'Executable',
    'Compressed',
    'Link',
    'Rich',
    'PDF',
]

productformats = [
    'Exam',
    'Additional Material',
    'Teachers Material',
    'Hybrid',
    'Exercise Book',
    'Textbook',
    'Other',
]

subjects = [
    'Finnish',
    'Finnish as a second language',
    'Swedish',
    'Swedish as a seconf language',
    'English',
    'German',
    'French',
    'Russian',
    'Biology',
    'Chemistry',
    'Environmental Studies',
    'Geography',
    'Health Education',
    'Home Economics',
    'History',
    'Mathematics',
    'Physics',
    'Religion & Ethics',
    'Art & Design',
    'Crafts',
    'Music',
    'Physical Education',
    'Other',
]


class Command(BaseCommand):
    help = 'Initializes Bazaar'

    def handle(self, *args, **options):

        self.stdout.write('EduCloud Bazaar initializing command v. 1.0')

        # Install languages into database
        self.stdout.write('Installing languages...')
        qs = Language.objects.all()
        for language in languages:
            if not qs.filter(name=language).exists():
                newLang = Language(name=language)
                newLang.save()
            else:
                self.stdout.write('Language %s already exists' % language)

        # Install producttypes into Database
        self.stdout.write('Installing product types...')
        qs = ProductType.objects.all()
        for producttype in producttypes:
            if not qs.filter(name=producttype).exists():
                newProduct = ProductType(name=producttype)
                newProduct.save()
            else:
                self.stdout.write('Product Type %s already exists' % producttype)

        # Install productformats into Database
        self.stdout.write('Installing product formats...')
        qs = ProductFormat.objects.all()
        for productformat in productformats:
            if not qs.filter(name=productformat).exists():
                newFormat = ProductFormat(name=productformat, slug=slugify(productformat))
                newFormat.save()
            else:
                self.stdout.write('Product Format %s already exists' % productformat)

        # Install subjects into Database
        self.stdout.write('Installing subjects ...')
        qs = Subject.objects.all()
        for subject in subjects:
            if not qs.filter(name=subject).exists():
                highest = Subject.objects.latest('id').path

                # Remove 0s
                pathStr = highest.replace("0", "")
                path = int(pathStr)
                path = path + 1
                pathStr = str(path)

                while(pathStr.count() < 4):
                    pathStr = "0" + pathStr

                newSubject = Subject(name=subject, path = pathStr, depth = 1, slug=slugify(subject), full_name=subject)
                newSubject.save()
            else:
                self.stdout.write('Subject %s already exists' % subject)

        self.stdout.write('All needed objects installed into database!')
        self.stdout.write('You are now ready to use EduCloud Bazaar')


        return 0
