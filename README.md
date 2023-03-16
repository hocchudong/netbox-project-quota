# Netbox Project Quota

## Installing

To install the plugin, first using pip and install netbox-project-quota:

```
pip3 install netbox-project-quota
```

Next, enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`, or if you have a `/configuration/plugins.py `file, the plugins.py file will take precedence.

```
PLUGINS = [
    'netbox_manage_project'
]
```

Then you may need to perform the final step of restarting the service to ensure that the changes take effect correctly:

```
sudo systemctl restart netbox
```

## Screenshots

![](./images/quotatemplate.png)

![](./images/projectquota.png)

![](./images/projectdetail.png)
