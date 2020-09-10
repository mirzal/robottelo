from dynaconf import Validator

from robottelo.constants import AZURERM_VALID_REGIONS
from robottelo.constants import VALID_GCE_ZONES


validators = dict(
    server=[
        Validator("server.hostname", must_exist=True),
        Validator("SERVER.ssh_key", must_exist=True)
        | Validator("SERVER.ssh_password", must_exist=True),
    ],
    azurerm=[
        Validator(
            "azurerm.client_id",
            "azurerm.client_secret",
            "azurerm.subscription_id",
            "azurerm.tenant_id",
            "azurerm.azure_region",
            "azurerm.ssh_pub_key",
            "azurerm.username",
            "azurerm.password",
            "azurerm.azure_subnet",
            must_exist=True,
        ),
        Validator("azurerm.azure_region", is_in=AZURERM_VALID_REGIONS),
    ],
    capsule=[Validator("capsule.instance_name", must_exist=True)],
    certs=[
        Validator(
            "certs.cert_file",
            "certs.key_file",
            "certs.req_file",
            "certs.ca_bundle_file",
            must_exist=True,
        )
    ],
    clients=[Validator("clients.provisioning_server")],
    compute_resources=[Validator("compute_resources.libvirt_image_dir", must_exist=True)],
    # FIXME: merge obecnego pliku do struktury dynaconf, dodanie walidacji
    container_repo=[
        Validator(
            'container_repo.label',
            'container_repo.registry_url',
            'container_repo.registry_username',
            'container_repo.registry_password',
            'container_repo.repos_to_sync',
            must_exist=True,
        )
    ],
    discovery=[Validator("discovery.discovery_iso", must_exist=True)],
    distro=[
        Validator(
            'distro.image_el7',
            'distro.image_el6',
            'distro.image_el8',
            'distro.image_sles11',
            'distro.image_sles12',
            must_exist=True,
        )
    ],
    docker=[Validator('docker.docker_image', 'docker.external_registry_1', must_exist=True)],
    ec2=[
        Validator('ec2.access_key', 'ec2.secret_key', 'ec2.region', must_exist=True,),
        Validator('ec2.manage_ip', is_in=('Private', 'Public')),
    ],
    fake_capsules=[Validator('fake_capsules.port_range', must_exist=True)],
    # FIXME: że musi być default nie jest sprawdzane
    # w sumie to yaml, więc można zmienić? - że musi być przynajmniej jeden
    fake_manifest=[
        Validator(
            'fake_manifest.cert_url', 'fake_manifest.key_url', 'fake_manifest.url', must_exist=True
        ),
    ],
    gce=[
        Validator(
            "gce.project_id",
            "gce.client_email",
            "gce.cert_path",
            "gce.zone",
            "gce.cert_url",
            must_exist=True,
        ),
        # FIXME: przenieś do constant
        Validator("gce.cert_path", startswith='/usr/share/foreman/'),
        Validator("gce.zone", is_in=VALID_GCE_ZONES),
    ],
    ipa=[
        Validator(
            "ipa.basedn_ipa",
            "ipa.grpbasedn_ipa",
            "ipa.hostname_ipa",
            "ipa.password_ipa",
            "ipa.username_ipa",
            "ipa.user_ipa",
            "ipa.otp_user",
            "ipa.time_based_secret",
            "ipa.disabled_user_ipa",
            must_exist=True,
        )
    ],
    ldap=[
        Validator(
            "ldap.basedn",
            "ldap.grpbasedn",
            "ldap.hostname",
            "ldap.password",
            "ldap.username",
            must_exist=True,
        )
    ],
    oscap=[Validator("oscap.content_path", "oscap.tailoring_path", must_exist=True,)],
    osp=[
        Validator(
            "osp.hostname",
            "osp.username",
            "osp.password",
            "osp.tenant",
            "osp.project_domain_id",
            "osp.security_group",
            "osp.vm_name",
            "osp.image_os",
            "osp.image_arch",
            "osp.image_username",
            "osp.image_name",
            must_exist=True,
        )
    ],
    ostree=[Validator("ostree.ostree_installer", must_exist=True)],
    performance=[
        Validator(
            "performance.cdn_address",
            "performance.virtual_machines",
            "performance.fresh_install_savepoint",
            "performance.enabled_repos_savepoint",
            must_exist=True,
        )
    ],
    report_portal=[
        Validator(
            "report_portal.portal_url",
            "report_portal.project",
            "report_portal.api_key",
            must_exist=True,
        )
    ],
    rhev=[
        Validator(
            "rhev.hostname",
            "rhev.username",
            "rhev.password",
            "rhev.datacenter",
            "rhev.vm_name",
            "rhev.storage_domain",
            "rhev.image_os",
            "rhev.image_arch",
            "rhev.image_username",
            "rhev.image_password",
            "rhev.image_name",
            must_exist=True,
        )
    ],
    rhsso=[
        Validator(
            "rhsso.host_name",
            "rhsso.host_url",
            "rhsso.rhsso_user",
            "rhsso.user_password",
            "rhsso.realm",
            must_exist=True,
        )
    ],
    # FIXME: SharedFunctionSettings
    shared_function=[],
    # FIXME: UpgradeSettings , complex validation rules
    upgrade=[],
    # FIXME: VirtWhoSettings
    virtwho=[],
    # FIXME: VlanNetworkSettings , complex validation rules
    vlan_networking=[],
    vmware=[
        Validator(
            "vmware.vcenter",
            "vmware.username",
            "vmware.password",
            "vmware.datacenter",
            "vmware.vm_name",
            "vmware.image_os",
            "vmware.image_arch",
            "vmware.image_username",
            "vmware.image_password",
            "vmware.image_name",
            must_exist=True,
        )
    ],
)
