/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Date;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.TermFreqVector;

/** Computes TF-IDF and cosine similarities and print */
public class ContentBasedAnalysis {

  /** Simple command-line based search demo. */
  public static void main(String[] args) throws Exception {
    String usage =
      "Usage:\tjava QueryConvert [-index dir]";
    if (args.length > 0 && ("-h".equals(args[0]) || "-help".equals(args[0]))) {
      System.out.println(usage);
      System.exit(0);
    }

    String index = "index";
    String field = "contents";
    String queries = null;
    String queryString = null;
    
    for(int i = 0;i < args.length;i++) {
      if ("-index".equals(args[i])) {
        index = args[i+1];
        i++;
      } else if ("-field".equals(args[i])) {
        field = args[i+1];
        i++;
      } 
    }
    
    // Creation of reader and a searcher for the index
    IndexReader reader = IndexReader.open(FSDirectory.open(new File(index)));
    IndexSearcher searcher = new IndexSearcher(reader);

    // Reader to read File Names
    BufferedReader in = null;
    if (queries != null) {
      in = new BufferedReader(new InputStreamReader(new FileInputStream(queries), "UTF-8"));
    } else {
      in = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
    }

    while (true) {
      System.out.println("Enter filename 1 (or hit <RETURN>): ");
      String f1 = in.readLine();
      if (f1 == null || f1.length() == -1) break;
      f1 = f1.trim(); if (f1.length() == 0) break;
      System.out.println("Enter filename 2: ");
      String f2 = in.readLine();
      int id1 = findDocId(searcher,f1);
      if (id1 < 0) { System.out.println("No file "+f1+" found in index!"); break; }
      int id2 = findDocId(searcher,f2);
      if (id1 < 0) { System.out.println("No file "+f1+" found in index!"); break; }

      // Conversion to TF-IDF format
      TermWeight[] v1 = toTfIdf(reader,id1);
      TermWeight[] v2 = toTfIdf(reader,id2);
      
      System.out.println("The cosine similarity of the two files is: "+cosineSimilarity(v1,v2));

    }
    searcher.close();
    reader.close();
  }

  // Searches index of a searcher for a file with 'path' == filename field 
  private static int findDocId(IndexSearcher searcher, String filename) throws Exception {
     Term t = new Term("path",filename);
     Query q = new TermQuery(t);
     TopDocs td = searcher.search(q,2);
     if (td.totalHits < 1) return -1;
     else return td.scoreDocs[0].doc;
  }

  // Count the number of times String s appears in a document 
  private static int docFreq(IndexReader reader, String s) throws Exception {
      return reader.docFreq(new Term("contents",s));
  }
  
  // Calculation of Term weights of documents
  private static TermWeight[] toTfIdf(IndexReader reader, int docId) throws Exception {
     // get Lucene representation of a Term-Frequency vector
     TermFreqVector tfv = reader.getTermFreqVector(docId,"contents");
     String[] terms = tfv.getTerms();
     int[] freqs = tfv.getTermFrequencies();
     TermWeight[] tw = new TermWeight[terms.length];

     // Maximum Frequency of a term in the document
     int fmax = freqs[0];
     for (int i = 1; i < freqs.length; i++) {
         if (freqs[i] > fmax) fmax = freqs[i];
     }

     // number of docs in the index
     int nDocs = reader.numDocs();
     for (int i = 0; i < tw.length; i++) {
         tw[i] = new TermWeight(terms[i]);
     }
     return tw;
  }

  // prints the list of pairs (term,weight) in vector v
  private static void printTermWeightVector(TermWeight[] v) {
	  for (TermWeight[] array : vector) {
		    for (Object obj : array) {
		        System.out.println(obj);
		    }
		}
  }

  // Calculation of cosine similarity of documents v1 and v2
  private static double cosineSimilarity(TermWeight[] v1, TermWeight[] v2) {
      double dotProduct = 0.0;
      double magnitude1 = 0.0;
      double magnitude2 = 0.0;
      double cosineSimilarity = 0.0;

      for (int i = 0; i < v1.length; i++) //docVector1 and docVector2 must be of same length
      {
          dotProduct += v1[i] * v2[i];
          magnitude1 += Math.pow(v1[i], 2);
          magnitude2 += Math.pow(v2[i], 2);
      }
      magnitude1 = Math.sqrt(magnitude1);
      magnitude2 = Math.sqrt(magnitude2);
      if (magnitude1 != 0.0 | magnitude2 != 0.0)
      {
          cosineSimilarity = dotProduct / (magnitude1 * magnitude2);
      } 
      else
      {
          return 0.0;
      }
      return cosineSimilarity;
  }
}