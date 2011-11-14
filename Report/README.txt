This template makes use of four LaTeX files

- master.tex is the root file for the project. This file contains the
  list of project files to include in the document. The variables for setting up
  cover- and info-pages are also defined here. 

- thesislayout.sty contains the graphical setup. Cover- and
  info pages are constructed here based on the information defined in
  master.tex. The style of the headings, the chapter title pages and
  theorem-like environments are likewise defined here.

- thesisdef.sty is intended for inclusion of various packages
  and user defined commands. The idea is that whereas
  thesislayout.sty is rather specific for the layout of the thesis,
  thesisdef.sty contains the packages and options 

_ The Mythesis.sty is for corrections as you prefer and is, hence, project independent.

Several variables are defined in master.tex to automate the generation of cover-
and info pages. Most variables are self-explanatory but some do require more
explanation. Below are some tables where variable and its possible values are
listed.

\projecttype
|----------------------------------------------------------------------------------|
|Project type                                         |     Text                   |
|----------------------------------------------------------------------------------|
|Afsluttende ph.d. rapport (UK)                      | PhD Thesis                  |
|Civilingeniør eksamensprojekt - gammel ordning (DK) | Eksamensprojekt             |
|Civilingeniør eksamensprojekt - gammel ordning (UK) | Master's Thesis             |
|Bachelorprojekt/Diplomprojekt (DK)                  | Bachelorprojekt             |
|Bachelorprojekt/Diplomprojekt (UK)                  | Bachelor's Thesis           |
|Polyteknisk Midtvejsprojekt                         | Polyteknisk Midtvejsprojekt |
|Afsluttende rapport fra specialkursus               | Specialprojekt              |
|Afsluttende rapport fra virksomhedsprojekt          | Virksomhedsprojekt          |
|----------------------------------------------------------------------------------|

\Klasse
|-------------------------------------------------------------------------------------|
|            CLASS                                     |     Text                     |
|-------------------------------------------------------------------------------------|
|1. The report is accessible for public and may be     | 1 (Public)                   |
|   distributed on DTU's homepage.                     |                              |
|-------------------------------------------------------------------------------------|
|2. The report is confidential and may not be          |                              |
|   distributed.                                       | 2 (confidential)             |
|-------------------------------------------------------------------------------------|
|3. The report may only be distributed after written   |                              |
|   permission from the Author                         | 3 (after written permission) |
|-------------------------------------------------------------------------------------|

\Degree
|---------------------------------------------------------------------------------------|
|           Grad/titel                  |                            Tekst              |
|---------------------------------------------------------------------------------------|
|Diplomingeniør (DK)                    |   titlen Diplomingeniør                       |
|Diplomingeniør (UK)                    |   Bachelor of Engineering                     |
|Bachelor (DK)                          |   graden Bachelor i teknisk videnskab (BScE)  |
|Bachelor (UK)                          |   Bachelor of Science in Engineering (BSc)    |
|Civilingeniør (DK)                     |   graden Civilingeniør                        |
|Civilingeniør (UK)                     |   Master of Science in Engineering (MSc)      |
|Ph.d. (UK)                             |   PhD in Electrical Engineering               |
|---------------------------------------------------------------------------------------|
