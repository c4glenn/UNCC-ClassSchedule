import scrapy
import regex as re

class courseSider(scrapy.Spider):
    name = "course"

    def start_requests(self):
        courseList = []
        with open("courseNumbers.txt") as f:
            courseList = f.read().split(",")
        urls = [f'https://catalog.charlotte.edu/preview_course.php?catoid=29&coid={x}#' for x in courseList]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response, **kwargs):
        coid = response.url[-5:]
        title = response.css('#course_preview_title::text').get()
        courseCode = title[:8]
        title = title[12:]

        blockContent = response.css('td.block_content_popup').get()

        dmatches = re.finditer("<hr>(.*?)<br>", blockContent, re.MULTILINE)
        description = ""
        for match in dmatches:
            description = match.group(1)

        hmatches = re.finditer("<\/strong> \((.*?)\)", blockContent, re.MULTILINE)
        hours = 0
        for match in hmatches:
            hours = match.group(1)

        rmatches = re.finditer("Restriction\(s\):<\/strong> (.*?)<br>", blockContent, re.MULTILINE) 
        restrictions = ""
        for match in rmatches:
            restrictions = match.group(1)

        pmatches =  re.finditer('<a href=\\"preview_course_nopop.php\?catoid=29&amp;coid=(.*?)\\"', blockContent, re.MULTILINE)
        prereqs = []
        for match in pmatches:
            prereqs.append(match.group(1)) 


        yield {
            'coid' : coid,
            'code' : courseCode,
            'title' : title,
            'description':description,
            'hours' : hours,
            'restrictions': restrictions,
            'prerequisits':prereqs
        }
