from bs4 import BeautifulSoup
import requests

def get_kanji(kanjiList):
    
    link = f"https://jisho.org/search/{kanjiList}%23kanji"
    page_html = requests.get(link).text

    pagesoup = BeautifulSoup(page_html, 'html.parser')
    searchedKanjis = pagesoup.find_all('h1', class_='character')
    
    for i, searchedKanji in enumerate(searchedKanjis):
        searchedKanjis[i] = str(searchedKanji.next_element)

    print(searchedKanjis)

    main_soups = pagesoup.find_all('div', class_='small-12 large-7 columns kanji-details__main')

    kanjiDatas = {}
    for kanji in kanjiList:
        if kanji in searchedKanjis:
            kanjiDatas[kanji] = KanjiData(list(), list(), list())

    for kanji, subsoup in zip(searchedKanjis, main_soups):
        kanjiDatas[kanji].kunyomi = subsoup.find('dl', class_='dictionary_entry kun_yomi')
        kanjiDatas[kanji].onyomi = subsoup.find('dl', class_='dictionary_entry on_yomi')
        kanjiDatas[kanji].translations = subsoup.find('div', class_='kanji-details__main-meanings')

    for kanjiData in kanjiDatas.values():

        kanjiData.kunyomi = kanjiData.kunyomi.find_all('a')
        kanjiData.onyomi = kanjiData.onyomi.find_all('a')

        for i, aLevelSoup in enumerate(kanjiData.kunyomi):
            kanjiData.kunyomi[i] = aLevelSoup.next_element
        for i, aLevelSoup in enumerate(kanjiData.onyomi):
            kanjiData.onyomi[i] = aLevelSoup.next_element

        kanjiData.translations = str(kanjiData.translations.next_element).strip().split(', ')

        kanjiData.kunyomi = [str(kun) for kun in kanjiData.kunyomi]
        kanjiData.onyomi = [str(on) for on in kanjiData.onyomi]

    for kanji, kanjiData in kanjiDatas.items():
        print(kanji + 'kunyomi: ' + str(kanjiData.kunyomi))
        print(kanji + 'onyomi: ' + str(kanjiData.onyomi))
        print(kanji + 'translations: ' + str(kanjiData.translations))
    
    return kanjiDatas

class KanjiData:
    def __init__(self, kunyomi, onyomi, translations):
        self.kunyomi = kunyomi
        self.onyomi = onyomi
        self.translations = translations


input = input("Enter kanji: ")
get_kanji(input)