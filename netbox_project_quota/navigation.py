from packaging import version

from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

try:
    from extras.plugins import PluginMenu
    HAVE_MENU = True
except ImportError:
    HAVE_MENU = False
    PluginMenu = PluginMenuItem

project_buttons = [
    PluginMenuButton(
        link='plugins:netbox_project_quota:project_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

quota_template_buttons = [
    PluginMenuButton(
        link='plugins:netbox_project_quota:quotatemplate_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]


menu_buttons = (
    PluginMenuItem(
        link='plugins:netbox_project_quota:project_list',
        link_text='Project',
        buttons=project_buttons
    ),
    PluginMenuItem(
        link='plugins:netbox_project_quota:quotatemplate_list',
        link_text='Quota Template',
        buttons=quota_template_buttons
    )
)


if HAVE_MENU:
    menu = PluginMenu(
        label=f'Project',
        groups=(
            ('Project Quota', menu_buttons),
        ),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    # display under plugins
    menu_items = menu_buttons