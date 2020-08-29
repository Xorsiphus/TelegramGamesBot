import json

ANIMALS_EN = ('BABOON BADGER BEAR BEAVER CAMEL COBRA COUGAR WOODPECKER '
              'COYOTE DONKEY EAGLE FERRET GOAT HARE PUPPY SQUIRREL '
              'GOOSE LIZARD MOLE MONKEY MOOSE MOUSE MULE PENGUIN '
              'OTTER PANDA PARROT PIGEON PYTHON RABBIT RAVEN HERON '
              'RHINO SALMON SEAL SKUNK SLOTH SNAKE SPIDER HEDGEHOG '
              'STORK TIGER TOAD TROUT TURKEY TURTLE WEASEL WHALE '
              'WOMBAT ZEBRA CROCODILE HIPPOPOTAMUS CHICKEN ').split()

ANIMALS_RU = ("МУРАВЕЙ БАБУИН БАРСУК ЛЕТУЧАЯ МЕДВЕДЬ ВЕРБЛЮД КОШКА МОЛЛЮСК КОБРА ПУМА "
              "КОЙОТ ВОРОНА ОЛЕНЬ СОБАКА ОСЕЛ УТКА ОРЕЛ ХОРЕК ЛИСА ЛЯГУШКА КОЗЕЛ "
              "ЯСТРЕБ ЯЩЕРИЦА ЛАМА ОБЕЗЬЯНА ТРИТОН ЩЕНОК БЕГЕМОТ ЦЫПЛЁНОК ЦАПЛЯ "
              "ВЫДРА СОВА ПАНДА ПОПУГАЙ ГОЛУБЬ ПИТОН КРОЛИК КРЫСА ВОРОН ДЯТЕЛ "
              "НОСОРОГ ЛОСОСЬ ТЮЛЕНЬ АКУЛА ОВЦА СКУНС ЛЕНИВЕЦ ЗМЕЯ ПАУК "
              "АИСТ ЛЕБЕДЬ ЖАБА ФОРЕЛЬ ИНДЕЙКА ЧЕРЕПАХА ЛАСКА ВОЛК БЕЛКА "
              "ВОМБАТ ЗЕБРА КРОКОДИЛ ЛИСИЦА БАРАН ЗАЯЦ КОРОВА ПИНГВИН ").split()

EAT_EN = ('BACON CHICKEN LIVER MEAT MUTTON CAULIFLOWER '
          'POULTRY SAUSAGE TENDERLOIN TURKEY VEAL VENISON '
          'HERRING MACKEREL PIKE PLAICE SALMON SARDINES SOLE STURGEON '
          'TROUT ASPARAGUS AVOCADO BEANS BROCCOLI CABBAGE CARROT '
          'CUCUMBER EGGPLANT GARLIC LENTILS ONION PEPPER POTATO '
          'SPINACH PUMPKIN TURNIP ZUCCHINI ALMOND APPLE APRICOT BANANA '
          'BLACKBERRY BLUEBERRY CHERRY CRANBERRY GRAPE GRAPEFRUIT HAZELNUT LEMON '
          'LIME MELON ORANGE PEACH PEANUT PEAR PECAN PINEAPPLE RASPBERRY '
          'STRAWBERRY TANGERINE WALNUT WATERMELON BUCKWHEAT RICE WHEAT BUTTER '
          'CHEESE CREAM KEFIR MILK YOGURT BISCUIT BUTTERSCOTCH CAKE '
          'CARAMEL CHOCOLATE CINNAMON CRACKER CROISSANT CUPCAKE PIZZA '
          'HONEY JELLY LOLLIPOP MARMALADE MARSHMALLOW MUFFIN NOUGAT '
          'PANCAKE POPCORN PRETZEL PUDDING SUGAR TOFFEE VANILLA  WAFFLE ').split()

