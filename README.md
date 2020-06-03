# PyThesisAnnouncement

An easy to configure python script which creates a DIN A4 thesis announcement using LaTeX.
Look inside the ```tex/``` folder to see the finished announcement.

## Getting Started
To create an announcement just edit the ```conf``` file, add your logos to the ```logos/``` folder and add images for the header to the ```images/``` folder.
Then just run
```
python3 createAnnouncement.py
```
If you do not have installed ```pdflatex``` on your system, the program will only generate the .tex file inside the ```tex/``` folder. If ```pdflatex``` is installed, it will also create the PDF file.

*(Note: All images must be ```.png``` or ```.jpeg``` files.)*

If you just want to see what the program will do, then just run ```python3 createAnnouncement.py```. Example images and text already exist.
