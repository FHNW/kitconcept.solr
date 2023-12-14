import pytest


@pytest.fixture()
def member_request(request_factory, user_credentials):
    request = request_factory()
    request.auth = user_credentials
    yield request
    request.auth = ()


class TestEndpointRolesAndUsers:
    url = "/@solr?q=chomsky"

    @pytest.fixture
    def api_request(self, request_factory, users_credentials_role):
        def func(role: str) -> dict:
            req = request_factory()
            credentials = users_credentials_role.get(role, None)
            if credentials:
                req.auth = credentials
            return req

        return func

    @pytest.fixture(autouse=True)
    def _init(self, portal_with_content):
        self.portal = portal_with_content


class TestEndpointPermsAll(TestEndpointRolesAndUsers):
    @pytest.mark.parametrize(
        "role,path,expected",
        [
            ("anonymous", "/plone/document2", False),
        ],
    )
    def test_paths(
        self, api_request, all_path_string, role: str, path: str, expected: bool
    ):
        data = api_request(role).get(self.url).json()
        path_strings = all_path_string(data)
        assert (path in path_strings) is expected