EAT_RU = ("БЕКОН ГОВЯДИНА КУРИЦА УТКА БАРАНИНА ПЕЧЕНЬ МЯСО БАРАНИНА СВИНИНА ЦВЕТНАЯ_КАПУСТА "
          "ПТИЦА КОЛБАСА ВЫРЕЗКА ИНДЕЙКА ТЕЛЯТИНА ОЛЕНИНА ТРЕСКА УГОРЬ "
          "СКУМБРИЯ ЩУКА КАМБАЛА ЛОСОСЬ САРДИНЫ КАМБАЛА ОСЕТРИНА "
          "ФОРЕЛЬ АВОКАДО ФАСОЛЬ СВЕКЛА БРОККОЛИ КАПУСТА МОРКОВЬ "
          "ОГУРЕЦ БАКЛАЖАН ЧЕСНОК ЧЕЧЕВИЦА ПЕРЕЦ КАРТОФЕЛЬ ПИЦЦА "
          "ШПИНАТ ТЫКВА РЕПА КАБАЧКИ МИНДАЛЬ ЯБЛОКО АБРИКОС БАНАН "
          "ЕЖЕВИКА ЧЕРНИКА ВИШНЯ КЛЮКВА ВИНОГРАД ГРЕЙПФРУТ ФУНДУК ЛИМОН "
          "ЛАЙМ ДЫНЯ АПЕЛЬСИН ПЕРСИК АРАХИС ГРУША ПЕКАН АНАНАС СЛИВА МАЛИНА "
          "КЛУБНИКА МАНДАРИН ГРЕЦКИЙ_ОРЕХ АРБУЗ ГРЕЧКА ПШЕНИЦА МАСЛО "
          "СЛИВКИ ЯЙЦА КЕФИР МОЛОКО ЙОГУРТ ПЕЧЕНЬЕ ИРИСКА ТОРТ "
          "СЛАДКАЯ КАРАМЕЛЬ ШОКОЛАД КРЕКЕР КОРИЦА КРУАССАН КЕКС "
          "МЕДОВОЕ ЛЕДЕНЕЦ МАРМЕЛАД ЗЕФИР МАФФИН НУГА "
          "ПОПКОРН КРЕНДЕЛЬ ПУДИНГ САХАР ИРИСКА ВАНИЛЬ ВАФЛЯ ").split()

HOUSE_EN = ('FLAT HOUSE FRONT_DOOR STAIRCASE GARDEN GARAGE CHIMNEY AERIAL NURSERY BEDROOM BATHROOM KITCHEN '
            'LIVING_ROOM TOILET BATHROOM MIRROR TOWEL SHOWER LIVING_ROOM BOOKCASE CEILING FURNITURE CARPET CHAIR '
            'SOFA WALLPAPER FIREPLACE FLOOR_LAMP COFFEE_TABLE CURTAINS INDOOR_PLANTS BOOKSHELF OVEN FRIDGE '
            'FREEZER DISHWASHER CUTLERY_DRAWER BEDROOM PILLOW PILLOW_CASE BLANKET WARDROBE ALARM_CLOCK '
            'CHEST_OF_DRAWERS HAIR_DRYER ').split()

HOUSE_RU = ('КВАРТИРА ВХОДНАЯ_ДВЕРЬ ЛЕСТНИЦА КРЫША ГАРАЖ ДЫМОХОД АНТЕННА ПИТОМНИК СПАЛЬНЯ ВАННАЯ КУХНЯ ГОСТИНАЯ ТУАЛЕТ '
            'ВАННАЯ ЗЕРКАЛО ВАННА ПОЛОТЕНЦЕ ГОСТИНАЯ КНИЖНЫЙ_ШКАФ ПОТОЛОК МЕБЕЛЬ КОВЕР СТУЛ ДИВАН ОБОИ КАМИН ЛАМПА '
            'ТОРШЕР КОФЕЙНЫЙ_СТОЛИК ЗАНАВЕСЫ КОМНАТНЫЕ_ЦВЕТЫ КНИЖНАЯ_ПОЛКА РАКОВИНА ДУХОВКА ХОЛОДИЛЬНИК МОРОЗИЛКА '
            'ПОСУДОМОЙКА СПАЛЬНЯ КРОВАТЬ ПОДУШКА НАВОЛОЧКА ОДЕЯЛО ГАРДЕРОБ БУДИЛЬНИК КОМОД ').split()

