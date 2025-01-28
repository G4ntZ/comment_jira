import configparser
import requests
import json
from requests.auth import HTTPBasicAuth
from config_credentials import load_config
import sys

RECHAZAR_QAT_CERTIFICACION = 531

def transition_issue(issue_key, jira_url, jira_token, jira_email, id_transition, urls, observaciones, pauta):
    """Cambia el estado de un issue utilizando la transición especificada."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    list_items = [
        {
            "type": "listItem",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": url,
                            "marks": [
                                {
                                    "type": "link",
                                    "attrs": {
                                        "href": url
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        for url in urls
    ]
    
    def attempt_transition(transition_id):
        data = {
            "transition": {
                "id": transition_id
            },
            "update": {
                "comment": [
                    {
                        "add": {
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
                                                        "text": "Revisión de Código",
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
                                                        "text": "Rechazado por SQA",
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
                                                                        "text": "bitbucket"
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
                                                        "text": "Observaciones",
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
                                            }
                                        ],
                                        "attrs": {
                                            "panelType": "error"
                                        }
                                    },
                                    {
                                        "type": "codeBlock",
                                        "attrs": {
                                            "language": "java"
                                        },
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": f"{observaciones}"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "panel",
                                        "content": [
                                            {
                                                "type": "bulletList",
                                                "content": list_items
                                            },
                                            {
                                                "type": "paragraph",
                                                "content": [
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
                                                    }
                                                ]
                                            }
                                        ],
                                        "attrs": {
                                            "panelType": "error"
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
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

    observaciones = "giros Security Hotspots Reviewed: 0 < 100\r\n Security Hotspots Reviewed: 0 < 100"
    
    urls = ["http://bamboo.afphabitat.net:8085/browse/CUEN-WSGQA0-2", 
            "http://bamboo.afphabitat.net:8085/browse/CUEN-GQA0-2"]
    
    transition_issue(issue_id,
                     jira_url=jira_url,
                     jira_token=jira_token,
                     jira_email=jira_email,
                     id_transition=RECHAZAR_QAT_CERTIFICACION,
                     pauta=pauta,
                     observaciones=observaciones,
                     urls=urls) #rechazar qat 
                       

            

if __name__ == "__main__":
    main()