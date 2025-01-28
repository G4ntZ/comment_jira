import configparser
import requests
import json
from requests.auth import HTTPBasicAuth
from config_credentials import load_config
import sys

def agregar_comentario(issue_id, jira_url, jira_email, jira_token, pauta, restriccion_horaria="sin restricción horaria"):
    url = f"{jira_url}/issue/{issue_id}/comment"
    auth = HTTPBasicAuth(jira_email, jira_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = json.dumps({
        "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "panel",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Paso a Producción",
                                        "marks": [
                                            {
                                                "type": "strong"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "heading",
                                "attrs": {
                                    "level": 6
                                },
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Aprobado por SQA",
                                        "marks": [
                                            {
                                                "type": "strong"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Revisión Manual",
                                        "marks": [
                                            {
                                                "type": "strong"
                                            },
                                            {
                                                "type": "underline"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": ":"
                                    }
                                ]
                            },
                            {
                                "type": "bulletList",
                                "content": [
                                    {
                                        "type": "listItem",
                                        "content": [
                                            {
                                                "type": "paragraph",
                                                "content": [
                                                    {
                                                        "type": "text",
                                                        "text": "Por SVN"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": " "
                                    },
                                    {
                                        "type": "hardBreak"
                                    },
                                    {
                                        "type": "text",
                                        "text": "Instalación",
                                        "marks": [
                                            {
                                                "type": "strong"
                                            },
                                            {
                                                "type": "underline"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": ":"
                                    }
                                ]
                            },
                            {
                                "type": "bulletList",
                                "content": [
                                    {
                                        "type": "listItem",
                                        "content": [
                                            {
                                                "type": "paragraph",
                                                "content": [
                                                    {
                                                        "type": "text",
                                                        "text": f"{restriccion_horaria}"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": " "
                                    },
                                    {
                                        "type": "hardBreak"
                                    },
                                    {
                                        "type": "text",
                                        "text": "Pauta(s)",
                                        "marks": [
                                            {
                                                "type": "strong"
                                            },
                                            {
                                                "type": "underline"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": ":"
                                    },
                                    {
                                        "type": "hardBreak"
                                    },
                                    {
                                        "type": "inlineCard",
                                        "attrs": {
                                            "url": f"https://afphabitat-cl.atlassian.net/browse/{pauta}#icft={pauta}"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": " Oracle"
                                    }
                                ]
                            }
                        ],
                        "attrs": {
                            "panelType": "success"
                        }
                    }
                ]
            }
    })
    
    response = requests.post(url, data=payload, headers=headers, auth=auth)
    
    if response.status_code == 201:
        print(f"Comentario agregado exitosamente al issue {issue_id}.")
    else:
        print(f"Error al agregar comentario: {response.status_code}")
        print(response.json())

def transition_issue(issue_key, jira_url, jira_token, jira_email, id_transition):
    """Cambia el estado de un issue utilizando la transición especificada."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    def attempt_transition(transition_id):
        data = {
            "transition": {
                "id": transition_id
            }
        }
        try:
            response = requests.post(
                f"{jira_url}/issue/{issue_key}/transitions",
                headers=headers,
                data=json.dumps(data),
                auth=HTTPBasicAuth(jira_email, jira_token)
            )

            response.raise_for_status()
            print(f"Issue {issue_key} transitioned successfully with ID {transition_id}.")
            return True  # Transición exitosa

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred with ID {transition_id}: {http_err}")
            return False  # Intento fallido
    
    attempt_transition(id_transition)


def main():
    """
    Función principal para buscar issues y cambiar el estado del primero encontrado.
    """
    jira_url, jira_token, jira_email = load_config()
    issue_id=sys.argv[1]
    pauta=sys.argv[2]
    transition_issue(issue_id,
                     jira_url=jira_url,
                     jira_token=jira_token,
                     jira_email=jira_email,
                     id_transition=301)
    
    agregar_comentario(issue_id=issue_id,
                       jira_url=jira_url,
                       jira_email=jira_email,
                       jira_token=jira_token,
                       pauta=pauta)

            

if __name__ == "__main__":
    main()