CLOTHES_EN = ('SHIRT T-SHIRT POLO_SHIRT CUFF POCKET BLOUSE TUNIC TURTLENECK JACKET TUXEDO FLAK_JACKET LIFE_JACKET '
              'SKIRT MINISKIRT DRESS CARDIGAN SWEATER PULLOVER JUMPER SWEATSHIRT SUIT TRACKSUIT WAISTCOAT TROUSERS '
              'SUSPENDERS JEANS CHINOS SHORTS OVERALL LEGGINGS STOCKINGS TIGHTS SOCKS LONG_SOCKS OVERCOAT '
              'RAINCOAT BIKINI PANTS UNDERPANTS SHOES SLIPPERS BOOTS SNEAKERS MOCCASINS BALACLAVA '
              'BASEBALL_CAP BERET BOBBLE_HAT CRASH_HELMETT SOMBRERO COWBOY_HAT TOP_HAT GLOVES MITTENS SCARF '
              'SHAWL BOW-TIE BACKPACK BRACELET WATCHES ').split()

CLOTHES_RU = ('РУБАШКА ФУТБОЛКА МАНЖЕТЫ КАРМАН БЛУЗКА ТУНИКА ВОДОЛАЗКА КУРТКА СМОКИНГ БРОНЕЖИЛЕТ '
              'СПАСАТЕЛЬНЫЙ_ЖИЛЕТ ЮБКА МИНИ-ЮБКА '
              'ПЛАТЬЕ КАРДИГАН СВИТЕР ПУЛОВЕР ДЖЕМПЕР ТОЛСТОВКА КОСТЮМ СПОРТИВНЫЙ_КОСТЮМ ЖИЛЕТ БРЮКИ '
              'ПОДТЯЖКИ ДЖИНСЫ ЧИНОСЫ ШОРТЫ КОМБИНЕЗОН ЛЕГГИНСЫ ЧУЛКИ КОЛГОТКИ НОСКИ ПАЛЬТО '
              'ПАЛЬТО БИКИНИ ПЛАВКИ БРЮКИ ТРУСЫ ОБУВЬ ТАПОЧКИ САПОГИ КРОССОВКИ МОКАСИНЫ БАЛАКЛАВА '
              'КЕПКА БЕРЕТ ШАПКА_С_ПОМПОНОМ СОМБРЕРО КОВБОЙСКАЯ_ШЛЯПА ЦИЛИНДР ПЕРЧАТКИ ВАРЕЖКИ '
              'ГАЛСТУК-БАБОЧКА РЮКЗАК БРАСЛЕТ ЧАСЫ ').split()

SCHOOL_EN = ('CLASSROOM BLACKBOARD CHALK DESK CHAIR TABLE PENCIL NOTEBOOK TEXTBOOK DICTIONARY ERASER RUBBER '
             'RULER SCISSORS GLUE PIECE_OF_PAPER FOLDER PENCIL_SHARPENER BACKPACK TEACHER PUPIL HEAD_MASTER '
             'HEAD_TEACHER PHYSICS ALGEBRA HISTORY ASTRONOMY LITERATURE GEOMETRY PHYSICAL_EDUCATION PHILOSOPHY '
             'BIOLOGY ECOLOGY SOCIAL_SCIENCE FOREIGN_LANGUAGE ECONOMICS READING SINGING TECHNOLOGY '
             'STUDY_OF_CULTURE TECHNICAL_DRAWING INFORMATION_SCIENCE ').split()

SCHOOL_RU = ('КЛАСС ШКОЛЬНАЯ_ДОСКА РАБОЧИЙ_СТОЛ РУЧКА КАРАНДАШ БЛОКНОТ УЧЕБНИК КНИГА СЛОВАРЬ ЛАСТИК '
             'РЕЗИНКА ПРАВИТЕЛЬ НОЖНИЦЫ КЛЕЙ БУМАЖКА ЧАСЫ ПАПКА ТОЧИЛКА СУМКА РЮКЗАК УЧИТЕЛЬ УЧЕНИК ДИРЕКТОР_ШКОЛЫ '
             'ЗАВУЧ МАТЕМАТИКА ФИЗИКА АЛГЕБРА ИСТОРИЯ АСТРОНОМИЯ ЛИТЕРАТУРА ГЕОМЕТРИЯ ФИЗИЧЕСКАЯ_КУЛЬТУРА ФИЛОСОФИЯ '
             'БИОЛОГИЯ ЭКОЛОГИЯ ОБЩЕСТВОЗНАНИЕ ИНОСТРАННЫЙ_ЯЗЫК ЭКОНОМИКА ИСКУССТВО ЧТЕНИЕ ПЕНИЕ ТЕХНОЛОГИЯ '
             'КУЛЬТУРА ЧЕРТЕЖ ИНФОРМАТИКА ').split()

