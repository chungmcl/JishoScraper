import os
import io
import KanjiScraper
from cairosvg import svg2png
from PIL import Image

def FormatAndSaveStrokeOrderDiagram(strokeOrderDiagramSVG, saveTo):
    with io.BytesIO() as png:
        svg2png(bytestring=strokeOrderDiagramSVG, write_to=png)
        png.seek(0)
        file = open(saveTo, 'wb')
        file.write(png.read())
        file.close()

saveLocation = input("Enter folder to save data to: ")
kanjis = input("Enter kanji to search for: ")
kanjis = KanjiScraper.get_kanji(kanjis)
for kanji, kanjiData in kanjis.items():
    FormatAndSaveStrokeOrderDiagram(kanjiData.strokeOrderDiagram, saveLocation + f'/{kanji}.png')



        