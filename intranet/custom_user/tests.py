from .apps import CustomUserConfig


def test_custom_user_installed(settings):
    assert CustomUserConfig.name in settings.INSTALLED_APPS