MUSIC_EN = ('VIOLIN CELLO ORGAN TRUMPET THE_DRUMS PIANO BAGPIPES TRIANGLE SAXOPHONE HARMONICA FLUTE GUITAR BANJO '
            'ACCORDION LYRICS DANCERS HEADSET DRUM_KIT STRING BATON CONCERT_HALL INSTRUMENTS ACOUSTIC_GUITAR '
            'COMPERE CLARINET ').split()

MUSIC_RU = ('СКРИПКА ВИОЛОНЧЕЛЬ АРФА ОРГАН ТРУБА БАРАБАН ПИАНИНО ВОЛЫНКА ТРЕУГОЛЬНИК САКСОФОН ГАРМОНИКА ФЛЕЙТА ГИТАРА '
            'БАНДЖО АККОРДЕОН ЛИРИКА ГРУППА НАУШНИКИ УДАРНАЯ_УСТАНОВКА СТРОКА ДУБИНКА КОНЦЕРТНЫЙ_ЗАЛ ИНСТРУМЕНТАРИЙ '
            'КОНФЕРАНСЬЕ КЛАРНЕТ ').split()

BODY_EN = ('BODY HEAD ELBOW SHOULDER FINGERS THUMB TOES FOOT KNEE ANKLE WAIST STOMACH FACE NOSE MOUTH EYES EARS HAIR '
           'CHEEKS TOOTH EYELASH FOREHEAD FRECKLE DIMPLE BRAIN HEART APPENDIX LARYNX THROAT TONGUE BLOOD MUSCLE '
           'BICEPS WRINKLE ').split()

BODY_RU = ('ТЕЛО ГОЛОВА ЛОКОТЬ ПЛЕЧО КИСТИ БОЛЬШОЙ_ПАЛЕЦ ЦЫПОЧКИ НОГА КОЛЕНО ЛОДЫЖКА ТАЛИЯ ЖЕЛУДОК ЛИЦО ГЛАЗА ШЕРСТЬ '
           'ЩЕКИ РЕСНИЦА ВЕСНУШКИ ЯМОЧКА СЕРДЦЕ ПРИЛОЖЕНИЕ ГОРТАНЬ ГОРЛО ЯЗЫК КРОВЬ МУСКУЛ МОРЩИНА ЗАТЫЛОК ПОДБОРОДОК '
           'НОЗДРЯ МОЧКА_УХА ЧЕЛЮСТЬ ЧЕРЕП ВОЛОСЫ ПОЧКА ПЕЧЕНЬ ЛЕГКОЕ ГОЛОСОВЫЕ_СВЯЗКИ АРТЕРИЯ СВЯЗКА МЫШЦА РЕБРО '
           'ПОЗВОНОЧНИК КЛЮЧИЦА ЛОПАТКА ').split()

SPORT_EN = ('DIVING ICE_SKATING SKIING SAILING MOTOR_RACING HORSE_RACING SHOT_PUT HOCKEY CYCLING HIGH_JUMP FOOTBALL '
            'BADMINTON BOXING BASKETBALL BASEBALL FENCING DISCUS_THROWING RUGBY TABLE_TENNIS WRESTLING VOLLEYBALL '
            'SWIMMING SPORT_EQUIPMENT SKATES HOCKEY_STICK TEAM TRAINING_SESSION PLAYER COACH CHAMPIONSHIP '
            'SCORE').split()

SPORT_RU = ('ДАЙВИНГ КАТАНИЕ_НА_ЛЫЖАХ ШАХМАТЫ ПАРУСНЫЙ_СПОРТ АВТОГОНКИ СКАЧКИ ТОЛКАНИЕ_ЯДРА ХОККЕЙ ВЕЛОСПОРТ '
            'ПРЫЖОК_В_ВЫСОТУ ФУТБОЛ БАДМИНТОН БАСКЕТБОЛ БЕЙСБОЛ ФЕХТОВАНИЕ МЕТАНИЕ_ДИСКА РЕГБИ НАСТОЛЬНЫЙ_ТЕННИС '
            'БОРЬБА ВОЛЕЙБОЛ ПЛАВАНИЕ ИНВЕНТАРЬ КОНЬКИ ШАЙБА ХОККЕЙНАЯ_КЛЮШКА ТРЕНАЖЕРНЫЙ_ЗАЛ КОМАНДА '
            'ТРЕНИРОВКА ИГРОК ТРЕНЕР ЧЕМПИОНАТ').split()

