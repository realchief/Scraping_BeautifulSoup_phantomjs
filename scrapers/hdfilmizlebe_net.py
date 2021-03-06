# coding=utf-8

from sandcrawler.scraper import ScraperBase, SimpleScraperBase

class HdfilmizlebeNet(SimpleScraperBase):
    BASE_URL = 'http://www.hdfilmizlebe.org'
    OTHER_URLS = ['http://www.hdfilmizlebe.net','http://www.hdfilmizlebe.com']
    SCRAPER_TYPES = [ ScraperBase.SCRAPER_TYPE_OSP, ]
    LANGUAGE = 'tur'
    MEDIA_TYPES = [ ScraperBase.MEDIA_TYPE_FILM, ScraperBase.MEDIA_TYPE_TV, ]

    URL_TYPES = [ScraperBase.URL_TYPE_SEARCH, ScraperBase.URL_TYPE_LISTING, ]

    def _fetch_search_url(self, search_term, media_type):
        return '{base_url}/?arama={search_term}'.format(base_url=self.BASE_URL, search_term=search_term)

    def _fetch_no_results_text(self):
        return u'Üzgünüz, kriterlerinize uygun film yok.'

    def _fetch_next_button(self, soup):
        next_button = soup.find('a', text=u'»')
        if next_button:
            return next_button.href
        return None

    def _parse_search_result_page(self, soup):
        for result in soup.select('div.moviefilm'):
            link = result.select_one('a')
            self.submit_search_result(
                link_url=link.href,
                link_title=link.text,
                image=self.util.find_image_src_or_none(result, 'img'),
            )
    def _parse_parse_page(self, soup):
        index_page_title = self.util.get_page_title(soup)
        series_season = series_episode = None
        title = soup.select_one('h1')
        if title and title.text:
            series_season, series_episode = self.util.extract_season_episode(title.text)
        for result_link in soup.select('div.keremiya_part a'):
            if '#respond' in result_link.href:
                continue
            film_soup = self.get_soup(result_link.href)
            for link in film_soup.select('div#kendisi p iframe'):
                link_url = link['src']
                link_title = link.text
                if 'youtube' in link_url or 'simdiarabul' in link_url or 'simdifilmizle' in link_url:
                    continue
                if 'http' not in link_url:
                    link_url = 'http:'+link_url
                self.submit_parse_result(
                    index_page_title=index_page_title,
                    link_url=link_url,
                    link_title=link_title,
                    series_season=series_season,
                    series_episode=series_episode,
                )
