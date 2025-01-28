import configparser

def load_config(config_file='config.ini'):
    """Carga la configuración desde un archivo INI."""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    jira_url = config.get('jira', 'url')
    jira_token = config.get('jira', 'token')
    jira_email = config.get('jira', 'email')



    return jira_url, jira_token, jira_email