from bs4 import BeautifulSoup
import requests

def get_kanji(kanjiList):
    
    link = f"https://jisho.org/search/{kanjiList}%23kanji"
    page_html = requests.get(link).text

    pagesoup = BeautifulSoup(page_html, 'html.parser')
    searchedKanjis = pagesoup.find_all('h1', class_='character')
    
    # Obtain all kanjis that were successfully searched and returned from jisho.org
    for i, searchedKanji in enumerate(searchedKanjis):
        searchedKanjis[i] = str(searchedKanji.next_element)

    # Obtain main sections of the page 
    mainInfoSoups = pagesoup.find_all('div', class_='small-12 large-7 columns kanji-details__main')
    readingCompoundSoups = pagesoup.find_all('div', class_='row compounds')
    strokeOrderDiagrams = pagesoup.find_all('div', class_='stroke_order_diagram--outer_container')
    for i, strokeOrderDiagram in enumerate(strokeOrderDiagrams):
        strokeOrderDiagrams[i] = strokeOrderDiagram.find('svg')

    # Declare kanjiDatas dictionary and intialize kanjiData for each kanji
    kanjiDatas = {}
    for kanji in kanjiList:
        if kanji in searchedKanjis:
            kanjiDatas[kanji] = KanjiData(list(), list(), list(), list(), list(), None)

    # Unpack subsoups of kanji data categories into respective kanjis' fields
    for kanji, mainInfoSoup, readingCompoundSoup, strokeOrderDiagram in zip(searchedKanjis, mainInfoSoups, readingCompoundSoups, strokeOrderDiagrams):
        kanjiDatas[kanji].kunyomi = mainInfoSoup.find('dl', class_='dictionary_entry kun_yomi')
        kanjiDatas[kanji].onyomi = mainInfoSoup.find('dl', class_='dictionary_entry on_yomi')
        kanjiDatas[kanji].translations = mainInfoSoup.find('div', class_='kanji-details__main-meanings')
        kanjiDatas[kanji].strokeOrderDiagrams = strokeOrderDiagram
        #file = open(f"/Users/chungmcl/Desktop/svgs/{kanji}.svg", "wt")
        #file.write(str(strokeOrderDiagram))
        #file.close()

        readingCompoundLists = readingCompoundSoup.find_all('ul', class_="no-bullet")
        for readingCompoundList in readingCompoundLists:
            if readingCompoundList.previous_sibling.previous_sibling.string == "Kun reading compounds":
                kanjiDatas[kanji].kunReadingCompounds = readingCompoundList
            else:
                kanjiDatas[kanji].onReadingCompounds = readingCompoundList

    # Reformat subsoups per kanjiData field into string data
    for kanjiData in kanjiDatas.values():
        # Some kanji DO NOT have kunyomi -- Check if it has kunyomi
        if kanjiData.kunyomi != None:
            kanjiData.kunyomi = kanjiData.kunyomi.find_all('a')
            for i, aLevelSoup in enumerate(kanjiData.kunyomi):
                kanjiData.kunyomi[i] = aLevelSoup.next_element
            kanjiData.kunyomi = [str(kun) for kun in kanjiData.kunyomi]
            kunReadingCompoundList = kanjiData.kunReadingCompounds.find_all('li')
            kanjiData.kunReadingCompounds = [str(kunReadingCompound.next_element) for kunReadingCompound in kunReadingCompoundList]
        
        # Some kanji DO NOT have onyomi -- Check if it has onyomi
        if kanjiData.onyomi != None:
            kanjiData.onyomi = kanjiData.onyomi.find_all('a')
            for i, aLevelSoup in enumerate(kanjiData.onyomi):
                kanjiData.onyomi[i] = aLevelSoup.next_element
            kanjiData.onyomi = [str(on) for on in kanjiData.onyomi]
            onReadingCompoundList = kanjiData.onReadingCompounds.find_all('li')
            kanjiData.onReadingCompounds = [str(onReadingCompound.next_element) for onReadingCompound in onReadingCompoundList]

        kanjiData.translations = str(kanjiData.translations.next_element).strip().split(', ')

    # Print out collected data
    for kanji, kanjiData in kanjiDatas.items():
        print(kanji + ' kunyomi: ' + str(kanjiData.kunyomi))
        print(kanji + ' onyomi: ' + str(kanjiData.onyomi))
        print(kanji + ' translations: ' + str(kanjiData.translations))
        print(kanji + ' kun reading compounds: ')
        for kunReadingCompound in kanjiData.kunReadingCompounds:
            print(kunReadingCompound)
        print(' ')
        
        print(kanji + ' on reading compounds: ')
        for onReadingCompound in kanjiData.onReadingCompounds:
            print(onReadingCompound)
        print(' ')
    
    return kanjiDatas

class KanjiData:
    def __init__(self, kunyomi, onyomi, translations, kunReadingCompounds, onReadingCompounds, strokeOrderDiagram):
        self.kunyomi = kunyomi
        self.onyomi = onyomi
        self.translations = translations
        self.kunReadingCompounds = kunReadingCompounds
        self.onReadingCompounds = onReadingCompounds
        self.strokeOrderDiagram = strokeOrderDiagram


input = input("Enter kanji: ")
get_kanji(input)