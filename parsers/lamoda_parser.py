import aiohttp
import bs4
from dao.kafka_dao import KafkaSetup
from di.lamoda_di import LamodaService
from fake_useragent import UserAgent


class LamodaParser:
    def __init__(self, kafka: KafkaSetup, lamoda_db: LamodaService):
        ua = UserAgent()
        self.HEADERS = {"User-Agent": ua.random}
        self.base_url = "https://lamoda.by"
        self.category_class = "d-header-topmenu-category__link"
        self.product_card_class = "x-product-card__link"
        self.product_category_class = "x-premium-product-title__model-name"
        self.product_brand_class = "x-premium-product-title__brand-name"
        self.product_price_class = "x-premium-product-prices__price"
        self.product_description_attr_class = (
            "x-premium-product-description-attribute__name"
        )
        self.product_description_value_class = (
            "x-premium-product-description-attribute__value"
        )
        self.kafka = kafka
        self.lamoda_db = lamoda_db.dao

    async def get_amount_of_pages(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADERS) as resp:
                content = await resp.text()
                pages_amount = int(
                    content.split("pagination")[1].split('pages":')[1].split(",")[0]
                )
        return pages_amount if pages_amount else 1

    async def get_soup(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADERS) as resp:
                page = await resp.text()
                soup = bs4.BeautifulSoup(page, "lxml")
        return soup

    async def parse(self):
        soup = await self.get_soup(self.base_url)
        categories = soup.find_all("a", attrs={"class": f"{self.category_class}"})

        visited_products = set()
        for category in categories:
            category_url = self.base_url + category.attrs["href"]

            pages = await self.get_amount_of_pages(category_url)
            for page in range(1, pages + 1):
                category_soup = await self.get_soup(category_url + f"&page={page}")

                product_cards = category_soup.find_all(
                    "a", attrs={"class": f"{self.product_card_class}"}
                )
                for product in product_cards:
                    product_url = self.base_url + product.attrs["href"]
                    if not (product_url in visited_products):
                        visited_products.add(product_url)

                        product_soup = await self.get_soup(product_url)
                        try:
                            name = product_soup.find(
                                "div", attrs={"class": self.product_category_class}
                            ).get_text()
                        except AttributeError:
                            break
                        try:
                            brand = (
                                product_soup.find(
                                    "span", attrs={"class": self.product_brand_class}
                                )
                                .get_text()
                                .strip()
                            )
                        except AttributeError:
                            break
                        try:
                            price = (
                                product_soup.find(
                                    "span", attrs={"class": self.product_price_class}
                                )
                                .get_text()
                                .split()[0]
                            )
                        except AttributeError:
                            break

                        description_attrs_list = product_soup.find_all(
                            "span", attrs={"class": self.product_description_attr_class}
                        )
                        description_values_list = product_soup.find_all(
                            "span",
                            attrs={"class": self.product_description_value_class},
                        )

                        description = dict(
                            zip(
                                [attr.get_text() for attr in description_attrs_list],
                                [value.get_text() for value in description_values_list],
                            )
                        )

                        product_data = {
                            "category": category.get_text().strip(),
                            "brand": brand,
                            "name": name,
                            "price": price,
                            "description": description,
                        }
                        self.kafka.producer.send("lamoda", value=product_data)

        await self.lamoda_db.send_data(self.kafka.consumer_lamoda)
