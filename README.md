Интернет-радиоплеер с интерфейсом на основе библиотеки Textual.  
Чтобы отредактировать список радиостанций, измените STATIONLIST в тексте скрипта.  
К сожалению, не все типы аудиопотоков работают. Принимаются потоки в формате mp3.  
Списки воспроизведения pls/m3u/etc не поддерживаются.  


![screenshot](screenshot.png)


ЗАПУСК:  
запустите «pip install -r requriements.txt» (miniaudio, textual)  
запустите «python main.py»  

рекомендуется Windows Terminal, но с cmd более-менее все в порядке.  
работа проверена под Windows для Python 3.11  
!к сожалению, для установки miniaudio на Windows Python 3.12 потребуется Microsoft C++ Build Tools **(6 GB)** в связи с отсутствием wheels/бинарников miniaudio.  

TODO - работа кнопок «Next» и «Previous», а также управление мышью  

TODO — гистограмма аудиопотока.  
кажется, у miniaudio нет такой опции? или что-то вроде DecodedSoundFile?  
может от системной громкости/микшера?..  
может быть, sparklines?  

TODO - на месте планируемой гистограммы, сделать индикатор прогресса "нажатие/событие", чтобы замаскировать ~1-2 секундную задержку загрузки аудиопотока.  

*************************  

Internet radio player with Textual interface.  
To edit the radiostation list, modify STATIONLIST in the script.  
Not all stream types are working, unfortunately. mp3 streams accepted..  
pls/m3u/etc playlists not supported.  

HOW TO RUN:  
run "pip install -r requriements.txt" (miniaudio, textual)  
run "python main.py"  

recommended Windows Terminal, but cmd is more or less ok.  
tested on Windows Python 3.11  
!unfortunately, for Python 3.12, Microsoft C++ Build Tools **(6 GB)** seems to be required to install miniaudio due to lack of wheels/binaries.  

TODO - make working next and previous buttons, mouse clicks  

TODO - histogram for the audio stream. Don't know how to start.  
seems miniaudio has no such option? or something like  DecodedSoundFile?  
maybe from the system volume/mixer?..
for display, maybe sparkines?  

TODO - while no histogram, make 'press/event' indicator there.  
