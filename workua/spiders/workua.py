import scrapy


class WorkUaSpider(scrapy.Spider):
    name = "workua"

    start_urls = ["https://www.work.ua/jobs-dnipro/"]

    def parse(self, response):
        for card in response.css(".card"):
            salary = (
                card.css(".add-bottom")
                .xpath("./following-sibling::div/span/text()")
                .get()
                .replace("\u202f", "")
                .replace("\xa0", "")
                .replace("\u2009", "")
            )
            if "грн" not in salary:
                salary = None
            description = card.css(".cut-bottom::text").getall()
            description = " ".join(description).strip()
            if salary is None:
                employer = card.css(".add-bottom").xpath("./following-sibling::div/span/span/text()").get()
            else:
                employer = (
                    card.css(".add-bottom")
                    .xpath("./following-sibling::div")
                    .xpath("./following-sibling::div/span/span/text()")
                    .get()
                )
            title = card.css(".add-bottom").xpath("./h2/a/@title").get()
            item = {"title": title, "salary": salary, "description": description, "employer": employer}
            yield item


# /html/body/section/div/div[3]/div[1]/div[2]/div[4]/div[4]/span[1]/span
