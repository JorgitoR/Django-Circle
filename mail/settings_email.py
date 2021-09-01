import os





TASKS_SEND_EMAILS_TO_ASSIGNED = os.getenv('TASKS_SEND_EMAILS_TO_ASSIGNED', 'false') == 'true'
TASKS_SEND_EMAILS_TO_PARTNERS = os.getenv('TASKS_SEND_EMAILS_TO_PARTNERS', 'false') == 'true'


# Enables the Tornado Django Coleman Viewer (it will send emails with the order URL)
# Check: https://github.com/mrsarm/tornado-dcoleman-mtasks-viewer
TASKS_VIEWER_ENABLED = os.getenv('TASKS_VIEWER_ENABLED', 'false') == 'true'
TASKS_VIEWER_HASH_SALT = os.getenv('TASKS_VIEWER_HASH_SALT', '1two3')   # REPLACE in production !!!
TASKS_VIEWER_ENDPOINT = os.getenv('TASKS_VIEWER_ENDPOINT', 'http://localhost:8888/{number}?t={token}')

MTASKS_EMAIL_WITHOUT_URL = '''\
Nueva tarea creada #{id}.
Titulo:
{titulo}
Usuario Asignado:
{usuario}
Descripcion:
{descripcion}
Tenga en cuenta: No responder este Email. Este correo electrónico se envía desde un buzón desatendido.
No se leerán las respuestas.
---
{sign}
'''


MTASKS_EMAIL_WITH_URL = '''\
New task #{id} created.
Title:
{titulo}
Assigned:
{usuario}
Description:
{descripcion}

Please note: Do NOT reply to this email. This email is sent from an unattended mailbox.
Replies will not be read.
---
{sign}
'''




CREDENCIALES_USUARIO = '''\
{titulo}: {nombre} {apellido}
Usuario:
{username}
password:
{password}
Tenga en cuenta: No responder este Email. Este correo electrónico se envía desde un buzón desatendido.
No se leerán las respuestas.
---
{sign}
'''