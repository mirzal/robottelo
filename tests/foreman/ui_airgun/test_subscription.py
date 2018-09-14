"""Test class for Subscriptions/Manifests UI

:Requirement: Subscription

:CaseAutomation: Automated

:CaseLevel: Acceptance

:CaseComponent: UI

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
from robottelo import manifests
from nailgun import entities

from robottelo.datafactory import gen_string

from robottelo.decorators import (
    fixture,
    tier1,
    skip_if_not_set,
    upgrade,
)


@fixture
def organization():
    return entities.Organization().create()


@fixture
def manifest_file():
    with manifests.clone() as manifest:
        with open(manifest.filename, 'wb') as handler:
            handler.write(manifest.content.read())
        return manifest.filename


@skip_if_not_set('fake_manifest')
@tier1
@upgrade
def test_positive_upload_and_delete(session, manifest_file, organization):
    """Upload a manifest with minimal input parameters and delete it

    :id: 58e549b0-1ba3-421d-8075-dcf65d07510b

    :expectedresults: Manifest is uploaded and deleted successfully

    :CaseImportance: Critical
    """
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        assert session.subscription.has_manifest
        session.subscription.delete_manifest()
        assert not session.subscription.has_manifest


@skip_if_not_set('fake_manifest')
@tier1
def test_negative_delete(session, manifest_file, organization):
    """Upload a manifest with minimal input parameters and attempt to
    delete it but hit 'Cancel' button on confirmation screen

    :id: dbb68a99-2935-4124-8927-e6385e7eecd6

    :BZ: 1266827

    :expectedresults: Manifest was not deleted

    :CaseImportance: Critical
    """
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        assert session.subscription.has_manifest
        session.subscription.delete_manifest(really=False)
        assert session.subscription.has_manifest


@skip_if_not_set('fake_manifest')
@tier1
def test_positive_delete_confirmation(session, manifest_file, organization):
    """Upload a manifest with minimal input parameters, press 'Delete'
    button and check warning message on confirmation screen

    :id: 16160ee9-f818-447d-b7ab-d04d396d50c5

    :BZ: 1266827

    :expectedresults: confirmation dialog contains informative message
        which warns user about downsides and consequences of manifest
        deletion

    :CaseImportance: Critical
    """
    expected_message = [
        'Are you sure you want to delete the manifest?',
        'Note: Deleting a subscription manifest is STRONGLY discouraged. '
        'Deleting a manifest will:',
        'Delete all subscriptions that are attached to running hosts.',
        'Delete all subscriptions attached to activation keys.',
        'Disable Red Hat Insights',
        'Require you to upload the subscription-manifest and re-attach '
        'subscriptions to hosts and activation keys.',
        'This action should only be taken in extreme circumstances or for '
        'debugging purposes.',
    ]
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        actual_message = session.subscription.read_delete_manifest_message()
        for line in expected_message:
            assert line in actual_message


@skip_if_not_set('fake_manifest')
def test_read_provided_products(session, manifest_file, organization):
    subscription_name = 'Red Hat Satellite Employee Subscription'
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        provided_products = session.subscription.provided_products(
                subscription_name)
        assert 'Red Hat Satellite' in provided_products


def test_read_enabled_products(session, organization):
    product_name = gen_string('alpha')
    with session:
        session.organization.select(organization.name)
        session.product.create({'name': product_name})
        enabled_products = session.subscription.enabled_products(product_name)
        assert len(enabled_products) > 0
        assert product_name in enabled_products


@skip_if_not_set('fake_manifest')
def test_negative_read_enabled_products(session, manifest_file, organization):
    subscription_name = 'Red Hat Satellite Employee Subscription'
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        enabled_products = session.subscription.enabled_products(
                subscription_name)
        assert len(enabled_products) == 0
        assert 'Red Hat Enterprise Linux Server' not in enabled_products


# Manifest file generated by Robottelo does not allow to add subscriptions
# right now, so we depend on Default Organization existing and having manifest
# that does allow to add subscriptions. That setup must be done manually.
# This is for Arigun side testing purpose only
def test_add_subscription(session):
    subscription_name = 'CloudForms Employee Subscription'
    with session:
        session.organization.select('Default Organization')
        session.subscription.add(subscription_name, 10)
        assert session.subscription.search(subscription_name) is not None


@skip_if_not_set('fake_manifest')
def test_search_subscription(session, manifest_file, organization):
    subscription_name = 'Red Hat Satellite Employee Subscription'
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        assert session.subscription.search(subscription_name) is not None


@skip_if_not_set('fake_manifest')
def test_negative_search_subscription(session, manifest_file, organization):
    subscription_name = gen_string('alpha')
    with session:
        session.organization.select(organization.name)
        session.subscription.add_manifest(manifest_file)
        assert not session.subscription.search(subscription_name)


# Manifest file generated by Robottelo does not allow to remove subscriptions
# right now, so we depend on Default Organization existing and having
# Employee SKU added already. That setup must be done manually.
# This is for Arigun side testing purpose only
def test_remove_subscription(session):
    subscription_name = 'Employee SKU'
    with session:
        session.organization.select('Default Organization')
        session.subscription.delete(subscription_name)
        assert not session.subscription.search(subscription_name)