PC_EN = ('LAPTOP PERSONAL_COMPUTER KEYBOARD MONITOR HARD_DRIVE FLASH_CARD FLOPPY_DISK MOTHERBOARD VIDEO_CARD '
         'POWER_SUPPLY INTERNAL_MODEM POWER_STRIP SOFTWARE ROUTER SYSTEM_UNIT MEMORY DISPLAY SOUND_CARD '
         'COMPUTER_MOUSE MOUSE_MAT POWER_INDICATOR DATA_CABLE COPIER COMPUTER_DESK OPERATING_SYSTEM OVERLOAD QUERY '
         'SOURCE SPEAKERS HEADPHONES BACKUP_COPY WINDOW STORAGE PLAYER MESSAGE EMAIL_ACCOUNT').split()

PC_RU = ('НОУТБУК КЛАВИАТУРА МОНИТОР ЖЕСТКИЙ_ДИСК ФЛЭШ_КАРТА ДИСКЕТА МАТЕРИНСКАЯ_ПЛАТА '
         'ВИДЕОКАРТА ИСТОЧНИК_ПИТАНИЯ ВНУТРЕННИЙ_МОДЕМ УДЛИНИТЕЛЬ МАРШРУТИЗАТОР '
         'СИСТЕМНЫЙ_БЛОК ПАМЯТЬ ДИСПЛЕЙ ЗВУКОВАЯ_КАРТА КОМПЬЮТЕРНАЯ_МЫШЬ КОВРИК_ДЛЯ_МЫШИ ИНДИКАТОР_ПИТАНИЯ '
         'КАБЕЛЬ_ДАННЫХ ПРИНТЕР КОМПЬЮТЕРНЫЙ_СТОЛ ПЕРЕГРУЗКА ЗАПРОС ИСТОЧНИК '
         'ССЫЛКА НАУШНИКИ РЕЗЕРВНАЯ_КОПИЯ ОКНО ПОЛЬЗОВАТЕЛЬ ИГРОК СООБЩЕНИЕ '
         'ПОЧТОВЫЙ_ЯЩИК').split()

NATURE_EN = ('TREE BRANCH LEAVES FLOWER GRASS RIVER LAKE WATER_BASINS WATERFALL OCEAN SHORE COAST PEBBLE DESERT WAVES '
             'TIDES CLOUDS THUNDER THUNDERSTORM LIGHTNING MOON FIELD FOREST WOOD MOUNTAIN MEADOW BERRIES MUSHROOMS '
             'WEATHER CLIMATE SEASONS SUMMER WINTER SPRING AUTUMN HURRICANE TORNADO TYPHOON EARTHQUAKE VOLCANO '
             'VOLCANO_ERUPTION WAVE TSUNAMI DROUGHT').split()

NATURE_RU = ('ДЕРЕВО ВЕТКА ЛИСТВА ЦВЕТОК СТЕБЕЛЬ ТРАВА ЛУЖАЙКА РЕЧНОЙ ОЗЕРО ВОДОХРАНИЛИЩЕ ВОДОПАД ОКЕАН БЕРЕГ '
             'ПОБЕРЕЖЬЕ БУЛЫЖНИК ПЕСОК ПУСТЫНЯ ПРИЛИВЫ НЕБО ОБЛАКА ГРОЗА МОЛНИЯ ТУМАН ВЕТЕР СОЛНЦЕ ЛУНА ПОЛЕ ДЕРЕВО '
             'ГОРА ЯГОДЫ ГРИБЫ ПОГОДА КЛИМАТ СМЕНА_СЕЗОНОВ ЛЕТО ЗИМА ВЕСНА ОСЕНЬ УРАГАН ТОРНАДО ТАЙФУН ЗЕМЛЕТРЯСЕНИЕ '
             'ВУЛКАН ВОЛНА ЦУНАМИ НАВОДНЕНИЕ ЗАСУХА').split()

PROFESSIONS_EN = ('FIREMAN EDITOR DRIVER LAWYER HAIRDRESSER BARBER VET SURGEON MINER DUSTMAN BUTCHER INTERPRETER '
                  'CARPENTER POSTMAN TURNER WRITER MANAGER NURSE FLORIST JOINER ELECTRICIAN BRICKLAYER SCIENTIST '
                  'TEACHER SECRETARY WAITER WAITRESS PLUMBER LOCKSMITH MIDWIFE CHEF ARCHITECT BUSINESSMAN ACTOR '
                  'ACTRESS DOCTOR DESIGNER SAILOR MUSICIAN PILOT POLICEMAN').split()

