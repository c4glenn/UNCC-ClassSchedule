import scrapy
import regex as re

class UnccSpider(scrapy.Spider):
    name = "uncc"

    def start_requests(self):
        urls = [f'https://catalog.charlotte.edu/content.php?catoid=29&catoid=29&navoid=2952&filter%5Bcpage%5D={x}' for x in range(1, 39)]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)
       
    def parse(self, response):
        page = response.url.split("%5D=")[1]

        regex = r'<a href=.*amp;coid=(.*?)"'
        
        unparsed = response.css('td.block_content_outer').css('table.table_default').css('table.table_default').getall()[3]
        #parsed = re.findall(r'<a href=."preview_course_nopop.php.catoid=29.amp.coid=(.*?)"', unparsed, re.MULTILINE)

        matches = re.finditer(regex, unparsed, re.MULTILINE)
        parsed = []

        for matchNum, match in enumerate(matches, start=1):
                self.log("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1

                    self.log("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

                parsed.append(match.groups()[0])

        yield {
            'page': page,
            'response': parsed
        }
        #.css('tbody').css('tr')
        #<a href=."preview_course_nopop.php.catoid=29&amp;coid=(.*?)"