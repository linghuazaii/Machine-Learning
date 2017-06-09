import urllib2, re
import BeautifulSoup as bsoup
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

ignore_words = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def db_commit(self):
        self.con.commit()

    def get_entry_id(self, table, field, value, create_new = True):
        cur = self.con.execute('select rowid from %s where %s=\'%s\'' % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute('insert into %s (%s) values (\'%s\')' % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    def add_to_index(self, url, soup):
        if self.is_indexed(url):
            return
        print "Indexing %s" % url
        text = self.get_text_only(soup)
        words = self.separate_words(text)
        urlid = self.get_entry_id('urllist', 'url', url)
        for i in range(len(words)):
            word = words[i]
            if word in ignore_words:
                continue
            wordid = self.get_entry_id('wordlist', 'word', word)
            self.con.execute('insert into wordlocation(urlid,wordid,location)\
             values (%d,%d,%d)' % (urlid, wordid, i))

    def get_text_only(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            result_text = ''
            for t in c:
                subtext = self.get_text_only(t)
                result_text += subtext + '\n'
            return result_text
        else:
            return v.strip()

    def separate_words(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def is_indexed(self, url):
        res = self.con.execute('select rowid from urllist where url=\'%s\'' % url).fetchone()
        if res != None:
            rs = self.con.execute('select * from wordlocation where urlid=%d' % res[0]).fetchone()
            if rs != None:
                return True
        return False

    def add_link_ref(self, url_from, url_to, link_text):
        fromid = self.get_entry_id('urllist', 'url', url_from)
        toid = self.get_entry_id('urllist', 'url', url_to)
        self.con.execute('insert into link values(%d, %d)' % (fromid, toid))

    def crawl(self, pages, depth = 2):
        for i in range(depth):
            new_pages = set()
            for page in pages:
                try:
                    doc = urllib2.urlopen(page)
                except Exception as e:
                    print "can't open %s (%s)" % (page, e)
                    continue
                soup = bsoup.BeautifulSoup(doc.read())
                self.add_to_index(page, soup)
                #print soup.prettify()

                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find('\'') != -1: 
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.is_indexed(url):
                            new_pages.add(url)
                        link_text = self.get_text_only(link)
                        self.add_link_ref(page, url, link_text)
                self.db_commit()
            pages = new_pages

    def create_index_tables(self):
        try:
            self.con.execute('drop table if exists urllist')
            self.con.execute('drop table if exists wordlist')
            self.con.execute('drop table if exists wordlocation')
            self.con.execute('drop table if exists link')
            self.con.execute('drop table if exists linwords')
            self.con.execute('create table urllist(url)')
            self.con.execute('create table wordlist(word)')
            self.con.execute('create table wordlocation(urlid,wordid,location)')
            self.con.execute('create table link(fromid integer,toid integer)')
            self.con.execute('create table linkwords(wordid,linkid)')
            self.con.execute('create index wordidx on wordlist(word)')
            self.con.execute('create index urlidx on urllist(url)')
            self.con.execute('create index wordurlidx on wordlocation(wordid)')
            self.con.execute('create index urltoindx on link(toid)')
            self.con.execute('create index urlfromidx on link(fromid)')
            self.db_commit()
        except Exception as e:
            print e

    def calculate_page_rank(self, iterations = 20):
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key, score)')
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.db_commit()

        for i in range(iterations):
            print "Iteration %d" % i
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15
                for (linker, ) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    linking_pr = self.con.execute('select score from pagerank where urlid=%d' % linker).fetchone()[0]
                    linking_count = self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr += 0.85 * (linking_pr / linking_count)
                self.con.execute('update pagerank set score=%f where urlid=%d' % (pr, urlid))
            self.db_commit()

class searcher:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def get_match_rows(self, q):
        field_list = 'w0.urlid'
        table_list = ''
        clause_list = ''
        word_ids = []

        words = q.split(' ')
        tablenumber = 0

        for word in words:
            wordrow = self.con.execute('select rowid from wordlist where word=\'%s\'' % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                word_ids.append(wordid) 
                if tablenumber > 0:
                    table_list += ','
                    clause_list += ' and '
                    clause_list += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                field_list += ',w%d.location' % tablenumber
                table_list += 'wordlocation w%d' % tablenumber
                clause_list += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1
        fullquery = 'select %s from %s where %s' % (field_list, table_list, clause_list)
        #print fullquery
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]

        return rows, word_ids
        
    def get_scored_list(self, rows, wordids):
        total_scores = dict([(row[0], 0) for row in rows])

        #weights = [(1.0, self.frequency_score(rows))]
        #weights = [(1.0, self.location_score(rows))]
        weights = [(1.5, self.location_score(rows)), (1.0, self.frequency_score(rows)),
         (1.0, self.distance_score(rows)), (1.5, self.page_rank_score(rows))]

        for (weight, scores) in weights:
            for url in total_scores:
                total_scores[url] += weight * scores[url]

        return total_scores

    def get_url_name(self, rowid):
        return self.con.execute('select url from urllist where rowid=%d' % rowid).fetchone()[0]

    def query(self, q):
        rows, wordids = self.get_match_rows(q)
        scores = self.get_scored_list(rows, wordids)
        ranked_scores = sorted([(score, url) for (url, score) in scores.items()], reverse = 1)
        for (score, urlid) in ranked_scores[0:10]:
            print '%f\t%s' % (score, self.get_url_name(urlid))

    def normalize_scores(self, scores, small_is_better = 0):
        vsmall = 0.00001
        if small_is_better:
            min_score = min(scores.values())
            return dict([(u, float(min_score) / max(vsmall, l)) for (u, l) in scores.items()])
        else:
            max_score = max(scores.values())
            if max_score == 0: 
                max_score = vsmall
            return dict([(u, float(c) / max_score) for (u, c) in scores.items()])

    def frequency_score(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalize_scores(counts)

    def location_score(self, rows):
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]:
                locations[row[0]] = loc
        return self.normalize_scores(locations, small_is_better =1)

    def distance_score(self, rows):
        if len(rows[0]) <= 2:
            return dict([(row[0], 1.0) for row in rows])

        min_distance = dict([(row[0], 1000000) for row in rows])
        
        for row in rows:
            dist = sum([abs(row[i] - row[i - 1]) for i in range(2, len(row))])
            if dist < min_distance[row[0]]:
                min_distance[row[0]] = dist
        return self.normalize_scores(min_distance, small_is_better = 1)

    def inbound_link_score(self, rows):
        unique_urls = set([row[0] for row in rows])
        inbound_count = dict([(u, self.con.excute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in unique_urls])

        return self.normalize_scores(inbound_count)

    def page_rank_score(self, rows):
        page_ranks = dict([(row[0], self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        max_rank = max(page_ranks.values())
        normalized_scores = dict([(u, float(l) / max_rank) for (u, l) in page_ranks.items()])
        return normalized_scores

if __name__ == '__main__':
    spider = crawler('search_index.db')
    #spider.create_index_tables()
    #spider.crawl(['https://en.wikipedia.org/wiki/Concurrency_pattern'])
    #spider.calculate_page_rank()
    search = searcher('search_index.db')
    search.query('parallel programming')