PROFESSIONS_RU = ('ПОЖАРНЫЙ РЕДАКТОР ВОДИТЕЛЬ АДВОКАТ ПАРИКМАХЕР БАРБЕР ВЕТЕРИНАР ХИРУРГ ГОРНОРАБОЧИЙ МУСОРЩИК '
                  'МЯСНИК ПЕРЕВОДЧИК ПЛОТНИК ПОЧТАЛЬОН ТОКАРЬ ПИСАТЕЛЬ МЕНЕДЖЕР МЕДСЕСТРА ЦВЕТОВОД СТОЛЯР ЭЛЕКТРИК '
                  'КАМЕНЩИК УЧЕНЫЙ УЧИТЕЛЬ СЕКРЕТАРЬ ОФИЦИАНТ ОФИЦИАНТКА САНТЕХНИК СЛЕСАРЬ АКУШЕРКА ШЕФ_ПОВАР '
                  'АРХИТЕКТОР БИЗНЕСМЕН АКТЕР АКТРИСА ВРАЧ ДИЗАЙНЕР МОРЯК МУЗЫКАНТ ЛЕТЧИК ПОЛИЦЕЙСКИЙ').split()

FIRST_POSITION = ('🗄️➖➖➖➕\n'
                  '🗄️                |\n'
                  '🗄️\n'
                  '🗄️\n'
                  '🗄️\n'
                  '🗄️\n'
                  '🗄📐\n')

SECOND_POSITION = ('🗄️➖➖➖➕\n'
                   '🗄️                |\n'
                   '🗄️              😕\n'
                   '🗄️\n'
                   '🗄️\n'
                   '🗄️\n'
                   '🗄📐\n')

THIRD_POSITION = ('🗄️➖➖➖➕\n'
                  '🗄️                |\n'
                  '🗄️              ☹️\n'
                  '🗄️                |\n'
                  '🗄️\n'
                  '🗄️\n'
                  '🗄📐\n')

FOURTH_POSITION = ('🗄️➖➖➖➕\n'
                   '🗄️                |\n'
                   '🗄️              😦\n'
                   '🗄️              /|\n'
                   '🗄️\n'
                   '🗄️\n'
                   '🗄📐\n')

FIFTH_POSITION = ('🗄️➖➖➖➕\n'
                  '🗄️                |\n'
                  '🗄️              😫\n'
                  '🗄️              /|\\\n'
                  '🗄️\n'
                  '🗄️\n'
                  '🗄📐\n')

SIXTH_POSITION = ('🗄️➖➖➖➕\n'
                  '🗄️                |\n'
                  '🗄️              😭\n'
                  '🗄️              /|\\\n'
                  '🗄️              /\n'
                  '🗄️\n'
                  '🗄📐\n')


filename = 'categories.json'
words = {'ANIMALS': (ANIMALS_RU, ANIMALS_EN), 'EAT': (EAT_RU, EAT_EN), 'HOUSE': (HOUSE_RU, HOUSE_EN),
         'CLOTHES': (CLOTHES_RU, CLOTHES_EN), 'SCHOOL': (SCHOOL_RU, SCHOOL_EN), 'MUSIC': (MUSIC_RU, MUSIC_EN),
         'BODY': (BODY_RU, BODY_EN), 'SPORT': (SPORT_RU, SPORT_EN), 'PC': (PC_RU, PC_EN),
         'NATURE': (NATURE_RU, NATURE_EN), 'PROFESSIONS': (PROFESSIONS_RU, PROFESSIONS_EN),
         'FIRST_POSITION': FIRST_POSITION, 'SECOND_POSITION': SECOND_POSITION,
         'THIRD_POSITION': THIRD_POSITION, 'FOURTH_POSITION': FOURTH_POSITION,
         'FIFTH_POSITION': FIFTH_POSITION, 'SIXTH_POSITION': SIXTH_POSITION}

with open(filename, 'w', encoding="utf-8") as write:
    json.dump(words, write, indent=2, ensure_ascii=False)

with open(filename, "r", encoding="utf8") as read:
    print(json.load(read))
