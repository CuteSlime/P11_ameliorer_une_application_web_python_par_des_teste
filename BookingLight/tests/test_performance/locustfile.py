from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def list_competitions(self):
        self.client.post("/showSummary", data={"email": "foo"})

    @task(2)
    def edit_point(self):
        # self.client.get("/")
        # self.client.get("/book/Spring Festival/Simply Lift")
        # self.client.get("/showPointBoard")
        self.client.post(
            "/purchasePlaces", {"competition": "foo", "club": "foo", "places": 10})
