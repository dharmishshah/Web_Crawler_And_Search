Prerequistes for project
1) Python
2) Pycharm or any other python IDE
3) Java
4) IntelliJ, Eclipse or any other java IDE

Libraries
# library used to process n gram terms
pip install nltk

# library used for pulling data out of HTML files
pip install bs4

# library used to locate positions of each terms and return list of positions.
pip install more_itertools

# library to plot graph for precision-recall
pip install matplotlib

Lucene
--> Create new Java project in IntelliJ ( or any other IDE)
--> Use the code from respective submitted file.
--> Import JAR files from lucene in your project
	--> lucene-core-VERSION.jar
	--> lucene-queryparser-VERSION.jar
	--> lucene-analyzers-common-VERSION.jar.
--> Run the LuceneApplication program as java application


Search Engine
Running the code - (Python 3.7)
--> Create a new Project in Pycharm (Or any other IDE)
--> Use the codes from respective submitted files.
--> Before running search.py, you can change the files and directory names appropiately.
--> Run the Search_engine.py


Extra Credit (Advance Search)
Running the code - (Python 3.7)
--> Create a new Project in Pycharm (Or any other IDE)
--> in the folder called "extraCredit" copy the folder QueryRelevence which contains "query.py" in the src folder.
--> in the invertedIndex place the invertedindex file (or in the code point it the the proper file)
--> place the stop word list in the stopWords folder (or in the code point it the the proper file)
--> in the query folder place pre defined query or you can enter your own query in the console.
--> Run the query.py.



Output Files


Corpuses - 
1) Clean corpus on raw 3204 documents
2) Clean corpus with stopping on raw 3204 documents
3) Clean corpus with stemming on raw 3204 documents

Indexes - 
1) Inverted and position inverted index for clean corpus with no stemming and no stopping raw 3204 documents
2) Inverted and position inverted index for clean corpus with stopping on raw 3204 documents
3) Inverted and position inverted index for clean corpus with stemming on raw 3204 documents

Results - 
1) 64 files are generated for each query search for Lucene giving top 100 documents
2) 64 files each are generated for each query search for BM25, tf.idf and JM Smoothing giving top 100 documents with no stemming and no stopping.
3) 64 files each are generated for each query search for BM25, tf.idf and JM Smoothing giving top 100 documents with stopping
4) 8 files each are generated for each query search for BM25, tf.idf and JM Smoothing giving top 100 documents with stemming
5) Snippets for each ranked output file is generated.
6) 64 files are generated for each query for BM25 after applying Pseudo Relevance feedback

Evaluation-
1) 64 files are generated for each query search for Lucene giving precision and recall
2) 64 files each are generated for each query search for BM25, tf.idf and JM Smoothing giving precision and recall with no stemming and no stopping.
3) 64 files each are generated for each query search for BM25, tf.idf and JM Smoothing giving precision and recall with stopping
4) 8 files each are generated for each query search for BM25, tf.idf and JM Smoothing giving precision and recall with stemming
5) 64 files are generated for each query for BM25 giving precision and recall after applying Pseudo Relevance feedback
6) It also generates MAP, MRR, P@5 and P@20
7) It also plots precision-recall curve(one curve per run.All runs are in one figure)

ExtraCredit-
we ran three pre defined queries for each for the advance search i.e "Exact Match", "Best Match" and "Ordered Best Proximity Match"
1) 3 file are generated in the output inside the "output/ExactMatch" folder which contains the ranking of the collection.
2) 3 file are generated in the output inside the "output/BestMatch" folder which contains the ranking of the collection.
3) 3 file are generated in the output inside the "output/ProximityMatch" folder which contains the ranking of the collection.


References - 

https://docs.python.org/3/
http://lucene.apache.org/core/documentation.html
http://lucene.apache.org/core/
https://lucene.apache.org/
http://lucene.apache.org/core/7_5_0/index.html
https://nlp.stanford.edu/IR-book/html/htmledition/results-snippets-1.html
https://link.springer.com/chapter/10.1007/978-3-642-45068-6_5