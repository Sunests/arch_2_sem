from faker import Faker
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio


class MongoConnector:
    _instance = None

    @classmethod
    def get_client(cls, collection_name: str):
        if cls._instance is None:
            username = "root"
            password = "example"
            mongo_uri = f"mongodb://{username}:{password}@mongo:27017/"
            cls._instance = AsyncIOMotorClient(mongo_uri)
        database = cls._instance["arch"]
        collection = database[collection_name]
        return collection


conferences_collection = MongoConnector.get_client(
    collection_name="conferences")
articles_collection = MongoConnector.get_client(collection_name="articles")
fake = Faker()


class DataIniter():

    def get_random_date(self, start_year, end_year):
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31)
        time_between_dates = end_date - start_date
        days_delta = int(time_between_dates.total_seconds() / 60 / 60 / 24)
        random_number_of_days = fake.random_int(min=0, max=days_delta)
        return start_date + datetime.timedelta(days=random_number_of_days)

    def get_fake_articles(self, conference_start_date, conference_end_date):
        articles = []
        count = fake.unique.random_int(min=100, max=1000)
        for _ in range(count):
            presentation_date = self.get_random_date(
                conference_start_date.year, conference_end_date.year
            )
            while presentation_date < conference_start_date or presentation_date > conference_end_date:
                presentation_date = self.get_random_date(
                    conference_start_date.year, conference_end_date.year
                )
            articles.append({
                "title": fake.sentence(),
                "text": fake.paragraph(nb_sentences=5),
                "UDK": fake.bothify(text="####-####"),
                "date_of_load": fake.date(),
                "presentation_date": presentation_date.strftime("%Y-%m-%d"),
            })
        return articles

    async def get_fake_conference(self):
        count_of_confs = fake.unique.random_int(min=20, max=30)
        confs = []
        for _ in range(count_of_confs):
            name = fake.unique.company()
            conference_start_date = self.get_random_date(2023, 2024)
            conference_end_date = conference_start_date + \
                datetime.timedelta(days=fake.random_int(min=1, max=10))
            dates_of_conference = []
            current_date = conference_start_date
            while current_date <= conference_end_date:
                dates_of_conference.append(current_date.strftime('%Y-%m-%d'))
                current_date += datetime.timedelta(days=1)

            report_ids = list(map(str, (await articles_collection.insert_many(
                self.get_fake_articles(
                    conference_start_date, conference_end_date)
            )).inserted_ids))
            confs.append(
                {
                    "name": name,
                    "articles": report_ids,
                    "dates_of_conference": dates_of_conference,
                }
            )
        await conferences_collection.insert_many(confs)


async def main():
    await articles_collection.drop()
    await conferences_collection.drop()
    await DataIniter().get_fake_conference()
    print(await conferences_collection.find_one())
    print(await articles_collection.find_one())

asyncio.run(main=main())
