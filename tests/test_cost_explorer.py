import pytest


def test_get_costs(botree_session, monkeypatch):
    """Get costs of AWS infrastructure based on time period."""
    monkeypatch.setattr(botree_session.cost_explorer.session, "client", mocked_ce)

    time_period = {"Start": "2023-07-01", "End": "2023-07-31"}
    granularity = "DAILY"
    metrics = ["UnblendedCost"]

    response = botree_session.cost_explorer.get_costs(time_period, granularity, metrics)
    assert response == MockCe.get_cost_and_usage()


def test_get_forecasts(botree_session, monkeypatch):
    """Get cost forecasts based on time period."""
    monkeypatch.setattr(botree_session.cost_explorer.session, "client", mocked_ce)

    time_period = {"Start": "2023-07-01", "End": "2023-07-31"}
    granularity = "MONTHLY"
    metric = "UnblendedCost"

    response = botree_session.cost_explorer.get_forecasts(
        time_period, granularity, metric
    )
    assert response == MockCe.get_cost_forecast()


def mocked_ce(*args, **kwargs):
    return MockCe()


class MockCe:
    """Class with mocked data to be able to test CostExplorer."""

    def get_cost_and_usage(*args, **kwargs):
        return {
            "TimePeriod": {"Start": "2023-07-01", "End": "2023-07-31"},
            "Granularity": "DAILY",
            "Metrics": ["UnblendedCost"],
        }

    def get_cost_forecast(*args, **kwargs):
        return {
            "TimePeriod": {"Start": "2023-07-01", "End": "2023-07-31"},
            "Granularity": "MONTHLY",
            "Metric": "UnblendedCost",
            "ForecastResultsByTime": [
                {
                    "TimePeriod": {"Start": "2023-07-01", "End": "2023-07-31"},
                    "MeanValue": "100.00",
                }
            ],
        }
