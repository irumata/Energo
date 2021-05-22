import pymorphy2
import re
import dateutil
from dateutil.parser import parse
import csv

# "Атмосферные перенапряжения (гроза)": 0,
# "Воздействие животных и птиц": 1,
# "Ветровые нагрузки": 2,
# "Прочие воздействия неблагоприятных природных явлений ": 3,
# "Термическое повреждение, перегрев, пережог": 4,
# "Гололедно-изморозевые отложения": 5,
# "Пожары": 4,
# "Природные пожары": 4,
# "Падение деревьев (природные)": 2,
# "Взрыв, загорание, пожар": 4,
# "Погодные явления": 3,
# "Разрушение фундамента, строительных конструкций, ослабление крепления оборудования к фундаменту": 6,
# "Гололёдообразование": 5,
# "Паводок": 7,
# "Воздействие повторяющихся стихийных явлений": 3,

RU_MONTH_VALUES = {
        'январь': 1,
        'февраль': 2,
        'март': 3,
        'апрель': 4,
        'май': 5,
        'июнь': 6,
        'июль': 7,
        'август': 8,
        'сентябрь': 9,
        'октябрь': 10,
        'ноябрь': 11,
        'декабрь': 12,
    }

EN_MONTH_VALUES = {
        'январь': "january",
        'февраль': "february",
        'март': "march",
        'апрель': "april",
        'май': "may",
        'июнь': "june",
        'июль': "july",
        'август': "august",
        'сентябрь': "september",
        'октябрь': "october",
        'ноябрь': "november",
        'декабрь': "december",
    }

class TextProcessor():
    def __init__(self, phrase):
        self.phrase = phrase
        morph = pymorphy2.MorphAnalyzer()

        text_full = re.sub(r"[A-Za-z0-9(),.!?\'`\"«»|\-№:;/—\t*]", " ", phrase)
        text_full = re.sub(r"\s{2,}", " ", text_full).strip()

        words = text_full.split()

        text_full = list()
        for word in words:
            p = morph.parse(word)[0]
            text_full.append(p.normal_form)
        self.lemmatized_text = " ".join(text_full)

        text_full = re.sub(r"\s{2,}", " ", phrase[:12]).strip()
        words = text_full.split()
        text_full = list()
        for word in words:
            p = morph.parse(word)[0]
            text_full.append(p.normal_form)
        self.date_text = " ".join(text_full)
        #print(text_full)

    def get_feature_vectors(self):
        #features:
        # снег, дождь, осадки, подъем вода, ветер, град, повалить, ураган, шквалистый, землетрясение
        # неблагоприятный погодный условие
        # мокрый снег
        # птицы птица животные животный
        # пожар пожары огонь

        features = {
            "storm" : 0,
            "birds" : 0,
            "snow" : 0,
            "fire" : 0,
            "rain" : 0,
            "wind" : 0,
            "earthquake" : 0,
            "other_weather" : 0,
            "hail" : 0,
            "flood" : 0
        }
        #any(x in self.lemmatized_text for x in ["гроза", "ураган", "молния", "молния"]):
        if any(x in self.lemmatized_text for x in ["гроза", "ураган", "молния", "молния"]):
            features["storm"] = 1
        if any(x in self.lemmatized_text for x in ["птицы", "птица", "животные"]):
            features["birds"] = 1
        if any(x in self.lemmatized_text for x in ["снег", "метель", "сильный снег"]):
            features["snow"] = 1
        if any(x in self.lemmatized_text for x in ["пожар", "огонь", "пожары", "вспышка", "воспламенение", "горит", "гореть"]):
            features["fire"] = 1
        if any(x in self.lemmatized_text for x in ["дождь", "мокрый"]):
            features["rain"] = 1
        if any(x in self.lemmatized_text for x in ["ветер", "сильный ветер", "повалить", "усиление ветер"]):
            features["wind"] = 1
        if any(x in self.lemmatized_text for x in ["землетрясение"]):
            features["earthquake"] = 1
        if any(x in self.lemmatized_text for x in ["погодный условие"]):
            features["other_weather"] = 1
        if any(x in self.lemmatized_text for x in ["град"]):
            features["hail"] = 1
        if any(x in self.lemmatized_text for x in ["подъем вода", "вода", "уровень вода"]):
            features["flood"] = 1
        return features

    #def get_date(self):

    #    pass

    def get_date(self, fuzzy=True):
        try:
            date_str = self.int_value_from_ru_month(self.date_text)
            dt = parse(date_str, fuzzy=fuzzy, dayfirst=True)
            retstr = dt.strftime('%d.%m.%Y')
            return True, retstr
        except ValueError as e:
            print(e)
            return False, None
        except dateutil.parser._parser.ParserError:
            return False, None
        except OverflowError:
            return False, None

    def int_value_from_ru_month(self, date_str):
        for k, v in EN_MONTH_VALUES.items():
            date_str = date_str.replace(k, str(v))

        return date_str

if __name__ == "__main__":
    csv_1 = "Аварии_погода_САЦ.xlsx - Авари_погода.csv"
    reasons = []
    with open(csv_1) as csvfile:
        csv_1_reader = csv.reader(csvfile)
        for row in csv_1_reader:
            #print(row[4])
            reasons.append(row[4])
            #features.append(row[2])

    for reason in reasons:
        tp = TextProcessor(reason)
        print(tp.get_feature_vectors())
        print(tp.get_date())