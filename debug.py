import KanjiScraper

input = input("Input sentence: ")

output = KanjiScraper.get_kanji(input)

for kanji, kanjiData in output.items():		
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
         file = open(f"/Users/chungmcl/Desktop/svgs/{kanji}.svg", "wt")		
         file.write(kanjiData.strokeOrderDiagram)		
         file.close()		
         print(' ')
         