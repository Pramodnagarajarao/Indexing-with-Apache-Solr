How to import and run the Lucene source from Eclipse:

This has been tested on 

Eclipse Standard/SDK
Version: Kepler Service Release 1
Build id: 20130919-0819

and

NetBeans IDE 7.3.1 

and 

lucene-3.6.2

on Macbook Pro

by Team 33 CSCI 572, Nov 11th, 2015

----------------- Instructions for Eclipse

0. Install Eclipse
1. Download lucene-3.6.2-src.tgz and uncompress it to a folder lucene-3.6.2-src
2. Open Eclipse. Create a project (File -> New -> Javaproject). 
   Give a project name (e.g.ContentBasedAnalysis), Next, Finish
3. Import the lucene core source code: 
   - In the package explorer on the left, open e.g.ContentBasedAnalysis folder
   - rightclick on src, then Import then General, then File System
   - "From directory": browse to the lucene-3.6.2-src -> lucene-3.6.2 -> core -> src.
     Select the java folder for import
   - in the next form, tick on the java folder (or "select all"), then Finish.
     You should see a lot of org.apache.lucene.* packages imported. 
4. Import the lucene demo source code:
   - Same with the folder lucene-3.6.2-src -> lucene-3.6.2 -> contrib -> demo -> src
   (say whatever to an "overwrite" warning)
5. Run the e.g.ContentBasedAnalysis.java program: 
   - look for e.g.ContentBasedAnalysis.java under org.apache.lucene.demo
   - (optional) click on it to check that it opens in the editor.
     if the syntax-checker flags the "package org.apache.lucene.demo" line, 
     you did something wrong with the import, the packages are not in the right place. 
   - right click on e.g.ContentBasedAnalysis.java. Run As Java Application.
   Hopefully it will run, and the console window will show
   "Usage: Hello”. This is ContentBasedAnalysis Running!
6. Go to the "Run -> Run Configurations" option in the main menu, 
   look for the ContentBasedAnalysis Configuration, then the Arguments tab, and enter 
   the command line you want to give contentbasedanalysis, something like:
   -docs directorydirectory\novels -index mynovelsindex
   Now run again, and it should index. 
7. You can edit now ContentBasedAnalysis.java (and/or other) files and run again

