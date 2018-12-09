import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class LuceneApplication {
  private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
  private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

  private IndexWriter writer;
  private ArrayList<File> queue = new ArrayList<File>();

  public static void main(String[] args) throws IOException {
    System.out.println("Enter the FULL path where the index will be created: " +
            "(e.g. /Usr/index or c:\\temp\\index)");

    String dir = new File("../").getCanonicalPath();
    String indexPath = dir + "/indexes/";

    String indexLocation = null;
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String s = indexPath;

    LuceneApplication indexer = null;
    try {
      indexLocation = s;
      indexer = new LuceneApplication(s);
    } catch (Exception ex) {
      System.out.println("Cannot create index..." + ex.getMessage());
      System.exit(-1);
    }

    // ===================================================
    // read input from user until he enters q for quit
    // ===================================================
    while (!s.equalsIgnoreCase("N")) {
      try {

        System.out
                .println("Do you want to create a new index?Press Y if yes and N if no");
        s = br.readLine();
        if(s.equalsIgnoreCase("Y")){
          dir = new File("../").getCanonicalPath();
          indexPath = dir + "/test_collection/corpus/";
          s = indexPath;
        }


        if (s.equalsIgnoreCase("N")) {
          break;
        }

        // try to add file into the index
        indexer.indexFileOrDirectory(s);
      } catch (Exception e) {
        System.out.println("Error indexing " + s + " : "
                + e.getMessage());
      }
    }

    // ===================================================
    // after adding, we always have to call the
    // closeIndex, otherwise the index is not created
    // ===================================================
    indexer.closeIndex();

    // =========================================================
    // Now search
    // =========================================================
    IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
            indexLocation)));
    IndexSearcher searcher = new IndexSearcher(reader);



    s = "";
    List<String> input = new ArrayList<String>();
    dir = new File("../").getCanonicalPath();
    File queryFile = new File(dir + "/test_collection/cacm.query.txt");

    FileReader fileReader = new FileReader(queryFile);
    // Always wrap FileReader in BufferedReader.
    BufferedReader bufferedReader = new BufferedReader(fileReader);
    String line;
    if (queryFile.exists()) {
      File currentDir = new File(dir + "/results/lucene/");
      if(!currentDir.exists()){
        currentDir.mkdir();
      }
      Pattern pt = Pattern.compile("[^a-zA-Z0-9]");

      while ((line = bufferedReader.readLine()) != null) {

        if(line.length() > 0 && line.equalsIgnoreCase("<DOC>")){
          String docno = line;
          String newLine;
          while(!(newLine = bufferedReader.readLine()).equalsIgnoreCase("</DOC>")){
            if(newLine.length() > 0){
              docno = docno + newLine;
            }
          }
          String[] output = docno.split("</DOCNO>");
          String query = output[1];

          Matcher match= pt.matcher(query);
          query=query.replaceAll("[^a-zA-Z0-9 ]", " ");
          while(match.find())
          {
            String temp= match.group();

          }
          System.out.println(query);
          input.add(query);
        }

      }
    }
    int queryId = 1;
    for(String in:input){
      s = in;

      try {
        TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);

        if (s.equalsIgnoreCase("q")) {
          break;
        }

        dir = new File("../").getCanonicalPath();

        File file = new File(dir + "/results/lucene/" + queryId + "_lucene.txt");
        FileWriter fw = new FileWriter(file);
        BufferedWriter writer = new BufferedWriter(fw);

        Query q = new QueryParser(Version.LUCENE_47, "contents",
                analyzer).parse(s);
        searcher.search(q, collector);
        ScoreDoc[] hits = collector.topDocs().scoreDocs;
        writer.write("##################################################################");
        writer.newLine();
        writer.write("Output for query - " + s );
        writer.newLine();
        writer.newLine();

        // 4. display results
        System.out.println("Found " + hits.length + " hits.");
        for (int i = 0; i < hits.length; ++i) {
          int docId = hits[i].doc;
          Document d = searcher.doc(docId);
          System.out.println((i + 1) + ". " + d.get("path")
                  + " score=" + hits[i].score);
          String path = d.get("path");
          String filename =  path.split("\\\\")[path.split("\\\\").length-1];
          String a = filename.split("\\.")[0];
          writer.write(queryId + " Q0 " + a + " " + (i+1) + " " + hits[i].score + " Lucene");
          writer.newLine();
        }
        // 5. term stats --> watch out for which "version" of the term
        // must be checked here instead!
        Term termInstance = new Term("contents", s);
        long termFreq = reader.totalTermFreq(termInstance);
        long docCount = reader.docFreq(termInstance);
        System.out.println(s + " Term Frequency " + termFreq
                + " - Document Frequency " + docCount);
//        writer.write("\n" + s + " Term Frequency " + termFreq
//                + " - Document Frequency " + docCount );
        writer.newLine();
        writer.newLine();

        writer.close();
        queryId++;
      } catch (Exception e) {
        System.out.println("Error searching " + s + " : "
                + e.getMessage());
        break;
      }

    }


  }

  /**
   * Constructor
   *
   * @param indexDir
   *            the name of the folder in which the index should be created
   * @throws IOException
   *             when exception creating index.
   */
  LuceneApplication(String indexDir) throws IOException {

    FSDirectory dir = FSDirectory.open(new File(indexDir));

    IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
            analyzer);

    writer = new IndexWriter(dir, config);
  }

  /**
   * Indexes a file or directory
   *
   * @param fileName
   *            the name of a text file or a folder we wish to add to the
   *            index
   * @throws IOException
   *             when exception
   */
  public void indexFileOrDirectory(String fileName) throws IOException {
    // ===================================================
    // gets the list of files in a folder (if user has submitted
    // the name of a folder) or gets a single file name (is user
    // has submitted only the file name)
    // ===================================================
    addFiles(new File(fileName));

    int originalNumDocs = writer.numDocs();
    for (File f : queue) {
      FileReader fr = null;
      try {
        Document doc = new Document();

        // ===================================================
        // add contents of file
        // ===================================================
        fr = new FileReader(f);
        doc.add(new TextField("contents", fr));
        doc.add(new StringField("path", f.getPath(), Field.Store.YES));
        doc.add(new StringField("filename", f.getName(),
                Field.Store.YES));

        writer.addDocument(doc);
        System.out.println("Added: " + f);
      } catch (Exception e) {
        System.out.println("Could not add: " + f);
      } finally {
        fr.close();
      }
    }

    int newNumDocs = writer.numDocs();
    System.out.println("");
    System.out.println("************************");
    System.out
            .println((newNumDocs - originalNumDocs) + " documents added.");
    System.out.println("************************");

    queue.clear();
  }

  private void addFiles(File file) {

    if (!file.exists()) {
      System.out.println(file + " does not exist.");
    }
    if (file.isDirectory()) {
      for (File f : file.listFiles()) {
        addFiles(f);
      }
    } else {
      String filename = file.getName().toLowerCase();

      // ===================================================
      // Only index text files
      // ===================================================
      if (filename.endsWith(".htm") || filename.endsWith(".html")
              || filename.endsWith(".xml") || filename.endsWith(".txt")) {
        queue.add(file);
      } else {
        System.out.println("Skipped " + filename);
      }
    }
  }

  /**
   * Close the index.
   *
   * @throws IOException
   *             when exception closing
   */
  public void closeIndex() throws IOException {
    writer.close();
  }
}