import logging

import nailgun.entities
import pytest
from airgun.session import Session
from fauxfactory import gen_string
from requests.exceptions import HTTPError

from robottelo.constants import DEFAULT_ORG

LOGGER = logging.getLogger('robottelo')


@pytest.fixture(scope='module')
def module_org():
    """Shares the same organization for all tests in specific test module.
    Returns 'Default Organization' by default, override this fixture on

    :rtype: :class:`nailgun.entities.Organization`
    """
    default_org_id = (
        nailgun.entities.Organization().search(query={'search': f'name="{DEFAULT_ORG}"'})[0].id
    )
    return nailgun.entities.Organization(id=default_org_id).read()


@pytest.fixture(scope='module')
def module_user(request, module_org):
    """Creates admin user with default org set to module org and shares that
    user for all tests in the same test module. User's login contains test
    module name as a prefix.

    :rtype: :class:`nailgun.entities.Organization`
    """
    # take only "module" from "tests.foreman.rhai.test_module"
    test_module_name = request.module.__name__.split('.')[-1].split('_', 1)[-1]
    login = f'{test_module_name}_{gen_string("alphanumeric")}'
    password = gen_string('alphanumeric')
    LOGGER.debug('Creating session user %r', login)
    user = nailgun.entities.User(
        admin=True,
        default_organization=module_org,
        description=f'created automatically by airgun for module "{test_module_name}"',
        login=login,
        password=password,
    ).create()
    user.password = password
    yield user
    try:
        LOGGER.debug('Deleting session user %r', user.login)
        user.delete(synchronous=False)
    except HTTPError as err:
        LOGGER.warning(f'Unable to delete session user: {err}')


@pytest.fixture
def autosession(test_name, module_user):
    """Session fixture which automatically initializes and starts airgun UI
    session and correctly passes current test name to it. Use it when you want
    to have a session started before test steps and closed after all of them,
    i.e., when you don't need manual control over when the session is started or
    closed.

    Usage::

        def test_foo(autosession):
            # your ui test steps here
            autosession.architecture.create({'name': 'bar'})

    """
    with Session(test_name, module_user.login, module_user.password) as started_session:
        yield started_session
