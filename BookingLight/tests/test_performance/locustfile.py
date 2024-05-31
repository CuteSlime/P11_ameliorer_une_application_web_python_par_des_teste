import time
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/")
        self.client.get("/book/Spring Festival/Simply Lift")
        self.client.get("/showPointBoard")
        self.client.post("/showSummary", data={"email": "foo"})
        self.client.post(
            "/purchasePlaces", {"competition": "foo", "club": "foo", "places": 10})

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    # def on_start(self):
