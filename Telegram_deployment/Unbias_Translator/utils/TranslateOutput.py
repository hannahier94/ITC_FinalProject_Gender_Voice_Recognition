from googletrans import Translator
import re

def get_translation(output, gender):
    heb_I =  'אני'
    heb_she = 'היא'
    heb_he = 'הוא'
    ind = []
    translate = ''
    lenght = 0
    translator = Translator()
    replacer = 'I'


    for sentence, val in output:
        res = translator.translate(sentence, dest='he').text
        res_list = re.findall(r"[\w]+|['.,!?;]", res)
        if val>0:
            if gender == 'female':
                replacer = 'she'
                heb_replacer = heb_she
            elif gender == 'male':
                replacer = 'he'
                heb_replacer = heb_he
            index = [i for i,x in enumerate(res_list) if x==heb_I][0]
            ind.append(index+lenght)
        lenght += len(res_list)
        sentence_list = re.findall(r"[\w]+|['.,!?;]", sentence)
        sentence = ' '.join([replacer if word == 'I' else word for word in sentence_list])
        translate += " " + sentence
    gender_res = translator.translate(translate, dest='he').text
    gender_res_list = re.findall(r"[\w]+|['.,!?;]", gender_res)
    for i in ind:
        if gender_res_list[i] == heb_replacer:
            gender_res_list[i] = heb_I
        elif gender_res_list[i-1] ==  heb_replacer:
            gender_res_list[i-1] = heb_I
        elif gender_res_list[i+1] ==  heb_replacer:
            gender_res_list[i+1] = heb_I

    return ' '.join(gender_res_list)

