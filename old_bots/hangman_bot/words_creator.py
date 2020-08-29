ABC = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ' \
      'a b c d e f g h i j k l m n o p q r s t u v w x y z '.split()

ABC_RU = 'А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я ' \
         'а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я '.split()
f = open('words.txt', encoding="utf-8")
words = list(f.read())
f.close()

for i in range(0, len(words)):
    if words[i] not in ABC_RU:
        words[i] = ' '

for i in range(0, len(words) - 1):
    if words[i] == ' ' and words[i + 1] != ' ' and words[i - 1] != ' ':
        words[i] = '_'

f = open('words.txt', 'w', encoding="utf-8")
f.write(str(' '.join(''.join(words).split())))
