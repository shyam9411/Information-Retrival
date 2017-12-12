import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
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

	String indexLocation = System.getProperty("user.dir") + "/InvertedIndex/";
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	//	String s = br.readLine();
	// 	String s =	System.getProperty("user.dir") + "/InvertedIndex/";
	Indexer_Module indexer = null;
	try {
		//	indexLocation = s;
	    indexer = new Indexer_Module(indexLocation);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}
	//Since we already obtained the inverted indexes, these codes can be omitted.
	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	//	while (!s.equalsIgnoreCase("q")) {
	//	    try {
	//		System.out
	//			.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
	//		System.out
	//			.println("[Acceptable file types: .xml, .html, .html, .txt]");
	//		s = br.readLine();
	//		if (s.equalsIgnoreCase("q")) {
	//		    break;
	//		}
	//
	//		// try to add file into the index
	//		indexer.indexFileOrDirectory(s);
	//	    } catch (Exception e) {
	//		System.out.println("Error indexing " + s + " : "
	//			+ e.getMessage());
	//	    }
	//	}

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
	//IndexSearcher searcher = new IndexSearcher(reader);
	TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);

	String s = "";
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out.println("Enter the search query (q=quit):");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		Query q = new QueryParser(Version.LUCENE_47, "contents",
			sAnalyzer).parse(s);
		IndexSearcher searcher = new IndexSearcher(reader);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");

		for (int i = 0; i < hits.length; ++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
            String[] sp = d.get("path").split("/");
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
	}
}