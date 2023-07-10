"""Botree Cost Explorer utilities."""


class CostExplorer:
    """AWS Cost Explorer operations."""

    def __init__(self, session):
        """
        Cost Explorer class init.

        Parameters
        ----------
        session : boto3.Session
            The authenticated session to be used for Cost Explorer operations.
        """
        self.session = session
        self.client = self.session.client(service_name="ce")

    def get_costs(self, time_period, granularity, metrics, **kwargs):
        """
        Get cost and usage data.

        Parameters
        ----------
        time_period : dict
            The time period for which you want to retrieve the data.
            Example: {'Start': '2023-07-01', 'End': '2023-07-31'}

        granularity : str
            The granularity of the returned data.
            Valid values: DAILY, MONTHLY

        metrics : list
            The metrics to retrieve.
            Example: ['BlendedCost', 'UnblendedCost']

        Returns
        -------
        dict
            The response containing cost and usage data.
        """
        response = self.client.get_cost_and_usage(
            TimePeriod=time_period, Granularity=granularity, Metrics=metrics, **kwargs
        )
        return response

    def get_forecasts(self, time_period, granularity, metric, **kwargs):
        """
        Get cost forecasts.

        Parameters
        ----------
        time_period : dict
            The time period for which you want to retrieve the forecast.
            Example: {'Start': '2023-07-01', 'End': '2023-07-31'}

        metric : str
            The forecast metric to retrieve.
            Example: 'BlendedCost'

        kwargs : dict, optional
            Additional optional parameters to be passed to the `get_cost_forecast` method.

        Returns
        -------
        dict
            The response containing the cost forecast data.
        """
        response = self.client.get_cost_forecast(
            TimePeriod=time_period, Granularity=granularity, Metric=metric, **kwargs
        )
        return response
