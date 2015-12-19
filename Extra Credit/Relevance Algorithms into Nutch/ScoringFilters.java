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

package org.apache.nutch.scoring;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.io.Text;
import org.apache.nutch.crawl.CrawlDatum;
import org.apache.nutch.crawl.Inlinks;
import org.apache.nutch.indexer.NutchDocument;
import org.apache.nutch.parse.Parse;
import org.apache.nutch.parse.ParseData;
import org.apache.nutch.plugin.PluginRepository;
import org.apache.nutch.protocol.Content;
import org.apache.nutch.scoring.ScoringFilters.LinkBasedSimilarity.document;

/**
 * Creates and caches {@link ScoringFilter} implementing plugins.
 * 
 * @author Andrzej Bialecki and Team 33 CSCI 572 
 */
public class ScoringFilters extends Configured implements ScoringFilter {

  private ScoringFilter[] filters;

  class ValueComparator implements Comparator 
  {
  	Map map;
  	public ValueComparator(Map map) {
  		this.map = map;
  	}
   
  	@SuppressWarnings("unchecked")
  	public int compare(Object keyA, Object keyB) {
  		Comparable valueA = (Comparable) map.get(keyA);
  		Comparable valueB = (Comparable) map.get(keyB);
  		return valueB.compareTo(valueA);
  	}
  }

  public class LinkBasedSimilarity 
  {
    public HashMap<Float,List<document>> reversemap = new HashMap<Float,List<document>>();
  	public class document
  	{
  	 public String id;	
  	 public int links;
  	 HashMap<document, Integer> hmap = new HashMap<document, Integer>();  		
  	 public List<String>gunType;
  	 public List<String>keywords;
  	 public List<String>locs;
  	 public float xcentre;
  	 public float ycentre;
  	 public void setlinks(int links)
  	 {
  		 this.links=links;
  	 }
  	 public void setHashmap(document doc,int links)
  	 {
  		 this.hmap.put(doc, links);
  	 }

  	}
  	
  	public void  populateRealDocs() throws IOException
  	{
  		String line1 = null, keepbuffer;
  		List<document> docs= new ArrayList<document>();
  		File doc1 = new File("solrindex");
  		FileReader fr1 = null;
  		try {
  			fr1 = new FileReader("C:\\Stuff\\workspace\\Linkbased\\src\\inp.txt");
  		} catch (FileNotFoundException e) {
  			// TODO Auto-generated catch block
  			e.printStackTrace();
  		}
  		BufferedReader buffer1 = new BufferedReader(fr1);
  		StringBuffer stringBuffer1 = new StringBuffer();
  		line1="dummy.";
  			for(int objs=0;objs<4;objs++)
  			{
  				LinkBasedSimilarity l=new LinkBasedSimilarity();
  				document temp=l.new document();
  			
  				line1=buffer1.readLine();
  				keepbuffer = line1.replaceAll("\\s","");
  				String content[]=keepbuffer.split(":");
  				temp.id=content[1];
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  				String strinstr=content[1];
  				temp.gunType=Arrays.asList(strinstr.split("\\s*,\\s*"));
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  				String strkw=content[1];
  				temp.keywords=Arrays.asList(strkw.split("\\s*,\\s*"));
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  				temp.wmlat=Float.parseFloat(content[1]);
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  				String strloc=content[1];
  				temp.locs=Arrays.asList(strloc.split("\\s*,\\s*"));
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  				temp.smlat=Float.parseFloat(content[1]);
  			
  				line1=buffer1.readLine().replaceAll("\\s","");
  				content=line1.split(":");
  				docs.add(temp);
  			}
  		keywordscommon(docs.get(0),docs.get(1));
  		loccommon(docs.get(0),docs.get(1));
  		instrcommon(docs.get(0),docs.get(1));
  	}
  	
  	public void keywordscommon(document d1,document d2)
  	{
  		Collection<String> col1=d1.keywords;
  		Collection<String> col2=d2.keywords;
  		Collection<String>sim= new HashSet<String>(col1);
  		System.out.println(col1);
  		System.out.println(col2);
  		sim.retainAll(col2);
  		System.out.println(sim);
  		
  	}
  	
  	public void loccommon(document d1,document d2)
  	{
  		Collection<String> col1=d1.locs;
  		Collection<String> col2=d2.locs;
  		Collection<String>sim= new HashSet<String>(col1);
  		System.out.println(col1);
  		System.out.println(col2);
  		sim.retainAll(col2);
  		System.out.println(sim);
  	}
  	
  	public void instrcommon(document d1,document d2)
  	{
  		Collection<String> col1=d1.gunType;
  		Collection<String> col2=d2.gunType;
  		Collection<String>sim= new HashSet<String>(col1);
  		System.out.println(col1);
  		System.out.println(col2);
  		sim.retainAll(col2);
  		System.out.println(sim);
  	}
  	
  	public void computedist(document d1,document d2)
  	{
  		float x1,x2,y1,y2;
  		x1=d1.xcentre;
  		x2=d2.xcentre;
  		y1=d1.ycentre;
  		y2=d2.ycentre;
  	}
  	
  	public void printorder(Map<Float, List<document>>pr)
  	{
  		for(Map.Entry<Float,List<document>> entry : pr.entrySet()) 
  		{
  			List<document>dl=entry.getValue();
  			List<String>idlist=new ArrayList<String>();
  			for(document d:dl)
  			{
  				idlist.add(d.id);
  			}
  			System.out.println(Arrays.toString(idlist.toArray())+":"+entry.getKey());	
  		}
  	}
  	
