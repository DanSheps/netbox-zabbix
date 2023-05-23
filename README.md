# Netbox Zabbix

A plugin to sync NetBox to Zabbix.

# Features

* Automatically update/delete zabbix with device information

# Installation

1. Install the plugin within your environment (pip install netbox-zabbix)
2. Create required configurations within NetBox:
   - username: Zabbix username
   - password: Zabbix password
   - tags: A list of tags to filter on for determining if the signal should fire.  Optional
   - snmp: dictionary with various SNMP settings.  Optional
   - group: Default host group.  Optional
3. Optionally, configure additional settings using configuration contexts with the root dictionary name of "zabbix":
   - Dictionary with the same settings available within the configuration.
4. Create a custom field to hold the zabbix host id:
   - Name: `zabbix_hostid`
   - Content type: `Device`
   - Label: `Zabbix Host ID`
   - Type: `Integer`
   - Required: `False`
   - UI visibility: `readonly`
5. Optionally, create a custom field to hold the zabbix host group id, if not using the default set group or configuration contexts
   - Name: `zabbix_group`
   - Content type: `Device Type`
   - Label: `Zabbix Group`
   - Type: `Integer`
   - Required: `False`
   - UI visibility:`read/write`
   
# SNMP Configuration

The SNMP configuration is quite robust and for pushing to Zabbix.

The SNMP dictionary can include any of the following:

```python
{
    'version': '2c',  # 1, 2c, 3
    'community': None,
    'context': None,
    'username': None,
    'level': None,  # None, noAuthNoPriv, authNoPriv, authPriv
    'auth_protocol': None,  # None, MD5, SHA1, SHA224, SHA256, SHA384, SHA512
    'auth_passphrase': None,
    'priv_protocol': None,  # None, DES, AES128, AES192, AES256, AES192C, AES256C
    'priv_passphrase': None,
}
```

# Config Contexts

Configuration Zabbix settings using Config Contexts within NetBox is available as well, which provide a much more robust configuration platform.  Any options from the settings can be used within the configuration context.

Confiuration context could look like:

```python
{
    'snmp': { 'community': 'public'},
    'tags': ['zabbix']
}
```

# Future

* Separate model for storing Zabbix information (instead of custom field)
* Separate model for storing configuration information (Remove config contexts, configuration parameters)