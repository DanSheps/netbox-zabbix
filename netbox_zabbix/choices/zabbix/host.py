from utilities.choices import ChoiceSet


class ZabbixHostInterfaceTypeChoices(ChoiceSet):
    """
    Choices for Zabbix host interface types.
    """

    AGENT = 'Agent'
    IPMI = 'IPMI'
    JMX = 'JMX'
    SNMP = 'SNMP'

    CHOICES = (
        (AGENT, 'Agent'),
        (IPMI, 'IPMI'),
        (JMX, 'JMX'),
        (SNMP, 'SNMP'),
    )

    MAPPING = {
        '1': AGENT,
        '2': SNMP,
        '3': IPMI,
        '4': JMX,
    }


class ZabbixHostInterfaceConnectionChoices(ChoiceSet):
    """
    Choices for Zabbix host interface connection types.
    """

    DNS = 'DNS'
    IP = 'IP'

    CHOICES = (
        (DNS, 'DNS'),
        (IP, 'IP Address'),
    )


class ZabbixHostInterfaceSNMPVersionChoices(ChoiceSet):
    """
    Choices for Zabbix host interface connection types.
    """

    V1 = '1'
    V2 = '2'
    V3 = '3'

    CHOICES = (
        (V1, 'SNMP v1'),
        (V2, 'SNMP v2c'),
        (V3, 'SNMP v3'),
    )


class ZabbixHostInterfaceSNMPSecurityChoices(ChoiceSet):
    """
    Choices for Zabbix host interface connection types.
    """

    NANP = 'noAuthNoPriv'
    ANP = 'authNoPriv'
    AP = 'authPriv'

    CHOICES = (
        (NANP, 'No Authentication and No Privacy'),
        (ANP, 'Authentication and No Privacy'),
        (AP, 'Athentication and Privacy'),
    )


class ZabbixHostInterfaceSNMPAuthProtocolChoices(ChoiceSet):
    """
    Choices for Zabbix host interface connection types.
    """

    MD5 = 'MD5'
    SHA1 = 'SHA1'
    SHA224 = 'SHA224'
    SHA256 = 'SHA256'
    SHA384 = 'SHA384'
    SHA512 = 'SHA512'

    CHOICES = (
        (MD5, 'MD5'),
        (SHA1, 'SHA1'),
        (SHA224, 'SHA224'),
        (SHA256, 'SHA256'),
        (SHA384, 'SHA384'),
        (SHA512, 'SHA512'),
    )


class ZabbixHostInterfaceSNMPPrivacyProtocolChoices(ChoiceSet):
    """
    Choices for Zabbix host interface connection types.
    """

    DES = 'DES'
    AES128 = 'AES128'
    AES192 = 'AES192'
    AES256 = 'AES256'
    AES192C = 'AES192C'
    AES256C = 'AES256C'

    CHOICES = (
        (DES, 'DES'),
        (AES128, 'AES128'),
        (AES192, 'AES192'),
        (AES256, 'AES256'),
        (AES192C, 'AES192C'),
        (AES256C, 'AES256C'),
    )
