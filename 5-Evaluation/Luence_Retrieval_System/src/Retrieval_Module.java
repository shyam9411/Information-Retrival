import java.io.*;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
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
public class Retrieval_Module {
//    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    // the actual Analyzer used
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    public static void main(String[] args) throws IOException {
        System.out
            .println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

        String indexLocation = System.getProperty("user.dir") + "/Inverted_Index/";
        // String corpusLocation = System.getProperty("user.dir") + "/Corpus/cacm";
        String queryLocation = System.getProperty("user.dir") + "/Query/processed.cacm.query.txt";
        String resultLocation = System.getProperty("user.dir") + "/Results/Lucene_Unigram_Case-folded.txt";

        Indexer_Module indexer = null;
        try {
            indexer = new Indexer_Module(indexLocation);
        } catch (Exception ex) {
            System.out.println("Cannot create index..." + ex.getMessage());
            System.exit(-1);
        }
        //Since we already obtained the inverted indexes, these codes can be omitted.
        // ===================================================
        // read input from user until he enters q for quit
        // ===================================================
        String s;
        // buildIndex(corpusLocation, indexer);
        // ===================================================
        // after adding, we always have to call the
        // closeIndex, otherwise the index is not created
        // ===================================================
        indexer.closeIndex();

        // =========================================================
        // Now search, change this program from interactive version into file reading version
        // =========================================================
        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
            indexLocation)));
        // read query bulks from txt.file
        FileInputStream fis = new FileInputStream(queryLocation);
        BufferedReader br = new BufferedReader(new InputStreamReader(fis));
        // write ranking results to files
        FileOutputStream fos = new FileOutputStream(resultLocation);
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));
        int query_index = 0;
        while ((s = br.readLine()) != null) {
            try {
                query_index ++;
                Query q = new QueryParser(Version.LUCENE_47, "contents",
                sAnalyzer).parse(s);
                TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
                IndexSearcher searcher = new IndexSearcher(reader);
                searcher.search(q, collector);
                ScoreDoc[] hits = collector.topDocs().scoreDocs;

                // 4. display results
                System.out.println("Found " + hits.length + " hits.");

                for (int i = 0; i < hits.length; ++i) {
                    int docId = hits[i].doc;
                    Document d = searcher.doc(docId);
                    String[] sp = d.get("path").split("/");
                    String result = query_index+" "+"Q0"+" "+sp[sp.length-1]+" "+
                            (i + 1)+" "+hits[i].score+" "+"Lucene_Unigram_Case-folded\n";
                    bw.write(result);
                    System.out.println((i + 1) + ". " + sp[sp.length-1]
                        + " score=" + hits[i].score);
                }
                // 5. term stats --> watch out for which "version" of the term
                // must be checked here instead!
                Term termInstance = new Term("contents", s);
                long termFreq = reader.totalTermFreq(termInstance);
                long docCount = reader.docFreq(termInstance);
                System.out.println(s + " Term Frequency " + termFreq
                    + " - Document Frequency " + docCount);

            } catch (Exception e) {
                System.out.println("Error searching " + s + " : "
                    + e.getMessage());
                break;
            }
	    }
	    br.close();
        bw.close();
	}

	public static void buildIndex(String path, Indexer_Module indexer){
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while (!path.equalsIgnoreCase("q")) {
            try {
                System.out
                        .println("Enter the FULL path to add into the index (q=quit): " +
                                "(e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
                System.out
                        .println("[Acceptable file types: .xml, .html, .html, .txt]");
                path = br.readLine();
                if (path.equalsIgnoreCase("q")) {
                    break;
                }

                // try to add file into the index
                indexer.indexFileOrDirectory(path);
            } catch (Exception e) {
                System.out.println("Error indexing " + path + " : "
                        + e.getMessage());
            }
        }
    }
}