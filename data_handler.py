from dotenv import dotenv_values
import pandas as pd
import requests

class DataHandler():

    def __init__(self) -> None:

        config = dotenv_values(".env")
        self.strava_id = config["STRAVA_ID"]
        self.strava_secret = config["STRAVA_SECRET"]
        self.refresh_token = config["REFRESH_TOKEN"]
        self.base_url = "https://www.strava.com/api/v3/"

        self._generate_access_token()

    def _generate_access_token(self) -> None:
        
        refresh_url = f"https://www.strava.com/oauth/token?client_id={self.strava_id}&client_secret={self.strava_secret}&refresh_token={self.refresh_token}&grant_type=refresh_token"
        r = requests.post(refresh_url)

        self.access_token = r.json()["access_token"]

    def get_activities(self, start_date: str) -> None:

        url = self.base_url + "athlete/activities"
        header = {"Authorization": "Bearer " + self.access_token}
        param = {"page": "1", "per_page": "200", "after": start_date}
        r = requests.get(url, headers=header, params=param)

        return pd.DataFrame(r.json())

    def get_activity_streams(self, id: str) -> pd.DataFrame:

        url = self.base_url + f"activities/{id}/streams"
        header = {"Authorization": "Bearer " + self.access_token}
        param = {"keys": "distance,heartrate,time,watts", "key_by_type":"true", "resolution": "high"}
        r = requests.get(url, headers=header, params=param)

        df = pd.DataFrame(
            list(zip(
                r.json()["time"]["data"],
                r.json()["distance"]["data"],
                r.json()["heartrate"]["data"],
                r.json()["watts"]["data"],
                )),
            columns=["time", "distance", "heartrate", "watts"]
            )

        return df.set_index("time")