  	public HashMap<Float,List<document>> getPageRank(HashMap<Float, List<document>> score){
  	  return score;
  	}

  	public void generatePageRank()
  	{
  		document[] document_list=new document[4];
  		LinkBasedSimilarity link=new LinkBasedSimilarity();
  		try {
  			populateRealDocs();
  		} catch (IOException e) {
  			// TODO Auto-generated catch block
  			e.printStackTrace();
  		}
  		HashMap<document , Float>pagerank=new HashMap<document, Float>();
  		HashMap<document , Float>new_pagerank=new HashMap<document, Float>();
  		for(int i=0;i<4;i++)
  		{
  			
  			pagerank.put(document_list[i], 1.0f);
  		}
  		float d=0.85f;
  		float sum;
  		while(true)
  		{
  			new_pagerank.clear();
  			for (int i=0;i<4;i++)
  			{
  				sum=0f;
  				for (Map.Entry<document, Integer> entry : document_list[i].hmap.entrySet())
  				{
  					sum+=pagerank.get(entry.getKey())/entry.getKey().links;
  				}
  				sum*=d;
  				sum+=(1-d);
  				new_pagerank.put(document_list[i],sum);	
  			}
  			if(pagerank.equals(new_pagerank))
  			{
  				break;
  			}
  			else
  			{
  				pagerank.clear();
  				for (Map.Entry<document, Float> entry : new_pagerank.entrySet())
  				{
  					pagerank.put(entry.getKey(), entry.getValue());
  					
  				}	
  			}
  			
  		}
  		
  		HashMap<Float, List<document>>ultapr=new HashMap<Float, List<LinkBasedSimilarity.document>>();
  		for (Map.Entry<document, Float> entry : pagerank.entrySet())
  		{
  			ultapr.put(entry.getValue(), new ArrayList<document>());
  		}
  		for (Map.Entry<document, Float> entry : pagerank.entrySet())
  		{
  			{
  				ultapr.get(entry.getValue()).add(entry.getKey());
  			}
  			
  		}
  		
  		TreeMap<Float, List<document>> map = new TreeMap<Float, List<document>>(ultapr);
  		reversemap = (HashMap<Float,List<document>>) map.descendingMap();
  		printorder(reversemap);
  	}
  }
  
  public ScoringFilters(Configuration conf) {
    super(conf);
    this.filters = (ScoringFilter[]) PluginRepository.get(conf)
        .getOrderedPlugins(ScoringFilter.class, ScoringFilter.X_POINT_ID,
            "scoring.filter.order");
  }

  /** Calculate a sort value for Generate. */
  public float generatorSortValue(Text url, CrawlDatum datum, float initSort)
      throws ScoringFilterException {
	  initSort=1;
    return initSort;
  }

  /** Calculate a new initial score, used when adding newly discovered pages. */
  public void initialScore(Text url, CrawlDatum datum)
      throws ScoringFilterException {
	  LinkBasedSimilarity l = new LinkBasedSimilarity();
	    try {
			l.populateRealDocs();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
  }

  /** Calculate a new initial score, used when injecting new pages. */
  public void injectedScore(Text url, CrawlDatum datum)
      throws ScoringFilterException {
	  LinkBasedSimilarity l = new LinkBasedSimilarity();
	    try {
			l.populateRealDocs();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
  }

  /** Calculate updated page score during CrawlDb.update(). */
  public void updateDbScore(Text url, CrawlDatum old, CrawlDatum datum,
      List<CrawlDatum> inlinked) throws ScoringFilterException {
      LinkBasedSimilarity l = new LinkBasedSimilarity();
      l.generatePageRank();
	  for (int i = 0; i < this.filters.length; i++) {
      this.filters[i].updateDbScore(url, old, datum, inlinked);
    }
  }

  public void passScoreBeforeParsing(Text url, CrawlDatum datum, Content content)
      throws ScoringFilterException {
    for (int i = 0; i < this.filters.length; i++) {
      this.filters[i].passScoreBeforeParsing(url, datum, content);
    }
  }

  public void passScoreAfterParsing(Text url, Content content, Parse parse)
      throws ScoringFilterException {
    for (int i = 0; i < this.filters.length; i++) {
      this.filters[i].passScoreAfterParsing(url, content, parse);
    }
  }

  public CrawlDatum distributeScoreToOutlinks(Text fromUrl,
      ParseData parseData, Collection<Entry<Text, CrawlDatum>> targets,
      CrawlDatum adjust, int allCount) throws ScoringFilterException {
    for (int i = 0; i < this.filters.length; i++) {
      adjust = this.filters[i].distributeScoreToOutlinks(fromUrl, parseData,
          targets, adjust, allCount);
    }
    return adjust;
  }

  public float indexerScore(Text url, NutchDocument doc, CrawlDatum dbDatum,
      CrawlDatum fetchDatum, Parse parse, Inlinks inlinks, float initScore)
      throws ScoringFilterException {
	  LinkBasedSimilarity l = new LinkBasedSimilarity();
	    l.generatePageRank();
	    HashMap<Float, List<document>> score = null;
	    
		HashMap<Float, List<document>> res = l.getPageRank(score);
    return initScore;
  }
}
