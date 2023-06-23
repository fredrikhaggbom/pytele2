import logging
import requests
import datetime
import json

from .const import (
    RES_UNLIMITED,
    RES_LIMIT,
    RES_USAGE,
    RES_DATA_LEFT,
    RES_PERIOD_START,
    RES_PERIOD_END,
    CONF_SUBSCRIPTION,
    CONF_SUBSCRIPTIONMODEL,
    RES_ERROR,
    Tele2ApiResult,
)


class Tele2Api:
    def __init__(
        self,
        username: str,
        password: str,
        subscriptionId: str = None,
        logger: logging.Logger = None,
    ):
        self._data = {
            RES_UNLIMITED: False,
            RES_USAGE: None,
            RES_LIMIT: None,
            RES_DATA_LEFT: None,
            RES_PERIOD_START: None,
            RES_PERIOD_END: None,
            RES_ERROR: None,
        }
        self.BASE_URL = "https://my.tso.tele2.se"
        self.AUTH_URL = self.BASE_URL + "/auth/login"
        self._LOGGER = logger

        self.SUBSCRIPTION_URL = (
            self.BASE_URL + "/api/subscriptions?refreshableOnly=false"
        )
        self.CREDENTIALS = {"username": username, "password": password}
        self.username = username
        self.session = requests.Session()
        self.tries = 0

        if subscriptionId == None:
            subData = self.getSubscription()
            subscriptionId = subData[CONF_SUBSCRIPTION]

        self.log("Subscription: %s", str(subscriptionId))

        self.DATA_USAGE_URL = (
            self.BASE_URL + "/api/subscriptions/" + subscriptionId + "/data-usage"
        )

    def getSubscription(self) -> dict:
        self.session.post(self.AUTH_URL, data=self.CREDENTIALS)
        resp = self.session.get(self.SUBSCRIPTION_URL)

        if resp.status_code == 200:
            data = json.loads(resp.content)
            self.log("Got subscription info: %s", str(data))
            if len(data) > 0 and "subsId" in data[0]:
                return {
                    CONF_SUBSCRIPTION: str(data[0]["subsId"]),
                    CONF_SUBSCRIPTIONMODEL: data[0]["name"],
                }

        return {}

    def getDataUsage(self) -> dict:
        try:
            resp = self.session.get(self.DATA_USAGE_URL)
            if (resp.status_code == 401 or resp.status_code == 403) and self.tries < 1:
                self.tries += 1
                self.updateAuth()
                return self.getDataUsage()
            elif resp.status_code == 200:
                data = json.loads(resp.content)
                limit = data[Tele2ApiResult.packageLimit]
                usage = data["usage"]
                remaining = data[Tele2ApiResult.remaining]

                self.log(
                    "Got result. Limit: %s, usage: %s, remaining: %s, unlimited: %s",
                    limit,
                    usage,
                    remaining,
                    data[Tele2ApiResult.unlimitedData],
                )
                self._data[RES_ERROR] = None

                if Tele2ApiResult.unlimitedData in data:
                    self._data[RES_UNLIMITED] = data[Tele2ApiResult.unlimitedData]

                if Tele2ApiResult.buckets in data and len(data["buckets"]) > 0:
                    for bucket in data["buckets"]:
                        if bucket["status"] == "active":
                            if Tele2ApiResult.startDate in bucket:
                                startDate = datetime.datetime.strptime(
                                    bucket[Tele2ApiResult.startDate], "%Y-%m-%d"
                                ).date()
                                self._data[RES_PERIOD_START] = startDate
                            if Tele2ApiResult.endDate in bucket:
                                endDate = datetime.datetime.strptime(
                                    bucket[Tele2ApiResult.endDate], "%Y-%m-%d"
                                ).date()
                                self._data[RES_PERIOD_END] = endDate
                            if Tele2ApiResult.unlimitedBucket in bucket:
                                self._data[RES_UNLIMITED] = bucket[
                                    Tele2ApiResult.unlimitedBucket
                                ]
                            break

                self.tries = 0
                self._data[RES_LIMIT] = limit
                self._data[RES_USAGE] = usage
                self._data[RES_DATA_LEFT] = remaining
                self.log("Setting native value to: %f", remaining)
                return self._data

        except requests.exceptions.RequestException as e:
            self._data[RES_ERROR] = e
            return self._data

        return {}

    def updateAuth(self) -> None:
        self.log("Updating authentication")
        self.session.post(self.AUTH_URL, data=self.CREDENTIALS)

    def log(self, msg, *args):
        if self._LOGGER is not None:
            self._LOGGER.error(msg, *args)
