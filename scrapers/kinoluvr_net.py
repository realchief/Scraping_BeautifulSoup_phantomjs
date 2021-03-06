# coding=utf-8

from sandcrawler.scraper import ScraperBase, SimpleScraperBase, OpenSearchMixin


class KinoluvrNet(OpenSearchMixin, SimpleScraperBase):
    BASE_URL = 'http://kinoluvr.net'
    OTHER_URLS = []
    SCRAPER_TYPES = [ScraperBase.SCRAPER_TYPE_OSP, ScraperBase.SCRAPER_TYPE_P2P, ]
    LANGUAGE = 'rus'
    MEDIA_TYPES = [ScraperBase.MEDIA_TYPE_FILM, ScraperBase.MEDIA_TYPE_TV, ]

    URL_TYPES = [ScraperBase.URL_TYPE_SEARCH, ScraperBase.URL_TYPE_LISTING, ]

    def _fetch_no_results_text(self):
        return u'К сожалению, поиск по сайту не дал никаких результатов'

    def _fetch_next_button(self, soup):
        next_link = soup.find('a', text=u'Вперед')
        return next_link['href'] if next_link else None

    def _parse_search_result_page(self, soup):
        for result in soup.select('div.shortstorryyyy'):
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
        for link in soup.select('div.viboom-overroll iframe'):
            link_url = link['src']
            if 'http' not in link_url:
                link_url = 'http:' + link_url
            link_title = link.text
            self.submit_parse_result(
                index_page_title=index_page_title,
                link_url=link_url,
                link_title=link_title,
                series_season=series_season,
                series_episode=series_episode,
            )
        for tor_link in soup.select('div.torrr a'):
            self.submit_parse_result(
                index_page_title=index_page_title,
                link_url=tor_link.href,
                link_title=tor_link.text,
                series_season=series_season,
                series_episode=series_episode,
            )