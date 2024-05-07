from utilities.choices import ChoiceSet


__all__ = (
    'SNMPAuthChoices',
    'SNMPPrivChoices',
    'SNMPSecurityChoices',
    'SNMPVersionChoices',
)


class SNMPVersionChoices(ChoiceSet):

    VERSION_1 = '1'
    VERSION_2C = '2c'
    VERSION_3 = '3'

    CHOICES = (
        (VERSION_1, 'Version 1'),
        (VERSION_2C, 'Version 2c'),
        (VERSION_3, 'Version 3'),
    )


class SNMPSecurityChoices(ChoiceSet):

    SECURITY_NOAUTHNOPRIV = 'noAuthNoPriv'
    SECURITY_AUTHNOPRIV = 'authNoPriv'
    SECURITY_AUTHPRIV = 'authPriv'

    CHOICES = (
        (SECURITY_NOAUTHNOPRIV, 'No Authentication, No Privacy'),
        (SECURITY_AUTHNOPRIV, 'Authentication, No Privacy'),
        (SECURITY_AUTHPRIV, 'Authentication, Privacy'),
    )


class SNMPAuthChoices(ChoiceSet):

    # MD5, SHA1, SHA224, SHA256, SHA384, SHA512

    AUTH_MD5 = 'hmac-md5'
    AUTH_SHA1 = 'hmac-sha'
    AUTH_SHA224 = 'hmac-sha-224'
    AUTH_SHA256 = 'hmac-sha-256'
    AUTH_SHA384 = 'hmac-sha-384'
    AUTH_SHA512 = 'hmac-sha-512'

    CHOICES = (
        (AUTH_MD5, AUTH_MD5.upper()),
        (AUTH_SHA1, AUTH_SHA1.upper()),
        (AUTH_SHA224, AUTH_SHA224.upper()),
        (AUTH_SHA256, AUTH_SHA256.upper()),
        (AUTH_SHA384, AUTH_SHA384.upper()),
        (AUTH_SHA512, AUTH_SHA512.upper()),
    )


class SNMPPrivChoices(ChoiceSet):

    # None, DES, AES128, AES192, AES256, AES192C, AES256C

    PRIV_DES = 'cbc-des'
    PRIV_3DES = 'cbc-3des'
    PRIV_CFB_AES_128 = 'cfb-aes-128'
    PRIV_CFB_AES_192 = 'cfb-aes-192'
    PRIV_CFB_AES_256 = 'cfb-aes-256'

    CHOICES = (
        (PRIV_DES, PRIV_DES.upper()),
        (PRIV_3DES, PRIV_3DES.upper()),
        (PRIV_CFB_AES_128, PRIV_CFB_AES_128.upper()),
        (PRIV_CFB_AES_192, PRIV_CFB_AES_192.upper()),
        (PRIV_CFB_AES_256, PRIV_CFB_AES_256.upper()),
    )
