def test_execute_query(botree_session, monkeypatch):
    """Execute query on AWS CloudWatch Logs."""
    monkeypatch.setattr(botree_session.cost_explorer.session, "client", mocked_logs)

    log_group_names = ["/log/group/mock"]
    query_string = "query_string"
    start_time = 1657606400000
    end_time = 1657612800000

    response = botree_session.logs.execute_query(
        log_group_names, query_string, start_time, end_time
    )

    assert response["status"] == "Complete"


def mocked_logs(*args, **kwargs):
    return MockLogs()


class MockLogs:
    """Class with mocked data to be able to test CostExplorer."""

    def start_query(*args, **kwargs):
        return {
            "queryId": "mocked-id",
        }

    def get_query_results(*args, **kwargs):
        return {"status": "Complete"}
