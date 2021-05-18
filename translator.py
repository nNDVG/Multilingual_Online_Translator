import argparse, requests
from bs4 import BeautifulSoup

languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
             'portuguese', 'romanian', 'russian', 'turkish']

parser = argparse.ArgumentParser()

parser.add_argument("my_lang", type=str)
parser.add_argument("to_lang", type=str)
parser.add_argument("word", type=str)

args = parser.parse_args()
my_lang = args.my_lang
to_lang = args.to_lang
word = args.word


def one_language(my_lang, to_lang, word):
    session = requests.Session()
    url = f'https://context.reverso.net/translation/{my_lang}-{to_lang}/{word}'
    user_agent = 'Mozilla/5.0'
    r = session.get(url, headers={'User-Agent': user_agent})
    page = BeautifulSoup(r.content, 'html.parser')
    trans_tags = page.find_all('a', {'class': 'translation'})
    example_tags = page.find_all('div', {'class': ['src', 'trg']})
    trans_words = find_text(trans_tags)
    trans_exam = find_text(example_tags)
    return show_result(word, to_lang, trans_words, trans_exam)


def all_language(my_lang, word):
    session = requests.Session()
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        for i in languages:
            if i != my_lang:
                url = f'https://context.reverso.net/translation/{my_lang}-{i}/{word} '
                user_agent = 'Mozilla/5.0'
                r = session.get(url, headers={'User-Agent': user_agent})
                page = BeautifulSoup(r.content, 'html.parser')
                trans_tags = page.find_all('a', {'class': 'translation'})
                example_tags = page.find_all('div', {'class': ['src', 'trg']})
                trans_words = find_text(trans_tags)[1]
                trans_exam = find_text(example_tags)[:2]
                print(f'\n{i.capitalize()} Translations:\n'
                      f'{trans_words}\n'
                      f'\n{i.capitalize()} Example:\n'
                      f'{trans_exam[0]}:\n'
                      f'{trans_exam[1]}\n'
                      )
                f.write(f'{i.capitalize()} Translations:\n'
                        f'{trans_words}\n'
                        f'\n{i.capitalize()} Example:\n'
                        f'{trans_exam[0]}:\n'
                        f'{trans_exam[1]}\n\n'
                        f'\n'
                        )
            else:
                continue


def show_result(word, to_lang, trans_words, trans_exam):
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        print(f'\n{to_lang} Translations:')
        for i in trans_words[1:6]:
            print(i)
        print(f'\n{to_lang} Examples:')
        print("\n\n".join(("\n".join(j for j in trans_exam[i:i + 2]) for i in range(0, 10, 2))))
        f.write(f'{to_lang} Translations:\n')
        for i in trans_words[1:6]:
            f.write(f'{i}\n')
        f.write(f'\n{to_lang} Examples:\n')
        f.write("\n\n".join(("\n".join(j for j in trans_exam[i:i + 2]) for i in range(0, 10, 2))))


def find_text(suop):
    result = []
    for i in suop:
        if i.text.strip() != '':
            result.append(i.text.strip())
    return result


if __name__ == '__main__':
    if my_lang not in languages:
        print(f"Sorry, the program doesn't support {my_lang}")
        exit()
    if to_lang not in ('all', *languages):
        print(f"Sorry, the program doesn't support {to_lang}")
        exit()
    if to_lang == 'all':
        try:
            all_language(my_lang, word)
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
        except IndexError:
            print(f'Sorry, unable to find {word}')
    else:
        try:
            one_language(my_lang, to_lang, word)
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
        except IndexError:
            print(f'Sorry, unable to find {word}')
