"""Botree AWS Logs utilities."""


class Logs:
    """AWS CloudWatch Logs operations."""

    def __init__(self, session):
        """
        Logs class init.

        Parameters
        ----------
        session : boto3.Session
            The authenticated session to be used for CloudWatch Logs operations.
        """
        self.session = session
        self.client = self.session.client(service_name="logs")

    def execute_query(
        self, log_group_names, query_string, start_time, end_time, **kwargs
    ):
        """
        Execute a query to retrieve logs and get the query results.

        Parameters
        ----------
        log_group_names : list
            The list of log group names to query.

        query_string : str
            The query string to search logs.

        start_time : int
            The start time of the logs to query (in milliseconds).

        end_time : int
            The end time of the logs to query (in milliseconds).

        kwargs : dict, optional
            Additional optional parameters to be passed to the `start_query` method.

        Returns
        -------
        dict
            The response containing the query results.
        """
        response = self.client.start_query(
            logGroupNames=log_group_names,
            queryString=query_string,
            startTime=start_time,
            endTime=end_time,
            **kwargs,
        )
        query_id = response["queryId"]

        while True:
            response = self.client.get_query_results(queryId=query_id)
            status_response = response["status"]
            if status_response == "Complete":
                break
            elif status_response == "Failed" or status_response == "Cancelled":
                raise Exception(
                    f"Query execution failed or was cancelled. Status: {status_response}"
                )

        return response
