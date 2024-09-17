import yaml


def load_config(config_file="/Users/simo/PycharmProjects/ArbitrageBot/arbitrage_bot/config.yml"):
    """
    Load the configuration file.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
